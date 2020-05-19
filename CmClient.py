#!/usr/bin/env python38

__author__ = ["Eszter Iklódi", "Stephan Laschet"]

import json
import requests
from requests_oauthlib import OAuth1Session, OAuth1


class CmClient:
    """
    Class that interacts with CM API
    """

    def __init__(self, config_data):
        if config_data is not None:
            self.config = config_data
        else:
            with open("./data/config.json", "r") as json_config:
                self.config = json.load(json_config)
        with open("./data/confidential_config.json", "r") as json_confidential_config:
            self.confidential_config = json.load(json_confidential_config)
        realm_url = "{}{}{}{}".format(self.config["urls"]["base_url"], "/users/", self.confidential_config["account"]["user_name"], "/articles")
        self.api_client = OAuth1Session(self.confidential_config["cm_access"]["app_token"],
                                        client_secret=self.confidential_config["cm_access"]["app_secret"],
                                        resource_owner_key=self.confidential_config["cm_access"]["access_token"],
                                        resource_owner_secret=self.confidential_config["cm_access"]["access_secret"],
                                        realm=realm_url
                                        )
        pass

    def get_data(self, url_ext=None, url=None, param=None):
        if url_ext is not None:
            url = "{}{}".format(self.config["urls"]["base_url_no_json"],url_ext)
        return self.api_client.get(url)

    def get_url(self, url):
        return self.api_client.get(url, auth=OAuth1)


if __name__ == "__main__":
    client = CmClient(None)
    # stock = client.get_data("/stock")
    stock = client.get_url("https://api.cardmarket.com/ws/v2.0/stock")
    pass
