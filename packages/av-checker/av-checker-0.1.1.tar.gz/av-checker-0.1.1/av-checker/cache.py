_MAX_CACHE_SIZE = 10
_MAX_CACHE_AGE_SECS = 180

import logging
import os
import os.path
import shutil
import tempfile
import time

ui_out = logging.getLogger("av_logger")


class Cache:

    def __init__(self):

        self.cache = {}
        self.cache_timestamps = {}
        self.tempdir = tempfile.TemporaryDirectory()

    def check(self, url):
        if url not in self.cache:
            return False
        now = time.time()
        cached = self.cache_timestamps[url]
        if now - cached > _MAX_CACHE_AGE_SECS:
            ui_out.debug("Expiring old cached copy of resource.")
            self._remove(url)
            return False
        ui_out.debug("Found cached copy of resource.")
        return True

    def _remove(self, url):
        self.cache_timestamps.pop(url)
        mime, filename = self.cache.pop(url)
        os.unlink(filename)
        self.validatecache()

    def add(self, url, mime, filename):
        # Copy client's buffer file to new cache file
        tmpf = tempfile.NamedTemporaryFile(dir=self.tempdir.name, delete=False)
        tmpf.close()
        shutil.copyfile(filename, tmpf.name)
        # Remember details
        self.cache_timestamps[url] = time.time()
        self.cache[url] = (mime, tmpf.name)
        if len(self.cache) > _MAX_CACHE_SIZE:
            self._trim()
        self.validatecache()

    def _trim(self):
        # Order cache entries by age
        lru = [(t, u) for (u, t) in self.cache_timestamps.items()]
        lru.sort()
        # Drop the oldest entry no matter what
        _, url = lru[0]
        ui_out.debug("Dropping cached copy of {} from full cache.".format(url))
        self._remove(url)
        # Drop other entries if they are older than the limit
        now = time.time()
        for cached, url in lru[1:]:
            if now - cached > _MAX_CACHE_AGE_SECS:
                ui_out.debug("Dropping cached copy of {} from full cache.".format(url))
                self._remove(url)
            else:
                break
        self.validatecache()

    def get(self, url):
        return self.cache[url]

    def validatecache(self):
        assert self.cache.keys() == self.cache_timestamps.keys()
        for _, filename in self.cache.values():
            assert os.path.isfile(filename)
