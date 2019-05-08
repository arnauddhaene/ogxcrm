#!/usr/bin/python
# -- coding: utf-8 --

import requests
import json

class Trello:
    """ Information relative to a person wanting to leave on exchange.
    """

    # manager library
    # key is the expa ID, label is the trello ID --> { 'expa ID' :  'Trello ID' }
    # Anais, Daniella, Gwenaelle, Jonas, Lucas, Adrien, Dylan, Jeremy, Morgane
    team = {'1856304': '5cbae2c59d966941df8d9b5f',
            '2108256': '5cb5dae61646158e92621248',
            '2209383': '5cb739286550d048542b0081',
            '2709530': '5cb4418c84476835eb75e95b',
            '2154457': '5cb73b6e19cff548f71ca5b2',
            '2064165': '5cb71e2e16cb0e546c301cef',
            '1803727': '5cb71e2f7f653c623d9aaa1f',
            '996944': '5cb85bdf02feea45bc7f89e1',
            '3001465': '5cbae37ccb202f790b6d9297'}


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


    def update_people(self, people):
        """
        Get's all card information from Trello

        :param people: people from expa
        """

        # first, we need to check who's already accounted for on Trello
        url = "https://api.trello.com/1/boards/5cb1f5a13ae5f15b88be935d/cards"

        querystring = {"fields": "name,idMembers",  # can add idMembers to check appointed members
                       "key": "448b14b4374aaa9429f4a8b979936e2b",
                       "token": "9f9de4286e6a5f627f083dc3ca8fdf6dceae7307a06c5e9dcedda4212491a4e3"}

        data = json.loads(requests.request("GET", url, params=querystring).text)

        # noms des personnes déjà dans le système (ceux sur Trello)
        names = [element['name'].encode('utf-8').strip() for element in data]

        for person in people:
            if person.name in names:
                person.trello = True


    def push_trello(self, people) :
        """
        Push new people on Trello

        :param people:
        """

        idList_SignUp = '5cb1f6163e3fc475f62e9ff0'

        params = {"key": "448b14b4374aaa9429f4a8b979936e2b",
                    "token": "9f9de4286e6a5f627f083dc3ca8fdf6dceae7307a06c5e9dcedda4212491a4e3"}

        response = []

        for person in people:

            if not person.trello:    # If person in people is not on Trello CRM

                url = "https://api.trello.com/1/cards"

                description = "DOB: " + person.dob + '\n' + "Phone: " + person.phone + '\n' + "Email: " + person.email + '\n' + "SUD: " + person.sud + '\n'

                querystring = {'name' : person.name, 'desc' : description, 'pos' : 'top', 'due' : person.sud, 'dueComplete' : 'true', 'idList' : idList_SignUp }

                response.append(requests.request("POST", url, params=params, data=querystring))

        print("TRELLO PUSH :::: " + str(len(response)) + " CARDS ADDED TO OGX CRM")


    def push_trello_special(self, special_people, specialID):
        """
        Push special IDs on trello
        :param special_people:
        :param specialID:
        :return:
        """

        idList_SignUp = '5cb1f6163e3fc475f62e9ff0'

        params = {"key": "448b14b4374aaa9429f4a8b979936e2b",
                  "token": "9f9de4286e6a5f627f083dc3ca8fdf6dceae7307a06c5e9dcedda4212491a4e3"}

        IDs = specialID
        specialpeople = special_people

        response = []

        for i in range(len(IDs)):

            for person in specialpeople:

                if person.expaId == int(IDs[i]):

                    if not person.trello:  # If person in people is not on Trello CRM

                        url = "https://api.trello.com/1/cards"

                        person.trello = True

                        description = "DOB: " + person.dob + '\n' + "Phone: " + person.phone + '\n' + "Email: " + person.email + '\n' + "SUD: " + person.sud + '\n'

                        querystring = {'name': person.name, 'desc': description, 'pos': 'top', 'due': person.sud,
                                       'dueComplete': 'true', 'idList': idList_SignUp}

                        response.append(requests.request("POST", url, params=params, data=querystring))



        print("TRELLO PUSH :::: " + str(len(response)) + " SPECIAL CARDS ADDED TO OGX CRM")


    def get_SignedUp_people(self):
        """
        Get a list of people present in the "Signed Up" list on Trello
        :return:
        """

        SU_People = []


        url = "https://api.trello.com/1/lists/"
        idList = '5cb1f6163e3fc475f62e9ff0'             #ID of the "Signed Up" List

        url1 = url + idList + "/cards"

        querystring = {"fields": "name",
                       "key": "448b14b4374aaa9429f4a8b979936e2b",
                       "token": "9f9de4286e6a5f627f083dc3ca8fdf6dceae7307a06c5e9dcedda4212491a4e3"}

        SU_People = json.loads(requests.request("GET", url1, params=querystring).text)

        return SU_People




    def Push_SignedUp_To_Assigned(self, id):
        """
        People present in the "Signed up" list and who have been assigned to a manager different from the VP are pushed in the "Assigned" List

        :return:
        """

        self.idCard = id

        key = "448b14b4374aaa9429f4a8b979936e2b"
        token = "9f9de4286e6a5f627f083dc3ca8fdf6dceae7307a06c5e9dcedda4212491a4e3"
        url = "https://api.trello.com/1/cards"
        AssignedListID = "5cb2e4b0c7a5380b61388d80"

        url1 = url + '/' + self.idCard

        requests.put(url1, params = dict(key = key, token = token),data = dict(idList = AssignedListID))






