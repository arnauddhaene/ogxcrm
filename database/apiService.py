#!/usr/bin/python
# -- coding: utf-8 --

import requests
import json

class ApiService:
    """
    API request handler
    """

    def __init__(self, baseUrl, params):
        """
        Initialises the link with the Trello API

        :param params: Map of relevant parameters for the requests
        """
        self.baseUrl = baseUrl
        self.params = params

    def get(url, params={}):
        # create endpoint URL
        endpoint = self.baseURL + url
        # add base params to request parameters
        query = dict(self.params, **params)

        result = requests.get(endpoint, query).text
        return json.loads(result)

    def put(url, body, params={}):
        # create endpoint URL
        endpoint = self.baseURL + url
        # add base params to request parameters
        query = dict(self.params, **params)

        result = requests.put(endpoint, body, query).text
        return json.loads(result)

    def post(url, body, params={}):
        # create endpoint URL
        endpoint = self.baseURL + url
        # add base params to request parameters
        query = dict(self.params, **params)

        result = requests.post(endpoint, body, query).text
        return json.loads(result)

class TrelloService(ApiService):

    def __init__(self):
        baseUrl = "https://api.trello.com/1"
        params = {
            "key": "448b14b4374aaa9429f4a8b979936e2b",
            "token": "9f9de4286e6a5f627f083dc3ca8fdf6dceae7307a06c5e9dcedda4212491a4e3"
        }

        super().__init__(self, baseUrl, params)

class ExpaService(ApiService):

    def __init__(self, token):
        baseUrl = "https://gis-api.aiesec.org/v2"
        params = {
            "access_token": token
        }

        super().__init__(self, baseUrl, params)
