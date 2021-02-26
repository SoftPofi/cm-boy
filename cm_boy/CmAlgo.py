#!/usr/bin/env python3
from cm_boy.CmBark import CmBark


class CmAlgo:

    def __init__(self, config, args):
        if config is not None:
            self.config = config
        else:
            raise ValueError("No config given")

        self.cm_bark = CmBark(args.quiet, args.outFile)
        self.list_of_cards_with_changed_prices = []
        self.args = args

    def adjust_price(self, card, listing, sell_count, username):
        if not self.is_position_in_range(card, listing, sell_count, username):
            old_card_price = card["price"]
            if self.match_price_of_target_offer(card, listing):
                self.list_of_cards_with_changed_prices.append({"card": card, "old_price": old_card_price})

    def is_position_in_range(self, card, listings, sell_count, username):
        if self.args.forcePriceSet:
            return False  # Pretend Card is not in acceptable range to force set it
        my_position = self._get_position_in_list(card, listings, sell_count, username)
        if self._get_min_pos_of_card(card) <= my_position <= self._get_max_pos_of_card(card):
            return True
        else:
            return False

    def is_price_of_card_already_min(self, card):
        if card["price"] <= self._get_min_price_for_card(card):
            return True
        else:
            return False

    def match_price_of_target_offer(self, card, listing):
        within_bound, target_position = self._verify_listing_boundaries(card, listing, self._get_target_pos_for_card(card))
        if not within_bound:
            return False
        if listing["article"][target_position]["price"] <= self._get_min_price_for_card(card):
            if self.is_price_of_card_already_min(card):
                return False
            card["price"] = self._get_min_price_for_card(card)
            return True
        else:
            if card["price"] == listing["article"][target_position]["price"]:
                return False
            else:
                card["price"] = listing["article"][target_position]["price"]
                return True

    def _get_min_pos_of_card(self, card):
        position_characteristic = "position"
        if card["isFoil"]:
            position_characteristic = "position_foil"
        return self.config["algo_parameter"][card["product"]["rarity"]][position_characteristic]["min"]

    def _get_max_pos_of_card(self, card):
        position_characteristic = "position"
        if card["isFoil"]:
            position_characteristic = "position_foil"
        return self.config["algo_parameter"][card["product"]["rarity"]][position_characteristic]["max"]

    def _get_target_pos_for_card(self, card):
        position_characteristic = "position"
        if card["isFoil"]:
            position_characteristic = "position_foil"
        return self.config["algo_parameter"][card["product"]["rarity"]][position_characteristic]["target"]

    def _get_position_in_list(self, card, listings, sell_count, username):
        my_position = 0
        for listed_card in listings["article"]:
            my_position = my_position + 1
            if self._is_entry_my_own(listed_card, username):
                return my_position
            if self._found_entry_based_on_price_and_sellcount(card, listed_card, sell_count):
                return my_position
            else:
                continue
        return -1  # position higher than length of listing

    def _is_entry_my_own(self, listed_card, username):
        return listed_card["seller"]["username"] == username

    def _found_entry_based_on_price_and_sellcount(self, card, listed_card, sell_count):
        if listed_card["price"] < card["price"]:
            return False
        elif listed_card["price"] == card["price"]:
            if listed_card["seller"]["sellCount"] <= sell_count:
                return True
            else:  # listed_card["seller"]["sellCount"] > sell_count
                return False
        else:  # listed_card["price"] > card["price"]
            return True

    def _get_min_price_for_card(self, card):
        min_price_parameter = self._card_type_parameter(card)
        return self.config["algo_parameter"][card["product"]["rarity"]]["min_price"][min_price_parameter]

    def _card_type_parameter(self, card):
        min_price_parameter = "normal"
        if card["isFoil"]:
            min_price_parameter = "foil"
        elif card["isPlayset"]:
            min_price_parameter = "playset"
        return min_price_parameter

    def _verify_listing_boundaries(self, card, listing, target_position):
        if len(listing["article"]) == 0:
            self.cm_bark.print_error("E: Zero Listings for card {}, skipp adjustment. Maybe increase requested listings, or unique position!".format(card["product"]["enName"]))
            return False, target_position
        if target_position > len(listing["article"]):
            self.cm_bark.print_error("W: Not enough Listings ({}) for card {}, will work with limited data. Maybe increase requested listings, or unique position!".format(len(listing["article"]), card["product"]["enName"]))
            target_position = len(listing["article"])
        return True, target_position - 1  # -1 to make position to list index

    def _parameter_for_card(self, card):
        ret_dict = {}
        ret_dict.update(
            {"idLanguage": card["language"]["idLanguage"],
             "minUserScore": 1,
             "minCondition": card["condition"],
             "isFoil": "true" if card["isFoil"] else "false",
             "isSigned": "true" if card["isSigned"] else "false",
             "isAltered": "true" if card["isAltered"] else "false"
             }
        )
        return ret_dict
