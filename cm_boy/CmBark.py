#!/usr/bin/env python3
import os
from datetime import datetime


class CmBark:

    def __init__(self, quiet, log_file_path):
        """
        The CM logging class
        """
        self.log_file_path = log_file_path
        self.log_file_name = "{}_log.log".format(str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")))
        if self.log_file_path is not None:
            if log_file_path == "":
                self.log_file_path = "./"
            else:
                if not os.path.isdir(self.log_file_path):
                    raise ValueError("Directory '{}' given is not an existing directory".format(self.log_file_path))
        self.quiet = quiet
        self.card_count = 0
        self.card_total = 0

    def come(self, user_name):
        self._cm_print("Updating the stock for user {}".format(user_name))

    def stock_statistics(self, card_inventory):
        self.card_total = len(card_inventory["article"])
        self._cm_print("Received stock of {} cards".format(self.card_total))

    def start_chew(self):
        self.card_count = 0
        self._cm_print("Start processing cards")

    def end_chew(self):
        self._cm_print("End processing cards")

    def update_current_card(self, card):
        self.card_count += 1
        print_str = "Process Card {:05d}/{:05d}: {}{: <128}".format(self.card_count, self.card_total, card["product"]["enName"], " ")
        self._cm_print(print_str, end="\r", flush=True)

    def price_update_statistic(self, card):
        card_info = "Stats: Rarity {} | Set: {} | Foil {} | Playset {}".format(
            card["card"]["product"]["rarity"],
            card["card"]["product"]["expansion"],
            card["card"]["isFoil"],
            card["card"]["isPlayset"]
        )
        value_color = "\033[32m" if card["card"]["price"] >= card["old_price"] else "\033[31m"
        printout_str = "Card [{}]:{}{:.02f} \033[m | old: {:.02f} new: {:.02f}\n\t\t\t\t{}\n".format(
            card["card"]["product"]["enName"],
            value_color,
            card["card"]["price"] - card["old_price"],
            card["old_price"],
            card["card"]["price"],
            card_info)
        self._cm_print(printout_str)

    def get_stock(self):
        self._cm_print("Fetching stock...")

    def print_error(self, err_str):
        timestamp = datetime.now()
        printout_str = "\n\033[31m{}: {}\033[m".format(timestamp, err_str)
        if not self.quiet:
            print(printout_str)
        if self.log_file_path is not None:
            with open(self.log_file_path + self.log_file_name, "a+") as log_file:
                log_file.write("{}: {}\n".format(timestamp, printout_str.strip()))

    def end_chew_message(self):
        if not self.quiet:
            print("")

    def put_start_message(self, dryrun, list_of_cards_with_changed_prices):
        self._cm_print("Starting upload process for {} cards".format(len(list_of_cards_with_changed_prices)))
        if dryrun:
            self.print_error("Dryrun specified, will not upload anything.")

    def _cm_print(self, printout_str, end="\n", flush=False):
        timestamp = datetime.now()
        if not self.quiet:
            print("{}: {}".format(timestamp, printout_str), end=end, flush=flush)
        if self.log_file_path is not None:
            with open(self.log_file_path + self.log_file_name, "a+") as log_file:
                log_file.write("{}: {}\n".format(timestamp, printout_str.strip()))
