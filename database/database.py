#!/usr/bin/python
# -- coding: utf-8 --

from trello import Trello
from expa import Expa

class Database:
    """ Information relative to a person wanting to leave on exchange.
    """

    def __init__(self, expaToken, trelloToken, trelloKey, idBoard):
        """
        Initializes de Database 
        
        :param expaToken: access token provided by Expa for AIESEC members 
        :param trelloToken: Trello token giving access to the API of the wanted account
        :param trelloKey: Trello key giving access to the API of the wanted account
        :param idBoard: board ID from trello
        """

        self.expa = Expa(expaToken)
        self.trello = Trello(trelloToken, trelloKey, idBoard)
        self.people = []
        self.get()

    def get(self, ):
        """
        Get's all information concerning people

        :return: a list of (Person)s
        """

        self.people = self.expa.get_data()
        self.trello.update_people(self.people)
        self.print_new()
        self.trello.push_trello(self.people)


    def print_new(self):

        to_add = [person for person in self.people if person.trello == False]

        print "\n ===== TRELLO UPDATE =====\n {} people will be added to Trello :".format(len(to_add))
        print(to_add)


    def Check_Managers (self) :

        pass

        """
        
        SU_people = trello.get_SignedUp_people()
        
        self.people = expa.get_data()
        
        for element in range(len(SU_people)):
            n
            if not SU_people[element]['name'] in self.people
        
        """
