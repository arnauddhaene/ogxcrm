#!/usr/bin/python
# -- coding: utf-8 --

class Person:
    """ Information relative to a person wanting to leave on exchange.
    """

    def __init__(self, name, expaId, email, dob, phone, sud, link, status, managers=None, trello=False, trelloId=None):
        """
        Initializes the instance of the representation of a person in the database

        :param name:
        :param expaId:
        :param email:
        :param dob:
        :param phone:
        :param sud:
        :param link:
        :param status:
        :param managers:
        :param trello:
        :param trelloId:
        """

        self.name = name
        self.expaId = id
        self.email = email
        self.dob = dob
        self.phone = phone
        self.sud = sud
        self.link = link
        self.status = status
        self.managers = managers
        self.trello = trello
        self.trelloId = trelloId


    def __eq__(self, other):
        """
        Equality evaluator surcharge

        :param other: the other person being compared to
        :return: True or False, self is equal to other ?
        """
        return self.id == other.id

    def __repr__(self):

        return 'Nom : {} | SUD : {} | Status : {}'.format(self.name, self.sud, self.status)