import re

from whitenoise.middleware import WhiteNoiseMiddleware

class CustomWhiteNoise(WhiteNoiseMiddleware):
    """
    Serves index pages for directory paths (such as the site root).
    """

    INDEX_NAME = 'index.html'

    def update_files_dictionary(self, *args):
        """Add support for serving index pages for directory paths."""
        super(CustomWhiteNoise, self).update_files_dictionary(*args)
        index_page_suffix = "/" + self.INDEX_NAME
        index_name_length = len(self.INDEX_NAME)
        index_files = {}
        for url, static_file in self.files.items():
            # Add an additional fake filename to serve index pages for '/'.
            if url.endswith(index_page_suffix):
                index_files[url[:-index_name_length]] = static_file
        self.files.update(index_files)

    def find_file(self, url):
        """Add support for serving index pages for directory paths when in DEBUG mode."""
        # In debug mode, find_file() is used to serve files directly from the filesystem
        # instead of using the list in `self.files`, so we append the index filename so
        # that will be served if present.
        if url[-1] == '/':
            url += self.INDEX_NAME
        return super(CustomWhiteNoise, self).find_file(url)
