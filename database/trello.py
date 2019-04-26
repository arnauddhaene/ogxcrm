#!/usr/bin/python
# -- coding: utf-8 --

import requests
import json

class Trello:
    """ Information relative to a person wanting to leave on exchange.
    """

    def __init__(self, token, key, idBoard):
        """
        Initialises the link with the Trello API

        :param key: Given by Trello API
        :param token: Given by Trello API
        :param idBoard: Trello board ID
        """
        self.key = key
        self.token = token
        self.idBoard = idBoard

    def get(self):
        """
        Get's all card information from Trello

        """

        # first, we need to check who's already accounted for on Trello
        url = "https://api.trello.com/1/boards/5cb1f5a13ae5f15b88be935d/cards"

        querystring = {"fields": "name,idMembers",  # can add idMembers to check appointed members
                       "key": "448b14b4374aaa9429f4a8b979936e2b",
                       "token": "9f9de4286e6a5f627f083dc3ca8fdf6dceae7307a06c5e9dcedda4212491a4e3"}

        data = json.loads(requests.request("GET", url, params=querystring).text)

        # noms des personnes déjà dans le système (ceux sur Trello)
        names = [element['name'] for element in data]

        for person in people:
            if person.name in names:
                person.trello = True
