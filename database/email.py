#!/usr/bin/python
# -- coding: utf-8 --

import yagmail

class Email:

    def __init__(self, template):
        self.template = ""
        with open(template, 'r', encoding='utf-8') as file:
            self.template = file.read()

    def effify(self, non_f_str: str):
        return eval(f'f"""{non_f_str}"""')

    def send(self, from_, to, subject, headers, cc=True):
        """
        Send an email from info.lausanne@aiesec.ch, with cc to sender

        :param from_: object representing the sender - fields are first_name, name (full name), phone, aiesec_email
        :param to: object representing the target - mandatory fields are first_name, name (full name) and email
        :param subject: email subject
        :param headers: additional headers
        """

        first_name = to["first_name"]
        name = to["name"]
        email = to["email"]

        member = from_

        # replace template expressions by values
        # possible values are
        # name, email, member.aiesec_email, member.phone, member.first_name, member.name
        body = eval(f'f"""{self.template}"""')

        # log into account
        pwd = input("Password for info.lausanne@aiesec.ch: ")
        yag = yagmail.SMTP(user="info.lausanne@aiesec.ch", password=pwd)
        yag.send(
            to=email,
            subject=subject,
            contents=body,
            headers=headers,
            cc=member.aiesec_email if cc else None
        )
