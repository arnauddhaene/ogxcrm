#!/usr/bin/python
# -- coding: utf-8 --

class Person:
    """ Information relative to a person wanting to leave on exchange.
    """

    def __init__(self, id, name, email, dob, phone, sud, link, status, managers=None, trello=False, trelloId=None, **args):
        """
        Initializes the instance of the representation of a person in the database

        :param id: EXPA id
        :param name:
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

        self.id = id
        self.name = name.encode('utf-8').strip()
        self.email = email
        self.dob = dob
        self.phone = phone
        self.sud = sud
        self.link = link
        self.status = status
        self.managers = managers
        self.trello = trello
        self.trelloId = trelloId

        # if there are any additional arguments
        for key, value in args.items():
            setattr(self, key, value)

    def __eq__(self, other):
        """
        Equality evaluator surcharge

        :param other: the other person being compared to
        :return: True or False, self is equal to other ?
        """
        return self.id == other.id

    def __repr__(self):
        return '\nNom : {} | SUD : {} | Status : {} | Managers : {}'.format(self.name, self.sud, self.status, self.managers)
