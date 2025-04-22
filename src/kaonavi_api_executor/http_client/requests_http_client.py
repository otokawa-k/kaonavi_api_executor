from .http_client import HttpClient
import requests

class RequestsHttpClient(HttpClient):

    def __init__(self):
        pass

    def post(self, url: str, data: dict, headers: dict, auth) -> dict:
        return requests.post(url, data=data, headers=headers, auth=auth)

    def get(self, url, params=None, headers=None, auth=None):
        return requests.get(url, params=params, headers=headers, auth=auth)