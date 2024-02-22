import glob
import logging
import os
import os.path
import uuid

import util

ui_out = logging.getLogger("av_logger")


class ClientCertificateManager:

    def __init__(self, config_dir):

        self.config_dir = config_dir
        self.client_certs = {
            "active": None
        }
        self.active_cert_domains = []
        self.active_is_transient = False
        self.transient_certs_created = []

    def cleanup(self):
        for cert in self.transient_certs_created:
            for ext in (".crt", ".key"):
                certfile = os.path.join(self.config_dir, "transient_certs", cert + ext)
                if os.path.exists(certfile):
                    os.remove(certfile)

    def manage(self):
        if self.client_certs["active"]:
            print("Active certificate: {}".format(self.client_certs["active"][0]))
        print("1. Deactivate client certificate.")
        print("2. Generate new certificate.")
        print("3. Load previously generated certificate.")
        print("4. Load externally created client certificate from file.")
        print("Enter blank line to exit certificate manager.")
        choice = input("> ").strip()
        if choice == "1":
            print("Deactivating client certificate.")
            self._deactivate_client_cert()
        elif choice == "2":
            self._generate_persistent_client_cert()
        elif choice == "3":
            self._choose_client_cert()
        elif choice == "4":
            self._load_client_cert()
        else:
            print("Aborting.")

    def associate_client_cert(self, context, gi):
        # Be careful with client certificates!
        # Are we crossing a domain boundary?
        if self.client_certs["active"] and gi.host not in self.active_cert_domains:
            if self.active_is_transient:
                if util.ask_yes_no("Permanently delete currently active transient certificate?"):
                    print("Destroying certificate.")
                    self._deactivate_client_cert()
                else:
                    print("Staying here.")
                    return False
            else:
                if util.ask_yes_no("PRIVACY ALERT: Deactivate client cert before connecting to a new domain?"):
                    print("Deactivating certificate.")
                    self._deactivate_client_cert()
                else:
                    print("Keeping certificate active for {}".format(gi.host))
                    self.active_cert_domains.append(gi.host)
                    self.client_certs[gi.host] = self.client_certs["active"]

        # Suggest reactivating previous certs
        if not self.client_certs["active"] and gi.host in self.client_certs:
            if util.ask_yes_no("PRIVACY ALERT: Reactivate previously used client cert for {}?".format(gi.host)):
                self._activate_client_cert(*self.client_certs[gi.host])
                self.active_cert_domains.append(gi.host)
            else:
                print("Remaining unidentified.")
                self.client_certs.pop(gi.host)

        # Associate certs to context based on above
        if self.client_certs["active"]:
            certfile, keyfile = self.client_certs["active"]
            context.load_cert_chain(certfile, keyfile)

        return True

    def is_cert_active(self):
        return self.client_certs["active"] != None

    def handle_cert_request(self, meta, status, host):

        # Don't do client cert stuff in restricted mode, as in principle
        # it could be used to fill up the disk by creating a whole lot of
        # certificates
        print("SERVER SAYS: ", meta)
        # Present different messages for different 6x statuses, but
        # handle them the same.
        if status in ("64", "65"):
            print("The server rejected your certificate because it is either expired or not yet valid.")
        elif status == "63":
            print("The server did not accept your certificate.")
            print("You may need to e.g. coordinate with the admin to get your certificate fingerprint whitelisted.")
        else:
            print("The site {} is requesting a client certificate.".format(host))
            print("This will allow the site to recognise you across requests.")

        # Give the user choices
        print("What do you want to do?")
        print("1. Give up.")
        print("2. Generate a new transient certificate.")
        print("3. Generate a new persistent certificate.")
        print("4. Load a previously generated certificate.")
        print("5. Load a certificate from an external file.")
        choice = input("> ").strip()
        if choice == "2":
            self._generate_transient_cert_cert()
        elif choice == "3":
            self._generate_persistent_client_cert()
        elif choice == "4":
            self._choose_client_cert()
        elif choice == "5":
            self._load_client_cert()
        else:
            print("Giving up.")
            return False

        if self.client_certs["active"]:
            self.active_cert_domains.append(host)
            self.client_certs[host] = self.client_certs["active"]

        return True

    def _load_client_cert(self):
        """
        Interactively load a TLS client certificate from the filesystem in PEM
        format.
        """
        print("Loading client certificate file, in PEM format (blank line to cancel)")
        certfile = input("Certfile path: ").strip()
        if not certfile:
            print("Aborting.")
            return
        certfile = os.path.expanduser(certfile)
        if not os.path.isfile(certfile):
            print("Certificate file {} does not exist.".format(certfile))
            return
        print("Loading private key file, in PEM format (blank line to cancel)")
        keyfile = input("Keyfile path: ").strip()
        if not keyfile:
            print("Aborting.")
            return
        keyfile = os.path.expanduser(keyfile)
        if not os.path.isfile(keyfile):
            print("Private key file {} does not exist.".format(keyfile))
            return
        self._activate_client_cert(certfile, keyfile)

    def _generate_transient_cert_cert(self):
        """
        Use `openssl` command to generate a new transient client certificate
        with 24 hours of validity.
        """
        certdir = os.path.join(self.config_dir, "transient_certs")
        name = str(uuid.uuid4())
        self._generate_client_cert(certdir, name, transient=True)
        self.active_is_transient = True
        self.transient_certs_created.append(name)

    def _generate_persistent_client_cert(self):
        """
        Interactively use `openssl` command to generate a new persistent client
        certificate with one year of validity.
        """
        certdir = os.path.join(self.config_dir, "client_certs")
        print("What do you want to name this new certificate?")
        print("Answering `mycert` will create `{0}/mycert.crt` and `{0}/mycert.key`".format(certdir))
        name = input("> ")
        if not name.strip():
            print("Aborting.")
            return
        self._generate_client_cert(certdir, name)

    def _generate_client_cert(self, certdir, basename, transient=False):
        """
        Use `openssl` binary to generate a client certificate (which may be
        transient or persistent) and save the certificate and private key to the
        specified directory with the specified basename.
        """
        if not os.path.exists(certdir):
            os.makedirs(certdir)
        certfile = os.path.join(certdir, basename + ".crt")
        keyfile = os.path.join(certdir, basename + ".key")
        cmd = "openssl req -x509 -newkey rsa:2048 -days {} -nodes -keyout {} -out {}".format(1 if transient else 365,
                                                                                             keyfile, certfile)
        if transient:
            cmd += " -subj '/CN={}'".format(basename)
        os.system(cmd)
        self._activate_client_cert(certfile, keyfile)

    def _choose_client_cert(self):
        """
        Interactively select a previously generated client certificate and
        activate it.
        """
        certdir = os.path.join(self.config_dir, "client_certs")
        certs = glob.glob(os.path.join(certdir, "*.crt"))
        if len(certs) == 0:
            print("There are no previously generated certificates.")
            return
        certdir = {}
        for n, cert in enumerate(certs):
            certdir[str(n + 1)] = (cert, os.path.splitext(cert)[0] + ".key")
            print("{}. {}".format(n + 1, os.path.splitext(os.path.basename(cert))[0]))
        choice = input("> ").strip()
        if choice in certdir:
            certfile, keyfile = certdir[choice]
            self._activate_client_cert(certfile, keyfile)
        else:
            print("What?")

    def _activate_client_cert(self, certfile, keyfile):
        self.client_certs["active"] = (certfile, keyfile)
        self.active_cert_domains = []
        ui_out.debug("Using ID {} / {}.".format(*self.client_certs["active"]))

    def _deactivate_client_cert(self):
        if self.active_is_transient:
            for filename in self.client_certs["active"]:
                os.remove(filename)
            for domain in self.active_cert_domains:
                self.client_certs.pop(domain)
        self.client_certs["active"] = None
        self.active_cert_domains = []
        self.active_is_transient = False
