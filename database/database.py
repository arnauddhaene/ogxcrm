#!/usr/bin/python
# -- coding: utf-8 --

from database.person import Person
from database.trello import Trello
from database.expa import Expa

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
        self.people = self.get()

    def get(self, ):
        """
        Get's all information concerning people

        :return: a list of (Person)s
        """

        self.expa.get()
        self.trello.get()

    def print_new(self):

        print([person for person in self.people if person.trello == False])