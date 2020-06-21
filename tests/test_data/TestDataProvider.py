#!/usr/bin/env python3
import json


class TestDataProvider:

    def __init__(self):
        pass

    def provide_config(self):
        with open("../data/config.json", "r") as json_config:
            config = json.load(json_config)
        return config


if __name__ == "__main__":
    pass