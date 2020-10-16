#!/usr/bin/env python3
from unittest import TestCase

from CmAlgo import CmAlgo
from tests.test_data.TestDataProvider import TestDataProvider


class test_CmAlgo(TestCase):

    def setUp(self):
        self.config = TestDataProvider().provide_config()
        self.confidential_config = TestDataProvider().provide_confidential_config()
        self.test_listing = TestDataProvider().provide_listing_id_27()
        self.test_card = TestDataProvider().provide_example_card_id_27()
        self.uut = CmAlgo(self.config, self.confidential_config)

    def test_card_in_range(self):
        result = self.uut.is_position_in_range(self.test_card, self.test_listing)
        self.assertTrue(result)

    def test_card_already_min(self):
        result = self.uut.is_price_of_card_already_min(self.test_card)
        self.assertFalse(result)

    def test_patch_price_of_target_offer(self):
        result = self.uut.match_price_of_target_offer(self.test_card, self.test_listing)
        self.assertTrue(result)
        self.assertEqual(self.test_card["price"], 0.15)