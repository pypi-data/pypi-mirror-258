import unittest
from scraper import WebScraper

class TestWebScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = WebScraper()

    def tearDown(self):
        self.scraper.close_browser()


    def test_get_player_aimstat(self):
        account_link = "https://leetify.com/app/profile/76561199506785320"
        aimstat = self.scraper.get_aim_stat(account_link)
        self.assertIsNotNone(aimstat)


    

if __name__ == "__main__":
    unittest.main()
