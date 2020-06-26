from unittest import TestCase

from CmClient import CmClient


class TestCmClient(TestCase):

    def setUp(self):
        self.uut = CmClient(None)
        self.product_id = 27

    def test_get_account_articles(self):
        resp = self.uut.get_account_articles()
        self.assert_response_ok(resp)

    def test_get_account_stock(self):
        resp = self.uut.get_account_stock()
        self.assert_response_ok(resp)

    def test_get_account_data(self):
        resp = self.uut.get_account_data()
        self.assert_response_ok(resp)

    def test_get_card_info(self):
        resp = self.uut.get_card_info(self.product_id)
        self.assert_response_ok(resp)

    def test_get_card_listing(self):
        resp = self.uut.get_card_listing(self.product_id)
        self.assert_response_ok(resp)

    def test_put_card_price(self):
        example_card = {
            "article":
                {
                    "idArticle": "593000831",
                    "count": 1,
                    "price": 0.44,
                }
        }
        resp = self.uut.put_card_price(example_card)
        self.assert_response_ok(resp)

    def assert_response_ok(self, resp):
        self.assertIn(resp.status_code, [200, 206])
