#!/usr/bin/env python3
import json
import os


class TestDataProvider:

    def __init__(self):
        pass

    def provide_config(self):
        with open("../data/config.json", "r") as json_config:
            config = json.load(json_config)
        return config

    def provide_confidential_config(self):
        with open("../data/confidential_config.json", "r") as json_config:
            config = json.load(json_config)
        return config

    def provide_listing_id_27(self):
        with open("test_data/listing_product_id_27_entries_20.json", "r") as json_listing:
            listing = json.load(json_listing)
        return listing

    def provide_filtered_listing_id_27(self):
        with open("test_data/listing_product_id_27_filtered_entries_20.json", "r") as json_filtered_listing:
            filtered_listing = json.load(json_filtered_listing)
        return filtered_listing

    def provide_example_card_id_27(self):
        with open("test_data/example_card_product_id_27.json", "r") as json_example_card:
            example_card = json.load(json_example_card)
        return example_card

    def anonymize_data(self):
        files = os.listdir("./")
        for file in files:
            if file.endswith("json"):
                try:
                    with open(file, "r") as json_file:
                        to_anonymize = json.load(json_file)
                except Exception as exc:
                    continue
                try:
                    for entry in to_anonymize["article"]:
                        try:
                            self._remove_sensitive_entries(entry)
                        except Exception as exc:
                            continue
                except Exception as exc:
                    continue

                with open(file, "w") as anonymized_file:
                    json.dump(to_anonymize, anonymized_file, indent=1)

    def _remove_sensitive_entries(self, entry):
        entry["seller"]["idUser"] = 0
        entry["seller"]["username"] = ""
        del entry["seller"]["name"]
        del entry["seller"]["address"]
        del entry["seller"]["phone"]
        del entry["seller"]["email"]
        del entry["seller"]["vat"]


if __name__ == "__main__":
    anonymizer = TestDataProvider().anonymize_data()

