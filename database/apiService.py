#!/usr/bin/python
# -- coding: utf-8 --

import requests
import json
from html.parser import HTMLParser

class ApiService:
    """
    API request handler
    """

    def __init__(self, baseUrl, params):
        """
        Initialises a service to access data from an API

        :param baseUrl: base URL for requests
        :param params: map of request arguments to include in every request
        """

        self.baseUrl = baseUrl
        self.params = params

    def get(self, url, params={}, toJson=True):
        """
        GET a resource

        :param url: endpoint of resource
        :param params: optional request arguments
        """

        # create endpoint URL
        endpoint = self.baseUrl + url
        # add base params to request parameters
        query = dict(self.params, **params)

        result = requests.get(endpoint, query)
        return result.json() if (result.ok and toJson) else result

    def put(self, url, body, params={}, toJson=True):
        """
        PUT a resource

        :param url: endpoint of resource
        :param body: resource to PUT
        :param params: optional request arguments
        """

        # create endpoint URL
        endpoint = self.baseUrl + url
        pms = [key + '=' + self.params[key] for key in self.params]
        if len(pms) > 0:
            endpoint += '?'
            endpoint += "&".join(pms)

        # add base params to request parameters
        query = params

        result = requests.put(endpoint, data=body, params=query)
        return result.json() if (result.ok and toJson) else result

    def post(self, url, body, params={}, toJson=True):
        """
        POST a resource

        :param url: endpoint of resource
        :param body: resource to POST
        :param params: optional request arguments
        """

        # create endpoint URL
        endpoint = self.baseUrl + url
        pms = [key + '=' + self.params[key] for key in self.params]
        if len(pms) > 0:
            endpoint += '?'
            endpoint += "&".join(pms)

        # add base params to request parameters
        query = params

        result = requests.post(endpoint, data=body, params=query)
        return result.json() if (result.ok and toJson) else result


# this class is WIP
class ExpaLoginService(ApiService):
    """
    Login service for communication with the EXPA server
    """

    def __init__(self):
        """
        Init class
        Very useful comment indeed
        """
        super().__init__("https://auth.aiesec.org", {})

    def sign_in(self, email, pwd):
        """
        Sign in the user

        :param username: expa username
        :param pwd: expa password
        """

        endpoint = "/users/sign_in"
        authenticity_token = self.get_authenticity_token()
        body = {
            "utf8": "✓",
            "authenticity_token": authenticity_token,
            "user[email]": email,
            "user[password]": pwd,
            "commit": "Log in"

        }

        return self.post(endpoint, body, toJson=False)

    def get_authenticity_token(self):

        # retrieve sign in page
        content = self.get("/users/sign_in", toJson=False).text

        # parse page
        class MyHTMLParser(HTMLParser):
            def __init__(self):
                # initialize the base class
                HTMLParser.__init__(self)
                self.authenticity_token = None

            def handle_starttag(self, tag, attrs):
                if tag == "meta":
                    for attr in attrs:
                        if attr[0] == "csrf-token":
                            self.authenticity_token = attr[1]
                            break

        parser = MyHTMLParser()
        parser.feed(content)

        return parser.authenticity_token
