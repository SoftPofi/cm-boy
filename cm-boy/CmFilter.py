#!/usr/bin/env python3


class CmFilter:

    def __init__(self, config):
        if config is not None:
            self.config = config
        else:
            raise ValueError("No config given")

    def prefilter(self, card_listings, card):
        offers_to_remove = []
        for offer in card_listings["article"]:
            if self._offer_not_matching_card(offer, card):
                offers_to_remove.append(offer)
        for offer in offers_to_remove:
            card_listings["article"].remove(offer)

    def _offer_not_matching_card(self, offer, card):
        ret_val = False
        ret_val = self._country_not_matching(offer, ret_val)
        if not ret_val:
            ret_val = self._playset_not_matching(card, offer, ret_val)
        return ret_val

    def _playset_not_matching(self, card, offer, ret_val):
        if offer["isPlayset"] != card["isPlayset"]:
            ret_val = True
        return ret_val

    def _country_not_matching(self, offer, ret_val):
        offer_country = offer["seller"]["address"]["country"]
        if offer_country != self.config["listing_static_filter"]["seller_country"]:
            ret_val = True
        return ret_val

    def stock_filter(self, card_inventory):
        offers_to_remove = []
        for item in card_inventory["article"]:
            if "|#00" in item["comments"]:
                offers_to_remove.append(item)
        for offer in offers_to_remove:
            card_inventory["article"].remove(offer)
