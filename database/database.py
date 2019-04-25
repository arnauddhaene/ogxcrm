#!/usr/bin/python
# -- coding: utf-8 --

class Database:
    """ Information relative to a person wanting to leave on exchange.
    """

    def __init__(self, ):
        """
        Initialises the person
        """

        self.expa = expa
        self.people = self.expa.get()

    def get(self, ):
        """
        Get's all information from Trello
        :return:
        """

    def print_new(self):

        print([person for person in self.people if person.trello == False]