#!/usr/bin/env python38

__author__ = ["Eszter Iklódi", "Stephan Laschet"]

import json


class CmInterface:
    """
    Class that interacts with CM API
    """

    def __init__(self, config_data):
        if config_data is not None:
            self.config = config_data
        with open(".data/confidential_config.json", "r") as json_config:
            self.confidential_config = json.load(json_config)


if __name__ == "__main__":
    pass
