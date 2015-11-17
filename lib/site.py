class VideoNotFound(Exception):
    pass

class NotImplemented(Exception):
    pass

class Site:
    def __init__(self):
        pass

    def get_link(self, url):
        raise NotImplemented()

