import os.path


def looks_like_url(word):
    return "." in word and word.startswith("gemini://")


def handle_filename_collisions(filename):
    while os.path.exists(filename):
        print("File %s already exists!" % filename)
        filename = input("Choose a new one, or leave blank to abort: ")
    return filename


def ask_yes_no(prompt, default=None):
    print(prompt)
    if default == True:
        prompt = "(Y)/N: "
    elif default == False:
        prompt = "Y/(N): "
    else:
        prompt = "Y/N: "
    while True:
        resp = input(prompt)
        if not resp.strip() and default != None:
            return default
        elif resp.strip().lower() in ("y", "yes"):
            return True
        elif resp.strip().lower() in ("n", "no"):
            return False


def fix_ipv6_url(url):
    if not url.count(":") > 2:  # Best way to detect them?
        return url
    # If there's a pair of []s in there, it's probably fine as is.
    if "[" in url and "]" in url:
        return url
    # Easiest case is a raw address, no schema, no path.
    # Just wrap it in square brackets and whack a slash on the end
    if "/" not in url:
        return "[" + url + "]/"
    # Now the trickier cases...
    if "://" in url:
        schema, schemaless = url.split("://")
    else:
        schema, schemaless = None, url
    if "/" in schemaless:
        netloc, rest = schemaless.split("/", 1)
        schemaless = "[" + netloc + "]" + "/" + rest
    if schema:
        return schema + "://" + schemaless
    return schemaless
