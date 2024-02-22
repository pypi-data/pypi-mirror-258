

import cmd
import cgi
import codecs
import fnmatch
import getpass
import logging
import mimetypes
import os
import os.path
import shlex
import shutil
import socket
import ssl
import subprocess
import sys
import tempfile
import time
import traceback
import urllib.parse
import webbrowser


try:
    import ansiwrap as textwrap
except ModuleNotFoundError:
    import textwrap

from __init__ import __version__
from cache import Cache
from tofu import TofuStore
from certmanager import ClientCertificateManager
import util

_MAX_REDIRECTS = 5

# Command abbreviations
_ABBREVS = {
    "a":    "add",
    "b":    "back",
    "bb":   "blackbox",
    "bm":   "bookmarks",
    "book": "bookmarks",
    "f":    "fold",
    "fo":   "forward",
    "g":    "go",
    "h":    "history",
    "hist": "history",
    "l":    "less",
    "n":    "next",
    "p":    "previous",
    "prev": "previous",
    "q":    "quit",
    "r":    "reload",
    "s":    "save",
    "se":   "search",
    "/":    "filter",
    "t":    "tour",
    "u":    "up",
}

_MIME_HANDLERS = {
    "application/pdf":      "xpdf %s",
    "audio/mpeg":           "mpg123 %s",
    "audio/ogg":            "ogg123 %s",
    "image/*":              "feh %s",
    "text/html":            "lynx -dump -force_html %s",
    "text/*":               "cat %s",
}

# monkey-patch Gemini support in urllib.parse
# see https://github.com/python/cpython/blob/master/Lib/urllib/parse.py
urllib.parse.uses_relative.append("gemini")
urllib.parse.uses_netloc.append("gemini")

# Set up logging (annoying necessity after splitting client into multiple
# .py files...was it worth it?
class AV98Formatter(logging.Formatter):
    def format(self, record):
        output = super().format(record)
        if record.levelno == logging.DEBUG:
            return "\x1b[0;32m[DEBUG] " + output + "\x1b[0m"
            return "[DEBUG] " + output
        else:
            return output
ui_out = logging.getLogger("av98_logger")
ui_handler = logging.StreamHandler()
ui_handler.setFormatter(AV98Formatter())
ui_out.addHandler(ui_handler)

standard_ports = {
        "gemini": 1965,
        "gopher": 70,
}

class GeminiItem():

    def __init__(self, url, name=""):
        if "://" not in url:
            url = "gemini://" + url
        self.url = util.fix_ipv6_url(url)
        self.name = name
        parsed = urllib.parse.urlparse(self.url)
        self.scheme = parsed.scheme
        self.host = parsed.hostname
        self.port = parsed.port or standard_ports.get(self.scheme, 0)
        self.path = parsed.path

    def root(self):
        return GeminiItem(self._derive_url("/"))

    def user(self):
        if not self.path.startswith("/~"):
            raise ValueError("This is not a tilde URL.")
        new_path = self.path.split("/")[1] + "/"
        print(new_path)
        return GeminiItem(self._derive_url(new_path))

    def up(self):
        pathbits = list(os.path.split(self.path.rstrip('/')))
        # Don't try to go higher than root
        if len(pathbits) == 1:
            return self
        # Get rid of bottom component
        pathbits.pop()
        new_path = os.path.join(*pathbits)
        return GeminiItem(self._derive_url(new_path))

    def query(self, query):
        query = urllib.parse.quote(query)
        return GeminiItem(self._derive_url(query=query))

    def _derive_url(self, path="", query=""):
        """
        A thin wrapper around urlunparse which avoids inserting standard ports
        into URLs just to keep things clean.
        """
        return urllib.parse.urlunparse((self.scheme,
            self.host if self.port == standard_ports[self.scheme] else self.host + ":" + str(self.port),
            path or self.path, "", query, ""))

    def absolutise_url(self, relative_url):
        """
        Convert a relative URL to an absolute URL by using the URL of this
        GeminiItem as a base.
        """
        return urllib.parse.urljoin(self.url, relative_url)

    def to_map_line(self, name=None):
        if name or self.name:
            return "=> {} {}\n".format(self.url, name or self.name)
        else:
            return "=> {}\n".format(self.url)

    def derive_filename(self, mime=None):
        # Simplest option it to use the end of the URL, if there is one.
        filename = os.path.basename(self.path)
        if filename:
            return filename

        # If there's not, try to pretty up the GeminiItem name
        if self.name:
            filename = self.name.lower().replace(" ","_")
        # Otherwise, use something generic.
        else:
            filename = "av98_download_" + time.strftime("%Y%m%d%H%M%S")

        # Add an extension
        if mime == "text/gemini":
            return filename + ".gmi"
        elif mime:
            ext = mimetypes.guess_extension(mime)
            if ext:
                return filename + ext
        return filename + ".file"

    @classmethod
    def from_map_line(cls, line, origin_gi):
        assert line.startswith("=>")
        assert line[2:].strip()
        bits = line[2:].strip().split(maxsplit=1)
        bits[0] = origin_gi.absolutise_url(bits[0])
        return cls(*bits)

CRLF = '\r\n'

class UserAbortException(Exception):
    pass

# GeminiClient Decorators
def needs_gi(inner):
    def outer(self, *args, **kwargs):
        if not self.gi:
            print("You need to 'go' somewhere, first")
            return None
        else:
            return inner(self, *args, **kwargs)
    outer.__doc__ = inner.__doc__
    return outer

def restricted(inner):
    def outer(self, *args, **kwargs):
        if self.restricted:
            print("Sorry, this command is not available in restricted mode!")
            return None
        else:
            return inner(self, *args, **kwargs)
    outer.__doc__ = inner.__doc__
    return outer

