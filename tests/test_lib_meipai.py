from lib.site_factory import SiteFactory
import unittest

class TestMeipai(unittest.TestCase):
    def setUp(self):
        self.site = SiteFactory("meipai")

    def tearDown(self):
        pass

    def test_get_link(self):
        print self.site.get_link('http://www.meipai.com/media/435782479')

    def test_search_video(self):
        print self.site.search_video('hello', 1, 1)
