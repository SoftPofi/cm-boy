#!/usr/bin/env python3

from unittest import TestCase

from cm_boy.CmFilter import CmFilter
from tests.test_data.TestDataProvider import TestDataProvider


class test_CmFilter(TestCase):

    def setUp(self):
        test_data = TestDataProvider()
        self.uut = CmFilter(config=test_data.provide_config())
        self.test_card = test_data.provide_example_card_id_27()
        self.listing = test_data.provide_listing_id_27()
        self.expected_result = test_data.provide_filtered_listing_id_27()

    def test_prefilter(self):
        self.uut.prefilter(self.listing, self.test_card)
        self.maxDiff = None  # to see diff if fails
        self.assertDictEqual(self.listing, self.expected_result)
