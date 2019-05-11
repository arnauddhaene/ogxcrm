#!/usr/bin/python
# -- coding: utf-8 --

from trello import Trello
from expa import Expa

class Database:
    """ Information relative to a person wanting to leave on exchange.
    """

    def __init__(self, expaToken, trelloToken, trelloKey, idBoard, additionalIDs=None):
        """
        Initializes de Database 
        
        :param expaToken: access token provided by Expa for AIESEC members 
        :param trelloToken: Trello token giving access to the API of the wanted account
        :param trelloKey: Trello key giving access to the API of the wanted account
        :param idBoard: board ID from trello
        :param additionalIDs: List of IDs of people who have to be added to Trello and are not in the wanted period
        """

        self.expa = Expa(expaToken)
        self.trello = Trello(trelloToken, trelloKey, idBoard)
        self.people = []
        self.additionalIDs = additionalIDs

    def get(self, ):
        """
        Get's all information concerning people

        :return: a list of (Person)s
        """

        # get all people that Signed Up in wanted date frame
        self.people = self.expa.getPeople()

        # get all additional people using their specific EXPA IDs
        if self.additionalIDs is not None:
            for personId in self.additionalIDs:

                self.people.append(self.expa.getPerson(personId))

        self.trello.updatePeople(self.people)
        self.display()

    def display(self):
        """
        Displays result of People and who needs to be added to Trello
        :return:
        """
        self.displayUpdate()
        self.displayPush()

    def displayUpdate(self):

        print("\n ===== DATABASE COUNT ===== {} SIGN UPS: \n".format(len(self.people)))

        for x in range(len(self.people)):
            print self.people[x]

    def displayPush(self):

        toPush = [person for person in self.people if person.trello == False]

        print "\n ===== TRELLO UPDATE ===== {} people will be added to Trello :\n".format(len(toPush))
        print(toPush)

    def push(self):
        """
        Pushes people to Trello that are not yet on Trello
        """

        self.trello.pushPeopleToList(self.people, '5cb1f6163e3fc475f62e9ff0')

    def checkManagers(self): # TODO implement this

        pass

        """
        
        SU_people = trello.get_SignedUp_people()
        
        self.people = expa.get_data()
        
        for element in range(len(SU_people)):
            n
            if not SU_people[element]['name'] in self.people
        
        """