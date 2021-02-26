#!/usr/bin/env python3
import argparse
import os

from unittest import TestCase

from cm_boy.CmAlgo import CmAlgo
from tests.test_data.TestDataProvider import TestDataProvider


class test_CmAlgo(TestCase):

    def setUp(self):
        self.config = TestDataProvider().provide_config()
        self.test_listing = TestDataProvider().provide_listing_id_27()
        self.test_card = TestDataProvider().provide_example_card_id_27()
        self.parser = argparse.ArgumentParser(description='This Boy handles all the cardmarket stuff, good boy!')
        self.setup_parser()
        args = self.parser.parse_args(["-d", "-q"])
        args.outFile = None
        self.uut = CmAlgo(self.config, args)

    def test_card_in_range(self):
        result = self.uut.is_position_in_range(self.test_card, self.test_listing, 50, os.environ["cm_user_name"])
        self.assertTrue(result)

    def test_card_already_min(self):
        result = self.uut.is_price_of_card_already_min(self.test_card)
        self.assertFalse(result)

    def test_patch_price_of_target_offer(self):
        result = self.uut.match_price_of_target_offer(self.test_card, self.test_listing)
        self.assertTrue(result)
        self.assertEqual(self.test_card["price"], 0.04)

    def setup_parser(self):
        self.parser.add_argument("-d", "--dryrun", action="store_true", help="Do NOT upload the cards with adjusted prices.")
        self.parser.add_argument("-q", "--quiet", action="store_true", help="Disable all output to the command line.")
        self.parser.add_argument("-f", "--forcePriceSet", action="store_true", help="Regardless of the current position, update the prices.")
        self.parser.add_argument("-o", "--outFile", action="store_true", help="Regardless of the current position, update the prices.")
