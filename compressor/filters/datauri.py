import os, re, base64
from compressor.filters import FilterBase, FilterError
from compressor.conf import settings


class DataUriFilter(FilterBase):
    def input(self, filename=None, **kwargs):
        if not filename or not filename.startswith(settings.MEDIA_ROOT):
            return self.content
        output = self.content
        for url_pattern in self.url_patterns:
            output = url_pattern.sub(self.data_uri_converter, output)
        return output

    def get_file_path(self, url):
        return os.path.join(settings.MEDIA_ROOT, url[len(settings.MEDIA_URL):])

    def data_uri_converter(self, matchobj):
        url = matchobj.group(1).strip(' \'"')
        if not url.startswith('data:'):
            path = self.get_file_path(url)
            if os.stat(path).st_size <= settings.COMPRESS_DATA_URI_MIN_SIZE:
                data = base64.b64encode(open(path, 'rb').read())
                return 'url("data:image/png;base64,%s")' % data
        return 'url("%s")' % url


class DataUriCssFilter(DataUriFilter):
    url_patterns = (
        re.compile(r'url\(([^\)]+)\)'),
    )