class GeminiClient(cmd.Cmd):

    def __init__(self, restricted=False):
        cmd.Cmd.__init__(self)

        self.no_cert_prompt = "\x1b[38;5;76m" + "AV-98" + "\x1b[38;5;255m" + "> " + "\x1b[0m"
        self.cert_prompt = "\x1b[38;5;202m" + "AV-98" + "\x1b[38;5;255m" + "+cert> " + "\x1b[0m"
        self.prompt = self.no_cert_prompt
        self.gi = None
        self.history = []
        self.hist_index = 0
        self.index = []
        self.index_index = -1
        self.lookup = self.index
        self.marks = {}
        self.page_index = 0
        self.permanent_redirects = {}
        self.restricted = restricted
        self.active_raw_file = ""
        self.active_rendered_file = ""
        self.visited_hosts = set()
        self.waypoints = []

        self.options = {
            "debug" : False,
            "ipv6" : True,
            "timeout" : 10,
            "width" : 80,
            "auto_follow_redirects" : True,
            "tls_mode" : "tofu",
            "gopher_proxy" : None,
            "http_proxy": None,
            "cache" : False,
            "search_url" : "gemini://geminispace.info/search"
        }

        self.log = {
            "start_time": time.time(),
            "requests": 0,
            "ipv4_requests": 0,
            "ipv6_requests": 0,
            "bytes_recvd": 0,
            "ipv4_bytes_recvd": 0,
            "ipv6_bytes_recvd": 0,
            "dns_failures": 0,
            "refused_connections": 0,
            "reset_connections": 0,
            "timeouts": 0,
            "cache_hits": 0,
            "redirects_followed": 0
        }

        self._stop = False
        self._init_config()
        ui_out.debug("Raw buffer: ", self.raw_file_buffer)
        ui_out.debug("Rendered buffer: ", self.rendered_file_buffer)
        self.tofu_store = TofuStore(self.config_dir)
        self.client_cert_manager = ClientCertificateManager(self.config_dir)
        self.cache = Cache()

    def _init_config(self):
        # Set umask so that nothing we create can be read by anybody else.
        # The certificate cache and TOFU database contain "browser history"
        # type sensitivie information.
        os.umask(0o077)

        # Find or create config directory
        ## Look for something pre-existing
        for confdir in ("~/.av98/", "~/.config/av98/"):
            confdir = os.path.expanduser(confdir)
            if os.path.exists(confdir):
                self.config_dir = confdir
                break
        ## Otherwise, make one in .config if it exists
        else:
            if os.path.exists(os.path.expanduser("~/.config/")):
                self.config_dir = os.path.expanduser("~/.config/av98/")
            else:
                self.config_dir = os.path.expanduser("~/.av98/")
            print("Creating config directory {}".format(self.config_dir))
            os.makedirs(self.config_dir)

        # Set some filename constants
        self.bm_file = os.path.join(self.config_dir, "bookmarks.gmi")
        # Claim two temporary filenames to use as buffers
        self.raw_file_buffer = tempfile.NamedTemporaryFile(delete=False).name
        self.rendered_file_buffer = tempfile.NamedTemporaryFile(delete=False).name

    def _go_to_gi(self, gi, update_hist=True, check_cache=True):
        """
        This method might be considered "the heart of AV-98".
        Everything involved in fetching a gemini resource happens here:
        sending the request over the network, parsing the response if
        its a menu, storing the response in a temporary file, choosing
        and calling a handler program, and updating the history.
        Most navigation commands are just a thin wrapper around a call
        to this.
        """

        # Don't try to speak to servers running other protocols
        if gi.scheme in ("http", "https"):
            if not self.options.get("http_proxy",None):
                webbrowser.open_new_tab(gi.url)
                return
            else:
                if not util.ask_yes_no("Do you want to try to open this link with a http proxy?", True):
                    webbrowser.open_new_tab(gi.url)
                    return
        elif gi.scheme == "gopher" and not self.options.get("gopher_proxy", None):
            print("""AV-98 does not speak Gopher natively.
However, you can use `set gopher_proxy hostname:port` to tell it about a
Gopher-to-Gemini proxy (such as a running Agena instance), in which case
you'll be able to transparently follow links to Gopherspace!""")
            return
        elif gi.scheme not in ("file", "gemini", "gopher"):
            print("Sorry, no support for {} links.".format(gi.scheme))
            return

        # Use local file, use cache, or hit the network if resource is not cached
        try:
            if gi.scheme == "file":
                if not os.path.exists(gi.path):
                    raise FileNotFoundError
                elif os.path.isdir(gi.path):
                    raise IsADirectoryError
                mime = self._handle_local_file(gi)
                self.active_raw_file = gi.path
            elif check_cache and self.options["cache"] and self.cache.check(gi.url):
                mime, self.active_raw_file = self.cache.get(gi.url)
                self.log["cache_hits"] += 1
            else:
                gi, mime = self._fetch_over_network(gi)
                self.active_raw_file = self.raw_file_buffer
        except UserAbortException:
            return
        except Exception as err:
            self._print_friendly_error(err)
            return

        # Render gemtext, updating the index
        if mime == "text/gemini":
            self._handle_gemtext(gi)
            self.active_rendered_file = self.rendered_file_buffer
        else:
            self.active_rendered_file = self.active_raw_file

        # Pass file to handler
        cmd_str = self._get_handler_cmd(mime)
        try:
            subprocess.call(shlex.split(cmd_str % self.active_rendered_file))
        except FileNotFoundError:
            print("Handler program %s not found!" % shlex.split(cmd_str)[0])
            print("You can use the ! command to specify another handler program or pipeline.")

        # Update state
        self.gi = gi
        self.mime = mime
        if update_hist:
            self._update_history(gi)

    def _handle_local_file(self, gi):
        """
        Guess the MIME type of local file, to determine the best handler.
        """
        mime, noise = mimetypes.guess_type(gi.path)
        if not mime:
            if gi.path.endswith(".gmi"):    # TODO: be better about this
                mime = "text/gemini"
        return mime

    def _fetch_over_network(self, gi, destination=None):
        """
        Fetch the provided GeminiItem over the network and save the received
        content to a file.
        """
        previous_redirectors = set()
        while True:
            # Obey permanent redirects
            if gi.url in self.permanent_redirects:
                gi = GeminiItem(self.permanent_redirects[gi.url], name=gi.name)
                continue

            # Send request to server
            status, meta, address, f = self._send_request(gi)

            # Update redirect loop/maze escaping state
            if not status.startswith("3"):
                previous_redirectors = set()

            # Handle non-SUCCESS headers, which don't have a response body
            # Inputs
            if status.startswith("1"):
                if status == "11":
                    user_input = getpass.getpass(meta + "\n> ")
                else:
                    user_input = input(meta + "\n> ")
                gi = gi.query(user_input)
                continue

            # Redirects
            elif status.startswith("3"):
                new_gi = GeminiItem(gi.absolutise_url(meta))
                if new_gi.url == gi.url:
                    raise RuntimeError("URL redirects to itself!")
                elif new_gi.url in previous_redirectors:
                    raise RuntimeError("Caught in redirect loop!")
                elif len(previous_redirectors) == _MAX_REDIRECTS:
                    raise RuntimeError("Refusing to follow more than %d consecutive redirects!" % _MAX_REDIRECTS)
                # Never follow cross-domain redirects without asking
                elif new_gi.host != gi.host:
                    follow = util.ask_yes_no("Follow cross-domain redirect to %s?" % new_gi.url)
                # Never follow cross-protocol redirects without asking
                elif new_gi.scheme != gi.scheme:
                    follow = util.ask_yes_no("Follow cross-protocol redirect to %s?" % new_gi.url)
                # Don't follow *any* redirect without asking if auto-follow is off
                elif not self.options["auto_follow_redirects"]:
                    follow = util.ask_yes_no("Follow redirect to %s?" % new_gi.url)
                # Otherwise, follow away
                else:
                    follow = True
                if not follow:
                    raise UserAbortException()
                ui_out.debug("Following redirect to %s." % new_gi.url)
                ui_out.debug("This is consecutive redirect number %d." % len(previous_redirectors))
                previous_redirectors.add(gi.url)
                self.log["redirects_followed"] += 1
                if status == "31":
                    # Permanent redirect
                    self.permanent_redirects[gi.url] = new_gi.url
                gi = new_gi
                continue

            # Errors
            elif status.startswith("4") or status.startswith("5"):
                raise RuntimeError(meta)

            # Client cert
            elif status.startswith("6"):
                if self.restricted:
                    print("The server is requesting a client certificate.")
                    print("These are not supported in restricted mode, sorry.")
                    raise UserAbortException()

                if not self.client_cert_manager.handle_cert_request(meta, status, gi.host):
                    raise UserAbortException()
                continue

            # Invalid status
            elif not status.startswith("2"):
                raise RuntimeError("Server returned undefined status code %s!" % status)

            # If we're here, this must be a success and there's a response body,
            # so break out of the request loop
            assert status.startswith("2")
            break

        # Fill in default MIME type or validate a provided one
        mime = meta
        if mime == "":
            mime = "text/gemini; charset=utf-8"
        mime, mime_options = cgi.parse_header(mime)
        if "charset" in mime_options:
            try:
                codecs.lookup(mime_options["charset"])
            except LookupError:
                raise RuntimeError("Header declared unknown encoding")

        # Save response body to disk
        size = self._write_response_to_file(mime, mime_options, f, destination)
        ui_out.debug("Wrote %d byte response to %s." % (size, destination or self.raw_file_buffer))

        # Maintain cache and update flight recorder
        if self.options["cache"]:
            self.cache.add(gi.url, mime, self.raw_file_buffer)
        self._log_visit(gi, address, size)

        return gi, mime

    def _send_request(self, gi):
        """
        Send a Gemini request to the appropriate host for the provided
        GeminiItem.  This is usually the GI's own host and port attributes,
        but if it's a gopher:// or http(s):// item, a proxy might be used.

        Returns the received response header, parsed into a status code
        and meta, plus a the address object that was connected to and a
        file interface to the underlying network socket.
        """

        # Figure out which host to connect to
        if gi.scheme == "gemini":
            # For Gemini requests, connect to the host and port specified in the URL
            host, port = gi.host, gi.port
        elif gi.scheme == "gopher":
            # For Gopher requests, use the configured proxy
            host, port = self.options["gopher_proxy"].rsplit(":", 1)
            ui_out.debug("Using gopher proxy: " + self.options["gopher_proxy"])
        elif gi.scheme in ("http", "https"):
            host, port = self.options["http_proxy"].rsplit(":",1)
            ui_out.debug("Using http proxy: " + self.options["http_proxy"])

        # Do DNS resolution
        try:
            addresses = self._get_addresses(host, port)
        except Exception as err:
            if isinstance(err, socket.gaierror):
                self.log["dns_failures"] += 1
            raise err

        # Prepare TLS context
        context = self._prepare_SSL_context(self.options["tls_mode"])
        if not self.client_cert_manager.associate_client_cert(context, gi):
            raise UserAbortException()
        if self.client_cert_manager.is_cert_active():
            self.prompt = self.cert_prompt
        else:
            self.prompt = self.no_cert_prompt

        # Connect to remote host by any address possible
        err = None
        for address in addresses:
            ui_out.debug("Connecting to: " + str(address[4]))
            s = socket.socket(address[0], address[1])
            s.settimeout(self.options["timeout"])
            s = context.wrap_socket(s, server_hostname = gi.host)
            try:
                s.connect(address[4])
                break
            except Exception as e:
                err = e
                # Log network errors
                if isinstance(err, ConnectionRefusedError):
                    self.log["refused_connections"] += 1
                elif isinstance(err, ConnectionResetError):
                    self.log["reset_connections"] += 1
                elif isinstance(err, (TimeoutError, socket.timeout)):
                    self.log["timeouts"] += 1
        else:
            # If we couldn't connect to *any* of the addresses, just
            # bubble up the exception from the last attempt for the
            # sake of error reporting to the user.
            raise err

        if sys.version_info.minor >=5:
            ui_out.debug("Established {} connection.".format(s.version()))
        ui_out.debug("Cipher is: {}.".format(s.cipher()))

        # Do TOFU
        if self.options["tls_mode"] == "tofu":
            cert = s.getpeercert(binary_form=True)
            self.tofu_store.validate_cert(address[4][0], address[4][1], host, cert)

        # Send request and wrap response in a file descriptor
        ui_out.debug("Sending %s<CRLF>" % gi.url)
        s.sendall((gi.url + CRLF).encode("UTF-8"))
        f = s.makefile(mode = "rb")

        # Fetch response header
        # Spec dictates <META> should not exceed 1024 bytes,
        # so maximum valid header length is 1027 bytes.
        header = f.readline(1027)
        header = header.decode("UTF-8")
        if not header or header[-1] != '\n':
            raise RuntimeError("Received invalid header from server!")
        header = header.strip()
        ui_out.debug("Response header: %s." % header)

        # Validate response header
        status, meta = header.split(maxsplit=1) if header[2:].strip() else (header[:2], "")
        if len(meta) > 1024 or len(status) != 2 or not status.isnumeric():
            f.close()
            raise RuntimeError("Received invalid header from server!")

        return status, meta, address, f

    def _get_addresses(self, host, port):
        """
        Convert a host and port into an address object suitable for
        instantiating a socket.
        """
        # DNS lookup - will get IPv4 and IPv6 records if IPv6 is enabled
        if ":" in host:
            # This is likely a literal IPv6 address, so we can *only* ask for
            # IPv6 addresses or getaddrinfo will complain
            family_mask = socket.AF_INET6
        elif socket.has_ipv6 and self.options["ipv6"]:
            # Accept either IPv4 or IPv6 addresses
            family_mask = 0
        else:
            # IPv4 only
            family_mask = socket.AF_INET
        addresses = socket.getaddrinfo(host, port, family=family_mask,
                type=socket.SOCK_STREAM)
        # Sort addresses so IPv6 ones come first
        addresses.sort(key=lambda add: add[0] == socket.AF_INET6, reverse=True)

        return addresses

    def _prepare_SSL_context(self, cert_validation_mode="tofu"):
        """
        Specify a bunch of low level SSL settings.
        """
        # Flail against version churn
        if sys.version_info >= (3, 10):
            _newest_supported_protocol = ssl.PROTOCOL_TLS_CLIENT
        elif sys.version_info >= (3, 6):
            _newest_supported_protocol = ssl.PROTOCOL_TLS
        else:
            _newest_supported_protocol = ssl.PROTOCOL_TLSv1_2
        context = ssl.SSLContext(_newest_supported_protocol)

        # Use CAs or TOFU
        if cert_validation_mode == "ca":
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
            context.load_default_certs()
        else:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

        # Impose minimum TLS version
        ## In 3.7 and above, this is easy...
        if sys.version_info.minor >= 7:
            context.minimum_version = ssl.TLSVersion.TLSv1_2
        ## Otherwise, it seems very hard...
        ## The below is less strict than it ought to be, but trying to disable
        ## TLS v1.1 here using ssl.OP_NO_TLSv1_1 produces unexpected failures
        ## with recent versions of OpenSSL.  What a mess...
        else:
            context.options |= ssl.OP_NO_SSLv3
            context.options |= ssl.OP_NO_SSLv2

        # Try to enforce sensible ciphers
        try:
            context.set_ciphers("AESGCM+ECDHE:AESGCM+DHE:CHACHA20+ECDHE:CHACHA20+DHE:!DSS:!SHA1:!MD5:@STRENGTH")
        except ssl.SSLError:
            # Rely on the server to only support sensible things, I guess...
            pass

        return context

    def _write_response_to_file(self, mime, mime_options, f, destination):
        """
        Given a file handler representing a network socket which will yield
        the response body for a successful Gemini request, and the associated
        MIME information, download the response body and save it in the
        specified file.  text/* responses which use an encoding other than
        UTF-8 will be transcoded to UTF-8 before hitting the disk.

        Returns the size in bytes of the downloaded response.
        """
        # Read the response body over the network
        spinner_seq = ["|", "/", "-", "\\"]
        body = bytearray([])
        chunk_count = 0
        while True:
            chunk = f.read(100*1024)
            chunk_count += 1
            if not chunk:
                break
            body.extend(chunk)
            if chunk_count > 1:
                spinner = spinner_seq[chunk_count % 4]
                if chunk_count < 10:
                    print("{} Received {} KiB...".format(spinner, chunk_count*100), end="\r")
                else:
                    print("{} Received {} MiB...".format(spinner, chunk_count/10.0), end="\r")
        print(" "*80, end="\r") # Clean up prompt space
        size = len(body)

        # Determine file mode
        if mime.startswith("text/"):
            mode = "w"
            # Decode received bytes with response-specified encoding...
            encoding = mime_options.get("charset", "UTF-8")
            try:
                body = body.decode(encoding)
            except UnicodeError:
                raise RuntimeError("Could not decode response body using %s encoding declared in header!" % encoding)
            # ...but alway save to disk in UTF-8
            encoding = "UTF-8"
        else:
            mode = "wb"
            encoding = None

        # Write
        with open(destination or self.raw_file_buffer, mode=mode, encoding=encoding) as fp:
            fp.write(body)

        return size

    def _log_visit(self, gi, address, size):
        """
        Update the "black box flight recorder" with details of requests and
        responses.
        """
        if not address:
            return
        self.log["requests"] += 1
        self.log["bytes_recvd"] += size
        self.visited_hosts.add(address)
        if address[0] == socket.AF_INET:
            self.log["ipv4_requests"] += 1
            self.log["ipv4_bytes_recvd"] += size
        elif address[0] == socket.AF_INET6:
            self.log["ipv6_requests"] += 1
            self.log["ipv6_bytes_recvd"] += size

    def _handle_gemtext(self, menu_gi):
        """
        Simultaneously parse and render a text/gemini document.
        Parsing causes self.index to be populated with GeminiItems
        representing the links in the document.
        Rendering causes self.rendered_file_buffer to contain a rendered
        view of the document.
        """
        self.index = []
        preformatted = False
        title = ""

        with open(self.active_raw_file, "r") as fp:
            body = fp.read()
        with open(self.rendered_file_buffer, "w") as fp:
            for line in body.splitlines():
                if line.startswith("```"):
                    preformatted = not preformatted
                elif preformatted:
                    fp.write(line + "\n")
                elif line.startswith("=>"):
                    try:
                        gi = GeminiItem.from_map_line(line, menu_gi)
                        self.index.append(gi)
                        fp.write(self._format_geminiitem(len(self.index), gi) + "\n")
                    except:
                        ui_out.debug("Skipping possible link: %s" % line)
                elif line.startswith("* "):
                    line = line[1:].lstrip("\t ")
                    fp.write(textwrap.fill(line, self.options["width"],
                        initial_indent = "• ", subsequent_indent="  ") + "\n")
                elif line.startswith(">"):
                    line = line[1:].lstrip("\t ")
                    fp.write(textwrap.fill(line, self.options["width"],
                        initial_indent = "> ", subsequent_indent="> ") + "\n")
                elif line.startswith("###"):
                    line = line[3:].lstrip("\t ")
                    fp.write("\x1b[4m" + line + "\x1b[0m""\n")
                elif line.startswith("##"):
                    line = line[2:].lstrip("\t ")
                    fp.write("\x1b[1m" + line + "\x1b[0m""\n")
                elif line.startswith("#"):
                    line = line[1:].lstrip("\t ")
                    fp.write("\x1b[1m\x1b[4m" + line + "\x1b[0m""\n")
                    if not title:
                        title = line
                else:
                    fp.write(textwrap.fill(line, self.options["width"]) + "\n")

        self.lookup = self.index
        self.page_index = 0
        self.index_index = -1

        # If the supplied GI didn't have a name (e.g. we arrived at it from a
        # manually entered URL, not a link), use the title inferred from the
        # first top level header
        if not menu_gi.name:
                menu_gi.name = title

    def _format_geminiitem(self, index, gi, url=False):
        """
        Render a link line.
        """
        protocol = "" if gi.scheme == "gemini" else " %s" % gi.scheme
        line = "[%d%s] %s" % (index, protocol, gi.name or gi.url)
        if gi.name and url:
            line += " (%s)" % gi.url
        return line

    def _get_handler_cmd(self, mimetype):
        """
        Given the MIME type of a downloaded item, figure out which program to
        open it with.

        Returns a string suitable for use with subprocess.call after the '%s'
        has been replaced with the name of the file where the downloaded item
        was saved.
        """
        # Now look for a handler for this mimetype
        # Consider exact matches before wildcard matches
        exact_matches = []
        wildcard_matches = []
        for handled_mime, cmd_str in _MIME_HANDLERS.items():
            if "*" in handled_mime:
                wildcard_matches.append((handled_mime, cmd_str))
            else:
                exact_matches.append((handled_mime, cmd_str))
        for handled_mime, cmd_str in exact_matches + wildcard_matches:
            if fnmatch.fnmatch(mimetype, handled_mime):
                break
        else:
            # Use "xdg-open" as a last resort.
            cmd_str = "xdg-open %s"
        ui_out.debug("Using handler: %s" % cmd_str)
        return cmd_str

    def _update_history(self, gi):
        # Don't duplicate
        if self.history and self.history[self.hist_index] == gi:
            return
        self.history = self.history[0:self.hist_index+1]
        self.history.append(gi)
        self.hist_index = len(self.history) - 1

    def _print_friendly_error(self, err):
        if isinstance(err, socket.gaierror):
            ui_out.error("ERROR: DNS error!")
        elif isinstance(err, ConnectionRefusedError):
            ui_out.error("ERROR: Connection refused!")
        elif isinstance(err, ConnectionResetError):
            ui_out.error("ERROR: Connection reset!")
        elif isinstance(err, (TimeoutError, socket.timeout)):
            ui_out.error("""ERROR: Connection timed out!
Slow internet connection?  Use 'set timeout' to be more patient.""")
        elif isinstance(err, FileNotFoundError):
            ui_out.error("ERROR: Local file not found!")
        elif isinstance(err, IsADirectoryError):
            ui_out.error("ERROR: Viewing local directories is not supported!")
        elif isinstance(err, RuntimeError): # Misusing this for status 4x or 5x
            ui_out.error("ERROR: " + str(err))
        else:
            ui_out.error("ERROR: " + str(err))
            ui_out.debug(traceback.format_exc())

    def _show_lookup(self, offset=0, end=None, url=False):
        for n, gi in enumerate(self.lookup[offset:end]):
            print(self._format_geminiitem(n+offset+1, gi, url))

    def _maintain_bookmarks(self):
        """
        Update any bookmarks whose URLs we tried to fetch during the current
        session and received a permanent redirect for, so they are fetched
        directly at the new address in future.
        """
        # Nothing to do if no bookmarks exist!
        if not os.path.exists(self.bm_file):
            return

        # Backup bookmark file
        backup_file = tempfile.NamedTemporaryFile(delete=False)
        backup_file.close()
        backup_file = backup_file.name
        shutil.copyfile(self.bm_file, backup_file)

        # Attempt maintenance, restore backup if anything fails
        try:
            with open(backup_file, "r") as fp_old, open(self.bm_file, "w") as fp_new:
                for line in fp_old:
                    if not line.startswith("=>"):
                        fp_new.write(line)
                        continue
                    old_url = line.split()[1]
                    url = old_url
                    while url in self.permanent_redirects:
                        url = self.permanent_redirects[url]
                    if url != old_url:
                        ui_out.debug("Updating old bookmark url {} to {} based on permanent redirect.".format(old_url, url))
                    fp_new.write(line.replace(old_url, url))
        except Exception as err:
            shutil.copyfile(backup_file, self.bm_file)
            ui_out.debug(traceback.format_exc())
        finally:
            os.unlink(backup_file)

    # Cmd implementation follows

    def postcmd(self, stop, line):
        return self._stop

    def default(self, line):
        """
        This is called when none of the do_* methods match the user's
        input.  This is probably either an abbreviated command, or a numeric
        index for the lookup table.
        """
        if line.strip() == "EOF":
            return self.onecmd("quit")
        elif line.strip() == "..":
            return self.do_up()
        elif line.startswith("/"):
            return self.do_filter(line[1:])

        # Expand abbreviated commands
        first_word = line.split()[0].strip()
        if first_word in _ABBREVS:
            full_cmd = _ABBREVS[first_word]
            expanded = line.replace(first_word, full_cmd, 1)
            return self.onecmd(expanded)

        # Try to parse numerical index for lookup table
        try:
            n = int(line.strip())
        except ValueError:
            print("What?")
            return

        # Pick out a GeminiItemt
        try:
            gi = self.lookup[n-1]
        except IndexError:
            print ("Index too high!")
            return

        # Go to selected item
        self.index_index = n
        self._go_to_gi(gi)

    ### Settings

    @restricted
    def do_set(self, line):
        """View or set various options."""
        # Compute some constants for pretty alignment
        ljust = max((len(k) for k in self.options.keys()))
        rjust = max((len(str(v)) for v in self.options.values()))
        gap = 48 - (ljust + rjust)
        if not line.strip():
            # Show all current settings
            for option in sorted(self.options.keys()):
                print(option.ljust(ljust+gap) + str(self.options[option]).rjust(rjust))
        elif len(line.split()) == 1:
            # Show current value of one specific setting
            option = line.strip()
            if option in self.options:
                print(option.ljust(ljust+gap) + str(self.options[option]).rjust(rjust))
            else:
                print("Unrecognised option %s" % option)
        else:
            # Set value of one specific setting
            option, value = line.split(" ", 1)
            if option not in self.options:
                print("Unrecognised option %s" % option)
                return
            # Enable/disable debugging output
            if option == "debug":
                if value.lower() == "true":
                    ui_out.setLevel(logging.DEBUG)
                elif value.lower() == "false":
                    ui_out.setLevel(logging.INFO)

            # Validate / convert values
            if option == "gopher_proxy":
                if ":" not in value:
                    value += ":1965"
                else:
                    host, port = value.rsplit(":",1)
                    if not port.isnumeric():
                        print("Invalid proxy port %s" % port)
                        return
            elif option == "tls_mode":
                if value.lower() not in ("ca", "tofu"):
                    print("TLS mode must be `ca` or `tofu`!")
                    return
            elif value.isnumeric():
                value = int(value)
            elif value.lower() == "false":
                value = False
            elif value.lower() == "true":
                value = True
            else:
                try:
                    value = float(value)
                except ValueError:
                    pass
            self.options[option] = value

    @restricted
    def do_handler(self, line):
        """View or set handler commands for different MIME types."""
        if not line.strip():
            # Show all current handlers
            for mime in sorted(_MIME_HANDLERS.keys()):
                print("%s   %s" % (mime, _MIME_HANDLERS[mime]))
        elif len(line.split()) == 1:
            mime = line.strip()
            if mime in _MIME_HANDLERS:
                print("%s   %s" % (mime, _MIME_HANDLERS[mime]))
            else:
                print("No handler set for MIME type %s" % mime)
        else:
            mime, handler = line.split(" ", 1)
            _MIME_HANDLERS[mime] = handler
            if "%s" not in handler:
                print("Are you sure you don't want to pass the filename to the handler?")

    @restricted
    def do_cert(self, line):
        """Manage client certificates"""
        print("Managing client certificates")
        self.client_cert_manager.manage()

    ### Stuff for getting around
    def do_go(self, line):
        """Go to a gemini URL or marked item."""
        line = line.strip()
        if not line:
            print("Go where?")
        # First, check for possible marks
        elif line in self.marks:
            gi = self.marks[line]
            self._go_to_gi(gi)
        # or a local file
        elif os.path.exists(os.path.expanduser(line)):
            gi = GeminiItem("file://" + os.path.abspath(os.path.expanduser(line)))
            self._go_to_gi(gi)
        # If this isn't a mark, treat it as a URL
        else:
            self._go_to_gi(GeminiItem(line))

    @needs_gi
    def do_reload(self, *args):
        """Reload the current URL."""
        self._go_to_gi(self.gi, check_cache=False)

    @needs_gi
    def do_up(self, *args):
        """Go up one directory in the path."""
        self._go_to_gi(self.gi.up())

    @needs_gi
    def do_root(self, *args):
        """Go to root selector of the server hosting current item."""
        self._go_to_gi(self.gi.root())

    @needs_gi
    def do_user(self, *args):
        """If the current URL has a leading ~user/ component, go to its root."""
        try:
            self._go_to_gi(self.gi.user())
        except ValueError:
            print("The current URL does not appear to start with a tilde dir.")

    def do_back(self, *args):
        """Go back to the previous gemini item."""
        if not self.history or self.hist_index == 0:
            print("You are already at the end of your history.")
            return
        self.hist_index -= 1
        gi = self.history[self.hist_index]
        self._go_to_gi(gi, update_hist=False)

    def do_forward(self, *args):
        """Go forward to the next gemini item."""
        if not self.history or self.hist_index == len(self.history) - 1:
            print("You are already at the end of your history.")
            return
        self.hist_index += 1
        gi = self.history[self.hist_index]
        self._go_to_gi(gi, update_hist=False)

    def do_next(self, *args):
        """Go to next item after current in index."""
        return self.onecmd(str(self.index_index+1))

    def do_previous(self, *args):
        """Go to previous item before current in index."""
        self.lookup = self.index
        return self.onecmd(str(self.index_index-1))

    def do_gus(self, line):
        """Submit a search query to the Gemini search engine."""
        ui_out.warning("[WARNING] The `gus` command is deprecated!  Use `search` instead.")
        self.do_search(line)

    def do_search(self, line):
        """Submit a search query a configured Gemini search engine."""
        gi = GeminiItem(self.options["search_url"])
        self._go_to_gi(gi.query(line))

    def do_tour(self, line):
        """Add index items as waypoints on a tour, which is basically a FIFO
queue of gemini items.

Items can be added with `tour 1 2 3 4` or ranges like `tour 1-4`.
All items in current menu can be added with `tour *`.
Current tour can be listed with `tour ls` and scrubbed with `tour clear`."""
        line = line.strip()
        if not line:
            # Fly to next waypoint on tour
            if not self.waypoints:
                print("End of tour.")
            else:
                gi = self.waypoints.pop(0)
                self._go_to_gi(gi)
        elif line == "ls":
            old_lookup = self.lookup
            self.lookup = self.waypoints
            self._show_lookup()
            self.lookup = old_lookup
        elif line == "clear":
            self.waypoints = []
        elif line == "*":
            self.waypoints.extend(self.lookup)
        elif util.looks_like_url(line):
            self.waypoints.append(GeminiItem(line))
        else:
            for index in line.split():
                try:
                    pair = index.split('-')
                    if len(pair) == 1:
                        # Just a single index
                        n = int(index)
                        gi = self.lookup[n-1]
                        self.waypoints.append(gi)
                    elif len(pair) == 2:
                        # Two endpoints for a range of indices
                        if int(pair[0]) < int(pair[1]):
                            for n in range(int(pair[0]), int(pair[1]) + 1):
                                gi = self.lookup[n-1]
                                self.waypoints.append(gi)
                        else:
                            for n in range(int(pair[0]), int(pair[1]) - 1, -1):
                                gi = self.lookup[n-1]
                                self.waypoints.append(gi)

                    else:
                        # Syntax error
                        print("Invalid use of range syntax %s, skipping" % index)
                except ValueError:
                    print("Non-numeric index %s, skipping." % index)
                except IndexError:
                    print("Invalid index %d, skipping." % n)

    @needs_gi
    def do_mark(self, line):
        """Mark the current item with a single letter.  This letter can then
be passed to the 'go' command to return to the current item later.
Think of it like marks in vi: 'mark a'='ma' and 'go a'=''a'."""
        line = line.strip()
        if not line:
            for mark, gi in self.marks.items():
                print("[%s] %s (%s)" % (mark, gi.name, gi.url))
        elif line.isalpha() and len(line) == 1:
            self.marks[line] = self.gi
        else:
            print("Invalid mark, must be one letter")

    ### Stuff that modifies the lookup table
    def do_ls(self, line):
        """List contents of current index.
Use 'ls -l' to see URLs."""
        self.lookup = self.index
        self._show_lookup(url = "-l" in line)
        self.page_index = 0

    def do_history(self, *args):
        """Display history."""
        self.lookup = self.history
        self._show_lookup(url=True)
        self.page_index = 0

    def do_filter(self, searchterm):
        """Filter index on names (case insensitive)."""
        results = [
            gi for gi in self.lookup if searchterm.lower() in gi.name.lower()]
        if results:
            self.lookup = results
            self._show_lookup()
            self.page_index = 0
        else:
            print("No results found.")

    def emptyline(self):
        """Page through index ten lines at a time."""
        i = self.page_index
        if i > len(self.lookup):
            return
        self._show_lookup(offset=i, end=i+10)
        self.page_index += 10

    ### Stuff that does something to most recently viewed item
    @needs_gi
    def do_cat(self, *args):
        """Run most recently visited item through `cat` command."""
        subprocess.call(shlex.split("cat %s" % self.active_rendered_file))

    @needs_gi
    def do_less(self, *args):
        """Run most recently visited item through `less` command."""
        cmd_str = self._get_handler_cmd(self.mime)
        cmd_str = cmd_str % self.active_rendered_file
        subprocess.call("%s | less -R" % cmd_str, shell=True)

    @needs_gi
    def do_fold(self, *args):
        """Run most recently visited item through `fold` command."""
        cmd_str = self._get_handler_cmd(self.mime)
        cmd_str = cmd_str % self.active_rendered_file
        subprocess.call("%s | fold -w 70 -s" % cmd_str, shell=True)

    @restricted
    @needs_gi
    def do_shell(self, line):
        """`cat` most recently visited item through a shell pipeline."""
        subprocess.call(("cat %s |" % self.active_rendered_file) + line, shell=True)

    @restricted
    @needs_gi
    def do_save(self, line):
        """Save an item to the filesystem.
`save n filename` saves menu item n to the specified filename.
`save filename` saves the last viewed item to the specified filename.
`save n` saves menu item n to an automagic filename."""
        args = line.strip().split()

        # First things first, figure out what our arguments are
        if len(args) == 0:
            # No arguments given at all
            # Save current item, if there is one, to a file whose name is
            # inferred from the gemini path
            if not self.gi:
                print("You need to visit an item first!")
                return
            else:
                index = None
                filename = None
        elif len(args) == 1:
            # One argument given
            # If it's numeric, treat it as an index, and infer the filename
            try:
                index = int(args[0])
                filename = None
            # If it's not numeric, treat it as a filename and
            # save the current item
            except ValueError:
                index = None
                filename = os.path.expanduser(args[0])
        elif len(args) == 2:
            # Two arguments given
            # Treat first as an index and second as filename
            index, filename = args
            try:
                index = int(index)
            except ValueError:
                print("First argument is not a valid item index!")
                return
            filename = os.path.expanduser(filename)
        else:
            print("You must provide an index, a filename, or both.")
            return

        # Determine GI to save
        if index:
            try:
                gi = self.lookup[index-1]
                saving_current = False
            except IndexError:
                print ("Index too high!")
                return
        else:
            gi = self.gi
            saving_current = True

        # Derive a filename if one hasn't been set
        if not filename:
            filename = gi.derive_filename(self.mime if saving_current else None)
        filename = util.handle_filename_collisions(filename)
        if not filename:
            return

        # Actually do the save operation
        if saving_current:
            src = gi.path if gi.scheme == "file" else self.active_raw_file
            shutil.copyfile(src, filename)
        else:
            ## Download an item that's not the current one
            self._fetch_over_network(gi, filename)

        print("Saved to %s" % filename)

    @needs_gi
    def do_url(self, *args):
        """Print URL of most recently visited item."""
        print(self.gi.url)

    ### Bookmarking stuff

    @restricted
    @needs_gi
    def do_add(self, line):
        """Add the current URL to the bookmarks menu.
Optionally, specify the new name for the bookmark."""
        with open(os.path.join(self.config_dir, "bookmarks.gmi"), "a") as fp:
            fp.write(self.gi.to_map_line(line))

    def do_bookmarks(self, line):
        """Show or access the bookmarks menu.
'bookmarks' shows all bookmarks.
'bookmarks n' navigates immediately to item n in the bookmark menu.
Bookmarks are stored using the 'add' command."""
        if not os.path.exists(self.bm_file):
            print("You need to 'add' some bookmarks, first!")
            return
        args = line.strip()
        if len(args.split()) > 1 or (args and not args.isnumeric()):
            print("bookmarks command takes a single integer argument!")
            return
        gi = GeminiItem("file://" + os.path.abspath(self.bm_file))
        if args:
            # Semi-sneaky
            # Parses the bookmark file and modifies self.index so that
            # self.default(n) works, but avoids invoking a handler so the
            # full bookmark list is never seen.
            self.active_raw_file = gi.path
            self._handle_gemtext(gi)
            self.default(line)
        else:
            self._go_to_gi(gi, update_hist=False)

    ### Flight recorder
    def do_blackbox(self, *args):
        """Display contents of flight recorder, showing statistics for the
current gemini browsing session."""
        lines = []
        # Compute flight time
        now = time.time()
        delta = now - self.log["start_time"]
        hours, remainder = divmod(delta, 3600)
        minutes, seconds = divmod(remainder, 60)
        # Count hosts
        ipv4_hosts = len([host for host in self.visited_hosts if host[0] == socket.AF_INET])
        ipv6_hosts = len([host for host in self.visited_hosts if host[0] == socket.AF_INET6])
        # Assemble lines
        lines.append(("Patrol duration", "%02d:%02d:%02d" % (hours, minutes, seconds)))
        lines.append(("Requests sent:", self.log["requests"]))
        lines.append(("   IPv4 requests:", self.log["ipv4_requests"]))
        lines.append(("   IPv6 requests:", self.log["ipv6_requests"]))
        lines.append(("Bytes received:", self.log["bytes_recvd"]))
        lines.append(("   IPv4 bytes:", self.log["ipv4_bytes_recvd"]))
        lines.append(("   IPv6 bytes:", self.log["ipv6_bytes_recvd"]))
        lines.append(("Unique hosts visited:", len(self.visited_hosts)))
        lines.append(("   IPv4 hosts:", ipv4_hosts))
        lines.append(("   IPv6 hosts:", ipv6_hosts))
        lines.append(("DNS failures:", self.log["dns_failures"]))
        lines.append(("Timeouts:", self.log["timeouts"]))
        lines.append(("Refused connections:", self.log["refused_connections"]))
        lines.append(("Reset connections:", self.log["reset_connections"]))
        lines.append(("Cache hits:", self.log["cache_hits"]))
        lines.append(("Redirects followed:", self.log["redirects_followed"]))
        # Print
        ljust = max((len(k) for k,v in lines))
        rjust = max((len(str(v)) for k,v in lines))
        gap = 48 - (ljust + rjust)
        for key, value in lines:
            print(key.ljust(ljust+gap) + str(value).rjust(rjust))

    ### Help
    def do_help(self, arg):
        """ALARM! Recursion detected! ALARM! Prepare to eject!"""
        if arg == "!":
            print("! is an alias for 'shell'")
        elif arg == "?":
            print("? is an alias for 'help'")
        else:
            cmd.Cmd.do_help(self, arg)

    def do_abbrevs(self, *args):
        """Print all AV-98 command abbreviations."""
        header = "Command Abbreviations:"
        self.stdout.write("\n{}\n".format(str(header)))
        if self.ruler:
            self.stdout.write("{}\n".format(str(self.ruler * len(header))))
        for k, v in _ABBREVS.items():
            self.stdout.write("{:<7}  {}\n".format(k, v))
        self.stdout.write("\n")

    def do_version(self, line):
        """Display version information."""
        print("AV-98 " + __version__)

    ### The end!
    def do_quit(self, *args):
        """Exit AV-98."""
        # Close TOFU DB
        self.tofu_store.close()
        # Clean up after ourself
        os.unlink(self.raw_file_buffer)
        os.unlink(self.rendered_file_buffer)
        self.client_cert_manager.cleanup()
        # Apply permanent redirects to bookmarks
        self._maintain_bookmarks()
        # Exit command loop
        self._stop = True

    do_exit = do_quit
