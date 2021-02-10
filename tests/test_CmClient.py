import os
from unittest import TestCase

from cm_boy.CmClient import CmClient
from tests.test_data.TestDataProvider import TestDataProvider


class TestCmClient(TestCase):

    def setUp(self):
        test_data = TestDataProvider()
        self.uut = CmClient(test_data.provide_config())
        self.product_id = 27

    def test_get_account_articles(self):
        resp, _, _ = self.uut.get_account_articles(os.environ["cm_user_name"])
        self.assertTrue(resp)

    def test_get_account_stock(self):
        resp, _, _ = self.uut.get_account_stock()
        self.assertTrue(resp)

    def test_get_account_data(self):
        resp, _, _ = self.uut.get_account_data()
        self.assertTrue(resp)

    def test_get_card_info(self):
        resp, _, _ = self.uut.get_card_info(self.product_id)
        self.assertTrue(resp)

    def test_get_card_listing(self):
        resp, _, _ = self.uut.get_card_listing(self.product_id)
        self.assertTrue(resp)

