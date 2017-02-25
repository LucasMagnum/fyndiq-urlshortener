import abc


class ShortenerBase:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def generate_short_url(self, url):
        pass

    @abc.abstractmethod
    def get_original_url(self, shortened_url):
        pass
