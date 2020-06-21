#!/usr/bin/env python3
import json

from CmFilter import CmFilter
from unittest import TestCase

from tests.test_data.TestDataProvider import TestDataProvider


class test_CmFilter(TestCase):

    def setUp(self):
        test_data = TestDataProvider()
        self.uut = CmFilter(config=test_data.provide_config())
        with open("./test_data/listing_product_id_27_entries_20.json", "r") as json_test_listing:
            self.listing = json.load(json_test_listing)

        with open("./test_data/example_card_product_id_27.json", "r") as json_test_card:
            self.test_card = json.load(json_test_card)

        with open("test_data/listing_product_id_27_filtered_entries_20.json", "r") as json_expected_result:
            self.expected_result = json.load(json_expected_result)

    def test_prefilter(self):
        self.uut.prefilter(self.listing, self.test_card)
        self.maxDiff =None
        self.assertDictEqual(self.listing, self.expected_result)