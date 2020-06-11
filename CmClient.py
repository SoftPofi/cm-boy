#!/usr/bin/env python3


import json
import logging

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
            with open("./data/config.json", "r") as json_config:
                self.config = json.load(json_config)
        with open("./data/confidential_config.json", "r") as json_confidential_config:
            self.confidential_config = json.load(json_confidential_config)
        self.cm_session = CmSession(self.config["urls"]["base_url"], self.confidential_config)

    def get_account_articles(self):
        url_ext = "/users/{}/articles".format(self.confidential_config["account"]["user_name"])
        self.cm_session.update_client_session_url(url_ext=url_ext)
        return self.cm_session.get_data(url_ext=url_ext)

    def get_account_stock(self):
        url_ext = "/stock"
        self.cm_session.update_client_session_url(url_ext=url_ext)
        return self.cm_session.get_data(url_ext=url_ext)

    def get_account_data(self):
        url_ext = "/account"
        self.cm_session.update_client_session_url(url_ext=url_ext)
        return self.cm_session.get_data(url_ext=url_ext)

    def get_card_info(self, product_id):
        url_ext = "/products/{}".format(product_id)
        self.cm_session.update_client_session_url(url_ext=url_ext)
        return self.cm_session.get_data(url_ext=url_ext)


if __name__ == "__main__":
    client = CmClient(None)
    response = client.get_account_stock()
    if response.status_code == 200 or response.status_code == 206:
        json_object = json.loads(response.text)
        json_formatted_str = json.dumps(json_object, indent=3)
        client.logger.debug(json_formatted_str)
    else:
        client.logger.error("Faulty response {}".format(response.status_code))
