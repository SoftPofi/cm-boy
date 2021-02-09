#!/usr/bin/env python3

from requests_oauthlib import OAuth1Session
import time

class CmSession:

    def __init__(self, base_url, confidential_config):
        self.api_client = None
        self.base_url = base_url
        self.confidential_config = confidential_config

    def generate_full_url(self, url, url_ext):
        if url is None:
            if url_ext is None:
                raise ValueError("No URL and no URL Extension given, can't request anything.")
            else:
                url = "{}{}".format(self.base_url, url_ext)
        return url

    def _update_client_session_url(self, url=None, url_ext=None, ):
        url = self.generate_full_url(url, url_ext)
        self.api_client = OAuth1Session(self.confidential_config["cm_access"]["app_token"],
                                        client_secret=self.confidential_config["cm_access"]["app_secret"],
                                        resource_owner_key=self.confidential_config["cm_access"]["access_token"],
                                        resource_owner_secret=self.confidential_config["cm_access"]["access_secret"],
                                        realm=url
                                        )

    def get_data(self, url=None, url_ext=None, params=None, retries=3, timeout=30):
        resp = None
        url = self.generate_full_url(url, url_ext)
        self._update_client_session_url(url)
        for no_retries in range(0, retries):
            resp = self.api_client.get(url, params=params)
            if resp.status_code in [200, 206]:
                return resp
            else:
                time.sleep(timeout)
        return resp

    def put_data(self, body=None, url=None, url_ext=None, params=None, retries=3, timeout=30):
        resp = None
        url = self.generate_full_url(url, url_ext=url_ext)
        self._update_client_session_url(url)
        for no_retries in range(0, retries):
            resp = self.api_client.put(url, data=body)
            if resp.status_code in [200, 206]:
                return resp
            else:
                time.sleep(timeout)
        return resp
