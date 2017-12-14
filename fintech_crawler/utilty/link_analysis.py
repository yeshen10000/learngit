# encoding: utf-8
from urlparse import urlparse, urljoin, urlunparse
import sys
reload(sys)
sys.setdefaultencoding('utf8')


HTML5_WHITESPACE = ' \t\n\r\x0c'


class LinkExtractor(object):

    def clean_link(self, link_text):
        pass

    def extractor_link(self, response_text, response_encoding):
        pass

    def remove_tags(self, response_text):
        pass

    # def url_join(self, base_url, url):
    #     print url, base_url, urljoin(base_url, url)
    #     url = urljoin(base_url, url)
    #     u = urlparse(url)
    #     return urlunparse((u.scheme, u.netloc, os.path.realpath(u.path), u.params, u.query, u.fragment))

    def url_join(self, base_url, url):
        return urljoin(base_url, url)

    def url_legal(self, url, domains):
        if url and (url.startswith("http") or url.startswith("https")):
            if self.url_is_from_any_domain(url, domains):
                return True
            return False
        else:
            return False

    def url_is_from_any_domain(self, url, domains):
        """
        返回url是否在所给的域名内
        :param url:
        :param domains: 域名 list
        :return: True or False
        """
        host = urlparse(url).netloc.lower()
        if not host:
            return False
        domains = [d.lower() for d in domains]
        return any((host == d) or (host.endswith('.%s' % d)) for d in domains)

    def strip_html5_whitespace(self, text):
        return text.strip(HTML5_WHITESPACE)


if __name__ == "__main__":
    pass

