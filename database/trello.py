#!/usr/bin/python
# -- coding: utf-8 --

from database.apiService import ApiService

class TrelloService(ApiService):
    """
    API service for Trello resources
    """

    def __init__(self):
        baseUrl = "https://api.trello.com/1"
        params = {
            "key": "f96139525bca604d080b712989ebc84c", #"448b14b4374aaa9429f4a8b979936e2b",
            "token": "f00985a288931c8148e3731dd2df088c2c3a111a2bcdf6a01e8cd5b0cf01cb16"  #"9f9de4286e6a5f627f083dc3ca8fdf6dceae7307a06c5e9dcedda4212491a4e3"
        }

        super().__init__(baseUrl, params)

        self.idBoard = "5cb1f5a13ae5f15b88be935d"
        self.listSignedUpId = "5cb1f6163e3fc475f62e9ff0"
        self.listAssignedId = "5cb2e4b0c7a5380b61388d80"
        self.listFirstEmailSent = "5cb1f72f2475f55104264aed"
        # self.listIds = self.getListIds()

    def getListIds(self):
        """
        Get all list ids from OGX board
        """

        url = f"/boards/{self.idBoard}/lists"
        params = {
            "cards": "none",
            "filter": "open",
            "fields": "all"
        }

        response = self.get(url, params)
        listIds = {}

        # map response to {name, id} pair
        for list in response:
            listIds[list['name']] = list['id']

        return listIds

    def updatePeople(self, people):
        """
        Get all card information from Trello

        :param people: people from EPXA
        """
        data = self.getAllCards()

        # people already on Trello
        names = [person['name'].encode('utf-8').strip() for person in data]

        for person in people:
            if person.name in names:
                person.trello = True

    def postNewPeople(self, people):
        """
        Push new people on Trello

        :param people: list of people to add to Trello
        """
        pushed = 0
        for person in people:
            if not person.trello:
                # build description for Trello card
                description = "\n".join((
                     "DOB: " + person.dob,
                     "Phone: " + person.phone,
                     "Email: " + person.email,
                     "SUD: " + person.sud
                ))

                # build body for API call
                body = {
                    'name'          : person.name,
                    'desc'          : description,
                    'pos'           : 'top',
                    'due'           : person.sud,
                    'dueComplete'   : 'true',
                    'idList'        : self.listSignedUpId
                }

                result = self.post("/cards", body, toJson=False)
                if not result.ok:
                    print(f"Error creating new card for {person.name}: {result.text} (Status {result.status_code})")
                else:
                    pushed += 1

        self.displayPush(pushed)

    def displayPush(self, nNewCards):
        """
        Displays message concerning Trello Push
        :param numberOfCardsAdded: number of cards added to Trello
        """

        print("\n ===== TRELLO PUSH ===== {} CARDS ADDED TO OGX CRM".format(nNewCards))

    def getCardsFromList(self, listId):
        """
        Get cards present in a list

        :param listId: ID of the Trello list we want to fetch cards from

        :return: list of cards pulled from list
        """

        url = f"/lists/{listId}/cards"
        params = { "fields": "name,idMembers,desc" }

        return self.get(url, params)

    def getAllPeople(self): return self.getAllCards()
    def getAllCards(self):
        """
        Get all cards in the OGX board
        """

        url = f"/boards/{self.idBoard}/cards"
        params = { "fields": "name,idMembers" }

        return self.get(url, params)

    def getAllMembers(self):
        """
        Get all members in the OGX board
        """

        return self.get(f"/boards/{self.idBoard}/members")

    def moveCardToList(self, cardId, listId):
        """
        Moves a specific card to a specific list.

        :param cardId: id of the Trello card that needs to change list
        :param listId: id of the Trello list to move the card to

        :return: success of operation
        """

        url = f"/cards/{cardId}"
        body = { "idList": listId }

        result = self.put(url, body)
        return result.ok
