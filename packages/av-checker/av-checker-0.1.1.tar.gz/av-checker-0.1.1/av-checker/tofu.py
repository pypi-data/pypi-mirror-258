import datetime
import hashlib
import logging
import os
import os.path
import sqlite3
import ssl
import time

try:
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend

    _HAS_CRYPTOGRAPHY = True
    _BACKEND = default_backend()
except ModuleNotFoundError:
    _HAS_CRYPTOGRAPHY = False

import util

ui_out = logging.getLogger("av_logger")


class TofuStore:

    def __init__(self, config_dir):

        self.config_dir = config_dir
        self.certdir = os.path.join(config_dir, "cert_cache")
        if not os.path.exists(self.certdir):
            os.makedirs(self.certdir)
        db_path = os.path.join(self.config_dir, "tofu.db")
        self.db_conn = sqlite3.connect(db_path)
        self.db_cur = self.db_conn.cursor()

        self.create_db()
        self.update_db()

    def create_db(self):
        self.db_cur.execute("""CREATE TABLE IF NOT EXISTS cert_cache
            (hostname text, port integer, address text, fingerprint text,
            first_seen date, last_seen date, count integer)""")

    def update_db(self):
        # Update 1 - check for port column
        try:
            self.db_cur.execute("""SELECT port FROM cert_cache where 1=0""")
            has_port = True
        except sqlite3.OperationalError:
            has_port = False
        if not has_port:
            self.db_cur.execute("""ALTER TABLE cert_cache ADD COLUMN port integer""")
            self.db_cur.execute("""UPDATE cert_cache SET port= 1965 WHERE count > 0""")

    def close(self):

        self.db_conn.commit()
        self.db_conn.close()

    def validate_cert(self, address, port, host, cert):
        """
        Validate a TLS certificate in TOFU mode.

        If the cryptography module is installed:
         - Check the certificate Common Name or SAN matches `host`
         - Check the certificate's not valid before date is in the past
         - Check the certificate's not valid after date is in the future

        Whether the cryptography module is installed or not, check the
        certificate's fingerprint against the TOFU database to see if we've
        previously encountered a different certificate for this hostname and
        port
        """

        now = datetime.datetime.utcnow()

        # Do 'advanced' checks if Cryptography library is installed
        if _HAS_CRYPTOGRAPHY:
            self.check_cert_expiry_and_names(cert, host, now)

        # Compute SHA256 fingerprint
        sha = hashlib.sha256()
        sha.update(cert)
        fingerprint = sha.hexdigest()

        # Have we been here before?
        self.db_cur.execute("""SELECT fingerprint, address, first_seen, last_seen, count
            FROM cert_cache WHERE hostname=? AND port=?""", (host, port))
        cached_certs = self.db_cur.fetchall()

        # If not, cache this first cert and we're done
        if not cached_certs:
            ui_out.debug("TOFU: Blindly trusting first ever certificate for this host!")
            self.cache_new_cert(cert, host, port, address, fingerprint, now)
            return

        # If we have, check the received cert against the cache
        if self.find_cert_in_cache(host, port, fingerprint, cached_certs, now):
            return

        # Handle an unrecognised cert
        ui_out.debug("TOFU: Unrecognised certificate {}!  Raising the alarm...".format(fingerprint))

        ## Find the most recently seen previous cert for reporting
        most_recent = None
        for cached_fingerprint, cached_address, first, last, count in cached_certs:
            if not most_recent or last > most_recent:
                most_recent = last
                most_recent_cert = cached_fingerprint
                most_recent_address = cached_address
                most_recent_count = count

        ## Report the situation
        print("****************************************")
        print("[SECURITY WARNING] Unrecognised certificate!")
        print("The certificate presented for {}:{} ({}) has never been seen before.".format(host, port, address))
        print("This MIGHT be a Man-in-the-Middle attack.")
        print("A different certificate has previously been seen {} times.".format(most_recent_count))
        if _HAS_CRYPTOGRAPHY:
            previous_ttl = self.get_cached_cert_expiry(most_recent_cert) - now
            if previous_ttl < datetime.timedelta():
                print("That certificate has expired, which reduces suspicion somewhat.")
            else:
                print("That certificate is still valid for: {}".format(previous_ttl))
        if most_recent_address == address:
            print("The new certificate is being served from the same IP address as the previous one.")
        else:
            print("The new certificate is being served from a DIFFERNET IP address as the previous one.")
        print("****************************************")
        print("Attempt to verify the new certificate fingerprint out-of-band:")
        print(fingerprint)

        ## Ask the question
        if util.ask_yes_no("Accept this new certificate?"):
            self.cache_new_cert(cert, host, port, address, fingerprint, now)
        else:
            raise Exception("TOFU Failure!")

    def cache_new_cert(self, cert, host, port, address, fingerprint, now):
        """
        Accept a new certificate for a given host/port combo.
        """
        # Save cert to disk
        with open(os.path.join(self.certdir, fingerprint + ".crt"), "wb") as fp:
            fp.write(cert)

        # Record in DB
        self.db_cur.execute("""INSERT INTO cert_cache
            (hostname, port, address, fingerprint, first_seen, last_seen, count)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
                            (host, port, address, fingerprint, now, now, 1))
        self.db_conn.commit()

    def check_cert_expiry_and_names(self, cert, host, now):
        """
         - Check the certificate Common Name or SAN matches `host`
         - Check the certificate's not valid before date is in the past
         - Check the certificate's not valid after date is in the future
        """
        c = x509.load_der_x509_certificate(cert, _BACKEND)

        # Check certificate validity dates
        if c.not_valid_before >= now:
            raise ssl.CertificateError("Certificate not valid until: {}!".format(c.not_valid_before))
        elif c.not_valid_after <= now:
            raise ssl.CertificateError("Certificate expired as of: {})!".format(c.not_valid_after))

        # Check certificate hostnames
        names = []
        common_name = c.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)
        if common_name:
            names.append(common_name[0].value)
        try:
            names.extend([alt.value for alt in
                          c.extensions.get_extension_for_oid(x509.oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME).value])
        except x509.ExtensionNotFound:
            pass
        names = set(names)
        for name in names:
            try:
                ssl._dnsname_match(name, host)
                break
            except Exception:
                continue
        else:
            # If we didn't break out, none of the names were valid
            raise ssl.CertificateError("Hostname does not match certificate common name or any alternative names.")

    def find_cert_in_cache(self, host, port, fingerprint, cached_certs, now):
        """
        Try to find a cached certificate for the given host:port matching the
        given fingerprint.  If one is found, update the "last seen" DB value.
        """
        for cached_fingerprint, cached_address, first, last, count in cached_certs:
            if fingerprint == cached_fingerprint:
                # Matched!
                ui_out.debug("TOFU: Accepting previously seen ({} times) certificate {}".format(count, fingerprint))
                self.db_cur.execute("""UPDATE cert_cache
                    SET last_seen=?, count=?
                    WHERE hostname=? AND port=? AND fingerprint=?""",
                                    (now, count + 1, host, port, fingerprint))
                self.db_conn.commit()
                return True
        return False

    def get_cached_cert_expiry(self, fingerprint):
        """
        Parse the stored certificate with a given fingerprint and return its
        expiry date.
        """
        with open(os.path.join(self.certdir, fingerprint + ".crt"), "rb") as fp:
            previous_cert = fp.read()
        previous_cert = x509.load_der_x509_certificate(previous_cert, _BACKEND)
        return previous_cert.not_valid_after
