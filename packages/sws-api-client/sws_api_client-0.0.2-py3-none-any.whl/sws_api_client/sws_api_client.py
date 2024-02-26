import argparse
import json
import os

import requests


class SwsApiClient:

    def __init__(self, sws_endpoint: str, access_token: str) -> None:
        self.sws_endpoint = sws_endpoint
        self.access_token = access_token
        self.discover = self.__get_discover()

    def __get_discover(self) -> dict:
        discover_endpoint = f"{self.sws_endpoint}/discover?v=2"
        headers = {"Authorization": self.access_token}
        return requests.get(url=discover_endpoint, headers=headers).json()

    @classmethod
    def from_env(cls, sws_endpoint_env="SWS_ENDPOINT", access_token_env="ACCESS_TOKEN"):
        return cls(
            sws_endpoint=os.getenv(sws_endpoint_env),
            access_token=os.getenv(access_token_env),
        )

    @classmethod
    def from_conf(cls, conf_file="conf_sws_api_client.json"):
        with open(conf_file) as f:
            kwargs = json.load(f)
            return cls(**kwargs)

    @classmethod
    def from_args(cls):
        parser = argparse.ArgumentParser(
            description="Instantiate SwsApiClient from args"
        )
        parser.add_argument(
            "--sws_endpoint", type=str, required=True, help="The sws endpoint"
        )
        parser.add_argument(
            "--access_token", type=str, required=True, help="The access token"
        )

        args, _ = parser.parse_known_args()

        return cls(**vars(args))

    def get_dataset_export_details(self, dataset_id: str) -> dict:

        session_api_key = self.discover["session_api"]["key"]
        session_api_path = self.discover["session_api"]["path"]

        url = f"{session_api_path}/dataset/{dataset_id}/info"
        params = {"extended": "true"}
        headers = {"Authorization": self.access_token, "x-api-key": session_api_key}

        response = requests.get(url, params=params, headers=headers).json()

        return response

    def get_read_access_url(self, path: str, expiration: int) -> dict:

        tag_api_key = self.discover["tag_api"]["key"]
        tag_api_path = self.discover["tag_api"]["path"]

        url = f"{tag_api_path}/tags/dissemination/getReadAccessUrl"
        body = {"path": path, "expiration": expiration}
        headers = {"Authorization": self.access_token, "x-api-key": tag_api_key}

        response = requests.post(url, json=body, headers=headers).json()

        return response
