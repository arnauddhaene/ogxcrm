#!/usr/bin/python
# -- coding: utf-8 --

from trello import Trello
from expa import Expa
from apiService import ExpaService
from fuzzywuzzy import process
import yagmail

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
        self.expaService = ExpaService(expaToken)
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
            print(self.people[x])

    def displayPush(self):

        toPush = [person for person in self.people if person.trello == False]

        print("\n ===== TRELLO UPDATE ===== {} people will be added to Trello :\n".format(len(toPush)))
        print(toPush)

    def push(self):
        """
        Pushes people to Trello that are not yet on Trello
        """

        self.trello.pushPeopleToList(self.people, '5cb1f6163e3fc475f62e9ff0')

    def moveFromAssigned(self):

        ogxMembers = []
        matchedOgxIndices = []

        trelloMembers = self.trello.getBoardMembers()
        expaTeams = self.expaService.getCurrentTeams()["data"]
        for team in expaTeams:
            if "outgoing" in team["title"].lower():
                expaMembers = self.expaService.getTeamMembers(team["id"])["data"]
                expaMembersNames = [ m["person"]["full_name"].lower() for m in expaMembers ]

                for m_trello in trelloMembers:
                    query = m_trello["fullName"].lower()
                    match = process.extractOne(query, expaMembersNames) # (name, score)

                    if match[1] > 90:
                        idx = expaMembersNames.index(match[0])
                        if idx not in matchedOgxIndices:
                            matchedOgxIndices.append(idx)
                            m_expa = expaMembers[idx]

                            person = self.expaService.getPerson(expaMembers[idx]["person"]["id"])
                            # build phone number
                            phone = ""
                            if person:
                                if person["country_code"]:
                                    phone = person["country_code"]
                                if person["phone"]:
                                    phone += person["phone"]

                            ogxMembers.append({
                                "trelloId": m_trello["id"],
                                "expaId": expaMembers[idx]["person"]["id"],
                                "email": expaMembers[idx]["person"]["aiesec_email"],
                                "firstName": expaMembers[idx]["person"]["first_name"],
                                "fullName": expaMembers[idx]["person"]["full_name"],
                                "phone": phone
                            })
                        else:
                            print("Error: duplicate match for Trello user {}".format(m_trello["fullName"]))

                    else:
                        print("No EXPA match for Trello user {}".format(m_trello["fullName"]))
                break

        cards = self.trello.getCardsFromList(self.trello.listAssignedId)
        for card in cards:
            cardMembers = card["idMembers"]
            if not cardMembers:
                continue

            memberId = cardMembers[0]
            for member in ogxMembers:
                if member["trelloId"] == memberId:
                    email_from = "info.lausanne@aiesec.ch"
                    email_reply_to = member["email"]
                    email_reply_to_name = member["fullName"]
                    email_reply_to_phone = member["phone"]

                    # we GUCCI
                    name_to = card["name"]
                    data = { "name": card["name"] }
                    # extract data from description
                    for info in card["desc"].split("\n"):
                        split = info.split(":")
                        data[split[0].strip().lower()] = split[1].strip()

                    email_to = data["email"]

                    print(f"Sending email to {name_to} <{email_to}>")

                    body = """<!doctype HTML><html><head></head><body><p>Hello {0},<br/>
Je m’appelle {1}, je suis membre du comité AIESEC Lausanne. Je me permets de t’écrire suite à ton passage à notre stand à l’amphimax ce mercredi!
Comme tu le sais on organise de stages de volontariat ainsi que des stages professionnels à travers le monde entier, je suis là pour répondre à tes questions et te conseiller pour trouver le stage idéal pour toi. Nos partenaires en ce moment incluent Costa Rica, Vietnam, Egypte, Turquie, Argentine, Kenya, Uganda, Mexique, Pérou, Inde, et Colombie !
Je t’invite à t’inscrire sur notre site internet (<a href="https://aiesec.ch" target="_blank">aiesec.ch</a>) et à m’envoyer un message au <a href="tel:{2}">{3}</a>. Ce serait super qu’on fixe un rendez-vous afin de pouvoir en discuter.<br/>
Salutations,
{4}</p></body></html>
                    """.format(data["name"].split(" ")[0], member["firstName"], email_reply_to_phone, email_reply_to_phone, email_reply_to_name)

                    yag = yagmail.SMTP(user="info.lausanne@aiesec.ch",password="Executiveboard1920")
                    yag.send(
                        to=email_to,
                        subject="Bienvenue | AIESEC",
                        contents=body,
                        headers={"Reply-To": f"{email_reply_to_name} <{email_reply_to}>"}
                    )

                    self.trello.moveCardToList(card["id"], self.trello.listFirstEmailSent)



    def checkManagers(self): # TODO implement this

        pass

        """

        SU_people = trello.get_SignedUp_people()

        self.people = expa.get_data()

        for element in range(len(SU_people)):
            n
            if not SU_people[element]['name'] in self.people

        """
