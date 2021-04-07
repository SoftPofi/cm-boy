import json
import os
import mock
from unittest import TestCase

from cm_boy.CmClient import CmClient
from tests.test_data.TestDataProvider import TestDataProvider


class response_mock:
    def __init__(self):
        self.status_code = 200
        self.reason = "OK"
        self.content = str(json.dumps({"test": "passed"})).encode("utf8")


class TestCmClient(TestCase):

    def setUp(self):
        test_data = TestDataProvider()
        self.uut = CmClient(test_data.provide_config())
        self.product_id = 27

    @mock.patch("cm_boy.CmClient.CmSession.get_data", return_value=response_mock())
    def test_get_account_articles(self, mock_session):
        resp, _, _ = self.uut.get_account_articles(os.environ["cm_user_name"])
        self.assertTrue(resp)

    @mock.patch("cm_boy.CmClient.CmSession.get_data", return_value=response_mock())
    def test_get_account_stock(self, mock_session):
        resp, _, _ = self.uut.get_account_stock()
        self.assertTrue(resp)

    @mock.patch("cm_boy.CmClient.CmSession.get_data", return_value=response_mock())
    def test_get_account_data(self, mock_session):
        resp, _, _ = self.uut.get_account_data()
        self.assertTrue(resp)

    @mock.patch("cm_boy.CmClient.CmSession.get_data", return_value=response_mock())
    def test_get_card_info(self, mock_session):
        resp, _, _ = self.uut.get_card_info(self.product_id)
        self.assertTrue(resp)

    @mock.patch("cm_boy.CmClient.CmSession.get_data", return_value=response_mock())
    def test_get_card_listing(self, mock_session):
        resp, _, _ = self.uut.get_card_listing(self.product_id)
        self.assertTrue(resp)
