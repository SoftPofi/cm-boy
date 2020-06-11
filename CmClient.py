#!/usr/bin/env python38


import json
import logging

import requests
from requests_oauthlib import OAuth1Session, OAuth1


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
            with open("./data/config.json", "r") as json_config:
                self.config = json.load(json_config)
        with open("./data/confidential_config.json", "r") as json_confidential_config:
            self.confidential_config = json.load(json_confidential_config)
        realm = "{}/users/{}/articles".format(self.config["urls"]["base_url"],self.confidential_config["account"]["user_name"])
        self.api_client = OAuth1Session(self.confidential_config["cm_access"]["app_token"],
                                        client_secret=self.confidential_config["cm_access"]["app_secret"],
                                        resource_owner_key=self.confidential_config["cm_access"]["access_token"],
                                        resource_owner_secret=self.confidential_config["cm_access"]["access_secret"],
                                        realm=realm
                                        )

    def generate_full_url(self, url, url_ext):
        if url is None:
            if url_ext is None:
                raise ValueError("No URL and no URL Extension given, can't request anything.")
            else:
                url = "{}{}".format(self.config["urls"]["base_url"], url_ext)
        return url

    def update_client_session_url(self, url=None, url_ext=None, ):
        url = self.generate_full_url(url, url_ext)
        self.api_client = OAuth1Session(self.confidential_config["cm_access"]["app_token"],
                                        client_secret=self.confidential_config["cm_access"]["app_secret"],
                                        resource_owner_key=self.confidential_config["cm_access"]["access_token"],
                                        resource_owner_secret=self.confidential_config["cm_access"]["access_secret"],
                                        realm=url
                                        )

    def get_data(self, url=None, url_ext=None, params=None):
        url = self.generate_full_url(url, url_ext)
        return self.api_client.get(url, params=params)

    def get_account_articles(self):
        url_ext = "/users/{}/articles".format(self.confidential_config["account"]["user_name"])
        self.update_client_session_url(url_ext=url_ext)
        return self.get_data(url_ext=url_ext)

    def get_account_stock(self):
        url_ext = "/stock"
        self.update_client_session_url(url_ext=url_ext)
        return self.get_data(url_ext=url_ext)

    def get_account_data(self):
        url_ext = "/account"
        self.update_client_session_url(url_ext=url_ext)
        return self.get_data(url_ext=url_ext)

    def get_card_info(self, product_id):
        url_ext = "/products/{}".format(product_id)
        self.update_client_session_url(url_ext=url_ext)
        return self.get_data(url_ext=url_ext)

    def debug_pretty_print_json(self, response):
        json_object = json.loads(response.text)
        json_formatted_str = json.dumps(json_object, indent=3)
        self.logger.debug(json_formatted_str)

    def _prettify_response(self, response):
        request_ok = response.status_code == 200
        if not request_ok:
            self.logger.error(response.reason)
            return request_ok, {}
        response_data = json.loads(response.text)
        return request_ok, response_data


if __name__ == "__main__":
    client = CmClient(None)
    client.debug_pretty_print_json(client.get_account_stock())
