#!/usr/bin/env python3
from copy import deepcopy


class CmFilter:

    def __init__(self, config):
        if config is not None:
            self.config = config
        else:
            raise ValueError("No config given")

    def prefilter(self, card_listings, card):
        filtered_copy = deepcopy(card_listings)
        offers_to_remove = []
        for offer in filtered_copy["article"]:
            if self._offer_not_matching_card(offer, card):
                offers_to_remove.append(offer)
        for offer in offers_to_remove:
            filtered_copy["article"].remove(offer)
        return filtered_copy

    def _offer_not_matching_card(self, offer, card):
        offer_country = offer["seller"]["address"]["country"]
        if offer_country != self.config["listing_static_filter"]["seller_country"]:
            return True
        if offer["isPlayset"] != card["isPlayset"]:
            return True
        return False
