#!/usr/bin/env python3


import json
from dicttoxml import dicttoxml

from CmSession import CmSession


class CmClient:
    """
    Class that interacts with CM API
    """

    def __init__(self, config_data):
        if config_data is None:
            raise ValueError("No config given!")
        else:
            self.config = config_data
        self.cm_session = CmSession(self.config["urls"]["base_url"])

    def get_account_articles(self, username):
        """
        Get all articles. This is not for getting the cards, but for also getting all the other articles one could sell on cm
        :return:
        """
        url_ext = "/users/{}/articles".format(username)
        response = self.cm_session.get_data(url_ext=url_ext)
        return self._response_ok(response), response.reason, self._response_content_to_json(response)

    def get_account_stock(self):
        """
        Get all the cards this account has to offer.
        :return:
        """
        url_ext = "/stock"
        response = self.cm_session.get_data(url_ext=url_ext)
        return self._response_ok(response), response.reason, self._response_content_to_json(response)

    def get_account_data(self):
        url_ext = "/account"
        response = self.cm_session.get_data(url_ext=url_ext)
        return self._response_ok(response), response.reason, self._response_content_to_json(response)

    def get_card_info(self, product_id):
        """
        Get the general information about this card such as rarity and edition.
        :param product_id:
        :return:
        """
        url_ext = "/products/{}".format(product_id)
        response = self.cm_session.get_data(url_ext=url_ext)
        return self._response_ok(response), response.reason, self._response_content_to_json(response)

    def get_card_listing(self, product_id, user_params=None):
        """
        Get all offers for the specified card.
        :param product_id:
        :param user_params:
        :return:
        """
        params = self.config["product_default_params"]
        if user_params is not None:
            params.update(user_params)
        url_ext = "/articles/{}".format(product_id)
        response = self.cm_session.get_data(url_ext=url_ext, params=params)
        return self._response_ok(response), response.reason, self._response_content_to_json(response)

    def put_card_price(self, card):
        if "idArticle" not in card or \
                "count" not in card or \
                "price" not in card:
            raise ValueError("Dictionary for card malformed or missing entries idArticle, price or count")
        upload_card = {"article": {"idArticle": card["idArticle"],
                                   "price": card["price"],
                                   "count": card["count"]}}
        xml_card_description = dicttoxml(upload_card, custom_root='request', attr_type=False)
        response = self.cm_session.put_data(url_ext="/stock", body=xml_card_description)
        return self._upload_ok(response), response.reason, self._response_content_to_json(response)

    def _response_ok(self, resp):
        return resp.status_code in [200, 206]

    def _response_content_to_json(self, resp):
        if self._response_ok(resp):
            resp.content.decode("utf8")
            return json.loads(resp.content)
        else:
            return {}

    def _upload_ok(self, response):
        if self._response_ok(response):
            return len(json.loads(response.text)["updatedArticles"]) > 0
        else:
            return False
