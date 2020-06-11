#!/usr/bin/env python38


import json

from CmClient import CmClient


class CmBoy:

    def __init__(self):
        with open(".data/config.json", "r") as json_config:
            self.config = json.load(json_config)
        self.cm_interface = CmClient(self.config)


if __name__ == "__main__":
    pass
