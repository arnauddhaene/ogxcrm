#!/usr/bin/python
# -- coding: utf-8 --

from apiService import TrelloService

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
        self.idBoard = "5cb1f5a13ae5f15b88be935d"
        self.listAssignedId = "5cb2e4b0c7a5380b61388d80"
        self.listSignedUpId = "5cb1f6163e3fc475f62e9ff0"
        self.listFirstEmailSent = "5cb1f72f2475f55104264aed"
        self.trelloService = TrelloService()
        self.listIds = self.getListIds()

    def getListIds(self):
        # Extraction from the Trello Dashboard Lists
        # First, we need the List IDs and their respective names
        url = "/boards/" + self.idBoard + "/lists"
        params = {
            "cards": "none",
            "filter": "open",
            "fields": "all"
        }

        response = self.trelloService.get(url, params)
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
        url = "/boards/" + self.idBoard + "/cards"
        params = {"fields": "name,idMembers"}  # can add idMembers to check appointed members

        data = self.trelloService.get(url, params)

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
        url = "/cards"
        response = []

        for person in people:
            if not person.trello:    # If person in people is not on Trello CRM

                description = "DOB: " + person.dob + '\n' + "Phone: " + person.phone\
                              + '\n' + "Email: " + person.email + '\n' + "SUD: " + person.sud + '\n'

                body = {
                    'name' : person.name,
                    'desc' : description,
                    'pos' : 'top',
                    'due' : person.sud,
                    'dueComplete': 'true',
                    'idList': listId
                }

                response.append(self.trelloService.post(url, body))

        self.displayPush(len(response))

    def displayPush(self, numberOfCardsAdded):
        """
        Displays message concerning Trello Push
        :param numberOfCardsAdded: number of cards added to Trello
        """

        print("\n ===== TRELLO PUSH ===== {} CARDS ADDED TO OGX CRM".format(numberOfCardsAdded))

    def getCardsFromList(self, listId):
        """
        Get a list of people present in the "Signed Up" list on Trello

        :param listId: ID of the Trello List we want to fetch cards from
        :return: cards: json loads list of people pulled from list
        """

        # SIGNED UP list ID '5cb1f6163e3fc475f62e9ff0' [TODO: integrate this function somewhere]
        url = "/lists/" + listId + "/cards"
        params = { "fields": "name,idMembers,desc" }

        return self.trelloService.get(url, params)

    def getBoardMembers(self):
        url = "/boards/" + self.idBoard + "/members"
        return self.trelloService.get(url)

    def moveCardToList(self, cardId, listId):
        """
        Moves a specific card to a specific list
        People present in the "Signed up" list and who have been assigned to a manager different from the VP are
        pushed in the "ASSIGNED" List
        :param cardId: ID of the Trello card ID that needs to change list
        :return: done or not
        """

        url = "/cards/" + cardId
        body = { "idList": listId }

        # AssignedListID is "5cb2e4b0c7a5380b61388d80" [TODO: integrate this function somewhere]
        self.trelloService.put(url, body)

        # TODO: find a way to return True if successful and False if unsuccessful
        # return
