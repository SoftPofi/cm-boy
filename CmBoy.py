#!/usr/bin/env python38

__author__ = ["Eszter Iklódi", "Stephan Laschet"]

import json

from CmInterface import CmInterface


class CmBot:

    def __init__(self):
        with open(".data/config.json", "r") as json_config:
            self.config = json.load(json_config)
        self.cm_interface = CmInterface(self.config.get("cm_access"))


if __name__ == "__main__":
    pass
