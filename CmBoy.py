#!/usr/bin/env python3

import json
import argparse

from cm_boy.CmAlgo import CmAlgo
from cm_boy.CmBark import CmBark
from cm_boy.CmClient import CmClient
from cm_boy.CmFilter import CmFilter
from cm_boy.CmSession import CmSession


def main():
    """
    get a good boy that first gets your account data, gets your stock processes each card and uploads the cards that have a new price.
    """
    good_cm_boy = CmBoy()
    good_cm_boy.come()
    good_cm_boy.fetch()
    good_cm_boy.chew()
    good_cm_boy.put()


class CmBoy:

    def __init__(self):
        with open("data/config.json", "r") as json_config:
            self.config = json.load(json_config)
        self.parser = argparse.ArgumentParser(description='This Boy handles all the cardmarket stuff, good boy!')
        self._setup_parser()

        self.cm_client = CmClient(self.config)
        self.cm_filter = CmFilter(self.config)
        self.cm_session = CmSession(self.config["urls"]["base_url"])
        self.cm_algo = CmAlgo(self.config, self.args)
        self.cm_bark = CmBark(self.args.quiet, self.args.outFile)

        self.card_inventory = {}

    def come(self):
        success, reason, account_data = self.cm_client.get_account_data()
        if success:
            self.username = account_data["account"]["username"]
            self.sell_count = account_data["account"]["sellCount"]
            self.cm_bark.come(self.username )
            self.config["listing_static_filter"]["seller_country"] = account_data["account"]["country"]
        else:
            raise ValueError("Could not get account data! Reason: {}".format(reason))

    def fetch(self):
        self.cm_bark.get_stock()
        success, reason, self.card_inventory = self.cm_client.get_account_stock()
        if success:
            self.cm_filter.stock_filter(self.card_inventory)
            self.cm_bark.stock_statistics(self.card_inventory)
        else:
            raise ValueError("Could not get card inventory! Reason: {}".format(reason))

    def chew(self):
        self.cm_bark.start_chew()
        for card in self.card_inventory["article"]:
            self.cm_bark.update_current_card(card)
            parameter = self.cm_algo._parameter_for_card(card)
            success, reason, listing = self.cm_client.get_card_listing(card["idProduct"], user_params=parameter)
            if success:
                self.cm_filter.prefilter(listing, card)
                self.cm_algo.adjust_price(card, listing, self.sell_count, self.username)
            else:
                self.cm_bark.print_error("Could not get listings for card {}! Reason: {}".format(card["product"]["enName"], reason))
        self.cm_bark.end_chew_message()
        self.cm_bark.end_chew()

    def put(self):
        self.cm_bark.put_start_message(self.args.dryrun, self.cm_algo.list_of_cards_with_changed_prices)
        if not self.args.dryrun:
            for card in self.cm_algo.list_of_cards_with_changed_prices:
                success, reason, listing = self.cm_client.put_card_price(card["card"])
                if not success:
                    self.cm_bark.print_error("Could not upload card {}! Reason: {}".format(card["card"]["product"]["enName"], reason))
        for card in self.cm_algo.list_of_cards_with_changed_prices:
            self.cm_bark.price_update_statistic(card)

    def _setup_parser(self):
        self.parser.add_argument("-d", "--dryrun", action="store_true", help="Do NOT upload the cards with adjusted prices.")
        self.parser.add_argument("-q", "--quiet", action="store_true", help="Disable all output to the command line.")
        self.parser.add_argument("-f", "--forcePriceSet", action="store_true", help="Regardless of the current position, update the prices.")
        self.parser.add_argument("-o", "--outFile", nargs='?', const='', help="Absolute path to folder where log files are stored. If empty, log is stored in CmBoy's folder.")
        self.args = self.parser.parse_args()


if __name__ == "__main__":
    main()
