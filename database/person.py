#!/usr/bin/python
# -- coding: utf-8 --

class Person:
    """ Information relative to a person wanting to leave on exchange.
    """

    def __init__(self, name, id, email, dob, phone, sud, link, status, managers=None, trello=False):
        """ Initialises the person
        """

        self.name = name
        self.id = id
        self.email = email
        self.dob = dob
        self.phone = phone
        self.sud = sud
        self.link = link
        self.status = status
        self.managers = managers
        self.trello = trello


    def __eq__(self, other):
        """ Equality surcharge

            :param other: the other person being compared to
        """

        return self.id == other.id

    def __repr__(self):

        return 'Nom : {} | Status : {}'.format(self.name, self.status)