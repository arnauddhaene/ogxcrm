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
        self.listIds = self.getListIds()

    def getListIds(self):

        # Extraction from the Trello Dashboard Lists
        # First, we need the List IDs and their respective names

        url = "https://api.trello.com/1/boards/{}/lists".format(self.idBoard)

        querystring = {"cards": "none", "filter": "open", "fields": "all",
                       "key": self.key, "token": self.token}

        response = json.loads(requests.request("GET", url, params=querystring).text)

        listIds = {}

        for list in response:
            listIds[list['name']] = list['id']

        return listIds

    def updatePeople(self, people):
        """
        Get's all card information from Trello

        :param people: people from expa
        """

        # first, we need to check who's already accounted for on Trello
        url = "https://api.trello.com/1/boards/{}/cards".format(self.idBoard)

        querystring = {"fields": "name,idMembers",  # can add idMembers to check appointed members
                       "key": self.key, "token": self.token}

        data = json.loads(requests.request("GET", url, params=querystring).text)

        # noms des personnes déjà dans le système (ceux sur Trello)
        names = [element['name'].encode('utf-8').strip() for element in data]

        for person in people:
            if person.name in names:
                person.trello = True


    def pushPeopleToList(self, people, listId) :
        """
        Push new people on Trello

        :param people:
        """

        # idList_SignUp = '5cb1f6163e3fc475f62e9ff0'

        params = {"key": self.key, "token": self.token}

        response = []

        for person in people:

            if not person.trello:    # If person in people is not on Trello CRM

                url = "https://api.trello.com/1/cards"

                description = "DOB: " + person.dob + '\n' + "Phone: " + person.phone\
                              + '\n' + "Email: " + person.email + '\n' + "SUD: " + person.sud + '\n'

                querystring = {'name' : person.name, 'desc' : description, 'pos' : 'top',
                               'due' : person.sud, 'dueComplete' : 'true', 'idList' : listId }

                response.append(requests.request("POST", url, params=params, data=querystring))

        self.displayPush(len(response))

    def displayPush(self, numberOfCardsAdded):
        """
        Displays message concerning Trello Push
        :param numberOfCardsAdded: number of cards added to Trello
        """

        print("\n ==== TRELLO PUSH ==== {} CARDS ADDED TO OGX CRM".format(numberOfCardsAdded))

    def getCardsFromList(self, listId):
        """
        Get a list of people present in the "Signed Up" list on Trello

        :param listId: ID of the Trello List we want to fetch cards from
        :return: cards: json loads list of people pulled from list
        """

        # SIGNED UP list ID '5cb1f6163e3fc475f62e9ff0' [TODO: integrate this function somewhere]

        url = "https://api.trello.com/1/lists/" + listId + "/cards"

        querystring = {"fields": "name",
                       "key": self.key, "token": self.token}

        cards = json.loads(requests.request("GET", url, params=querystring).text)

        return cards


    def moveCardToList(self, cardId, listId):
        """
        Moves a specific card to a specific list
        People present in the "Signed up" list and who have been assigned to a manager different from the VP are
        pushed in the "ASSIGNED" List
        :param cardId: ID of the Trello card ID that needs to change list
        :return: done or not
        """

        url = "https://api.trello.com/1/cards" + '/' + cardId

        # AssignedListID is "5cb2e4b0c7a5380b61388d80" [TODO: integrate this function somewhere]

        requests.put(url, params = dict(key=self.key, token=self.token), data=dict(idList=listId))

        # TODO: find a way to return True if successful and False if unsuccessful
        # return