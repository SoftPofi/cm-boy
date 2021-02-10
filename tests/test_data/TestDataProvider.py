#!/usr/bin/env python3
import json
import os


class TestDataProvider:

    def __init__(self):
        pass

    def provide_config(self):
        dirname = os.path.dirname(__file__)
        filepath = os.path.join(dirname, "../../data/config.json")
        with open(filepath, "r") as json_config:
            config = json.load(json_config)
        return config

    def provide_listing_id_27(self):
        dirname = os.path.dirname(__file__)
        filepath = os.path.join(dirname, "listing_product_id_27_entries_20.json")
        with open(filepath, "r") as json_listing:
            listing = json.load(json_listing)
        return listing

    def provide_filtered_listing_id_27(self):
        dirname = os.path.dirname(__file__)
        filepath = os.path.join(dirname, "listing_product_id_27_filtered_entries_20.json")
        with open(filepath, "r") as json_filtered_listing:
            filtered_listing = json.load(json_filtered_listing)
        return filtered_listing

    def provide_example_card_id_27(self):
        dirname = os.path.dirname(__file__)
        filepath = os.path.join(dirname, "example_card_product_id_27.json")
        with open(filepath, "r") as json_example_card:
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
                        self._remove_sensitive_entries(entry)
                except Exception as exc:
                    continue

                with open(file, "w") as anonymized_file:
                    json.dump(to_anonymize, anonymized_file, indent=1)

    def _remove_sensitive_entries(self, entry):
        try:
            entry["seller"]["idUser"] = 0
        except:
            pass
        try:
            entry["seller"]["username"] = ""
        except:
            pass
        try:
            del entry["seller"]["name"]
        except:
            pass
        try:
            country = entry["seller"]["address"]["country"]
            del entry["seller"]["address"]
            entry["seller"].update({"address": {"country": country}})# keep country
        except:
            pass
        try:
            del entry["seller"]["phone"]
        except:
            pass
        try:
            del entry["seller"]["email"]
        except:
            pass
        try:
            del entry["seller"]["vat"]
        except:
            pass


if __name__ == "__main__":
    anonymizer = TestDataProvider().anonymize_data()

