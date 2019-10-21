#!/usr/bin/python
# -- coding: utf-8 --

from database.trello import TrelloService
from database.expa import ExpaService
from fuzzywuzzy import process
import yagmail

class Database:
    """ Information relative to a person wanting to leave on exchange.
    """

    def __init__(self, expaToken, additionalIDs=None):
        """
        Initializes de Database

        :param expaToken: access token provided by Expa for AIESEC members
        :param additionalIDs: List of IDs of people who have to be added to Trello and are not in the wanted period
        """

        self.expa = ExpaService(expaToken)
        self.trello = TrelloService()
        self.peopleExpa = []
        self.peopleTrello = []
        self.additionalIDs = additionalIDs

    def get(self):
        """
        Get's all information concerning people

        :return: a list of (Person)s
        """

        # get all people from both platforms
        self.peopleExpa = self.expa.getNonMemberPeople()
        self.peopleTrello = self.trello.getAllPeople()

        # get all additional people using their specific EXPA IDs
        if self.additionalIDs is not None:
            for personId in self.additionalIDs:
                self.peopleExpa.append(self.expa.getPerson(personId))

        # update people objects
        names = [person['name'].encode('utf-8').strip() for person in self.peopleTrello]
        for person in self.peopleExpa:
            if person.name in names:
                person.trello = True

        self.displayStatus()
        self.displayUpdate()

    def displayStatus(self):

        print("\n ===== DATABASE COUNT ===== {} SIGN UPS: \n".format(len(self.peopleExpa)))

        for person in self.peopleExpa:
            print(person)

    def displayUpdate(self):

        toPush = [person for person in self.peopleExpa if person.trello == False]

        print("\n ===== TRELLO UPDATE ===== {} people will be added to Trello :\n".format(len(toPush)))
        print(toPush)

    def push(self):
        """
        Pushes people to Trello that are not yet on Trello
        """

        self.trello.postNewPeople(self.peopleExpa)


    def moveFromAssigned(self):
        """
        Move people from assigned list to mail sent list
        Sends the users a mail
        """

        ogxMembers = []
        matchedOgxIndices = []

        # get all members on Trello -> should be OGX
        trelloMembers = self.trello.getAllMembers()
        # get all teams on EXPA
        expaTeams = self.expaService.getCurrentTeams()["data"]

        for team in expaTeams:
            if "outgoing" in team["title"].lower():
                # we found OGX
                # get member info from EXPA
                expaMembers = self.expaService.getTeamMembers(team["id"])["data"]
                # get person info from EXPA
                expaMembersPeople = [ self.expaService.getPerson(m["person"]["id"]) for m in expaMembers ]

                # build Person objects
                ogx = [ ExpaService.jsonToMember(expaMembers[i], expaMembersPeople[i]) for i in range(len(expaMembers)) ]
                expaMembersNames = [ person.name.lower() for person in ogx ]

                for mTrello in trelloMembers:
                    # we're trying to find the EXPA member whose name matches that of a Trello member
                    query = mTrello["fullName"].lower()
                    match = process.extractOne(query, expaMembersNames) # (name, score)

                    if match[1] > 90:
                        idx = expaMembersNames.index(match[0])
                        if idx not in matchedOgxIndices:
                            # Trello member has not been linked to EXPA member yet
                            matchedOgxIndices.append(idx)

                            # add info to EXPA member
                            ogx[idx].trelloId = mTrello["id"]
                            ogx[idx].trello = True

                            ogxMembers.append(ogx[idx])
                        else:
                            # Trello member is matched to EXPA user that was already linked
                            print("Error: duplicate match for Trello user {}".format(mTrello["fullName"]))

                    else:
                        # No name match found between Trello member and EXPA members
                        print("No EXPA match for Trello user {}".format(mTrello["fullName"]))

                break

        # get cards in assigned list
        cards = self.trello.getCardsFromList(self.trello.listAssignedId)
        for card in cards:
            # members assigned to card
            cardMembers = card["idMembers"]
            if not cardMembers:
                continue

            # assigned member is first member (in case there are more than 1)
            memberId = cardMembers[0]
            for member in ogxMembers:
                if member.trelloId == memberId:
                    # useful email attributes
                    email_from = "info.lausanne@aiesec.ch"
                    email_reply_to = member.aiesec_email
                    email_reply_to_name = member.name
                    email_reply_to_phone = member.phone

                    # extract data from card description
                    data = { "name": card["name"] }
                    for info in card["desc"].split("\n"):
                        split = info.split(":")
                        data[split[0].strip().lower()] = split[1].strip()

                    # more useful email attributes
                    name_to = card["name"]
                    first_name_to = name_to.split(" ")[0]
                    email_to = data["email"]

                    print(f"Sending email to {name_to} <{email_to}>")

                    # build email body
                    body = f"""<!doctype HTML><html><head></head><body><p>Hello {first_name_to},<br/>
Je m’appelle {member.first_name}, je suis membre du comité AIESEC Lausanne. Je me permets de t’écrire suite à ton passage à notre stand à l’amphimax ce mercredi!
Comme tu le sais on organise de stages de volontariat ainsi que des stages professionnels à travers le monde entier, je suis là pour répondre à tes questions et te conseiller pour trouver le stage idéal pour toi. Nos partenaires en ce moment incluent Costa Rica, Vietnam, Egypte, Turquie, Argentine, Kenya, Uganda, Mexique, Pérou, Inde, et Colombie !
Je t’invite à t’inscrire sur notre site internet (<a href="https://aiesec.ch" target="_blank">aiesec.ch</a>) et à m’envoyer un message au <a href="tel:{email_reply_to_phone}">{email_reply_to_phone}</a>. Ce serait super qu’on fixe un rendez-vous afin de pouvoir en discuter.<br/>
Salutations,
{email_reply_to_name}</p></body></html>"""

                    # send email
                    yag = yagmail.SMTP(user="info.lausanne@aiesec.ch",password="Executiveboard1920")
                    yag.send(
                        to=email_to,
                        subject="Bienvenue | AIESEC",
                        contents=body,
                        headers={"Reply-To": f"{email_reply_to_name} <{email_reply_to}>"}
                    )

                    # move card to next list
                    self.trello.moveCardToList(card["id"], self.trello.listFirstEmailSent)
