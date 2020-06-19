#!/usr/bin/env python3


import json
import logging
from dicttoxml import dicttoxml

from CmSession import CmSession


class CmClient:
    """
    Class that interacts with CM API
    """

    def __init__(self, config_data, logger=None):
        if logger is None:
            logging.basicConfig(level=logging.DEBUG)
            self.logger = logging.getLogger('local_client_logger')
        else:
            self.logger = logger
        if config_data is not None:
            self.config = config_data
        else:
            with open("../data/config.json", "r") as json_config:
                self.config = json.load(json_config)
        with open("../data/confidential_config.json", "r") as json_confidential_config:
            self.confidential_config = json.load(json_confidential_config)
        self.cm_session = CmSession(self.config["urls"]["base_url"], self.confidential_config)

    def get_account_articles(self):
        url_ext = "/users/{}/articles".format(self.confidential_config["account"]["user_name"])
        return self.cm_session.get_data(url_ext=url_ext)

    def get_account_stock(self):
        url_ext = "/stock"
        return self.cm_session.get_data(url_ext=url_ext)

    def get_account_data(self):
        url_ext = "/account"
        return self.cm_session.get_data(url_ext=url_ext)

    def get_card_info(self, product_id):
        url_ext = "/products/{}".format(product_id)
        return self.cm_session.get_data(url_ext=url_ext)

    def get_card_listing(self, product_id, user_params=None):
        params = self.config["product_default_params"]
        if user_params is not None:
            params.update(user_params)
        url_ext = "/articles/{}".format(product_id)
        return self.cm_session.get_data(url_ext=url_ext, params=params)

    def put_card_price(self, card):
        if "article" not in card or \
                "idArticle" not in card["article"] or \
                "price" not in card["article"] or \
                "count" not in card["article"]:
            raise ValueError("Dictionary for card malformed or missing entries idArticle, price or count")
        xml_card_description = dicttoxml(card, custom_root='request', attr_type=False)
        return self.cm_session.put_data(url_ext="/stock", body=xml_card_description)
