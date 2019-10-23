#!/usr/bin/python
# -- coding: utf-8 --

from database.trello import TrelloService
from database.expa import ExpaService
from database.email import Email
from fuzzywuzzy import process
from unidecode import unidecode

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

    @staticmethod
    def effify(non_f_str: str):
        return eval(f'f"""{non_f_str}"""')


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
                self.peopleExpa.append(self.expa.getNonMemberPerson(personId))

        # update people objects
        names = [person['name'].strip() for person in self.peopleTrello]
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
        expaTeams = self.expa.getCurrentTeams()["data"]

        for team in expaTeams:
            if "outgoing" in team["title"].lower():
                # we found OGX
                # get member info from EXPA
                expaMembers = self.expa.getTeamMembers(team["id"])["data"]
                # get person info from EXPA
                expaMembersPeople = [ self.expa.getMember(m["person"]["id"]) for m in expaMembers ]

                # build Person objects
                ogx = [ ExpaService.jsonToMember(expaMembers[i], expaMembersPeople[i]) for i in range(len(expaMembers)) ]
                expaMembersNames = [ unidecode(person.name.lower()) for person in ogx ]

                for mTrello in trelloMembers:
                    # we're trying to find the EXPA member whose name matches that of a Trello member
                    query = unidecode(mTrello["fullName"].lower())
                    match = process.extractOne(query, expaMembersNames) # (name, score)

                    if match[1] > 80:
                        idx = expaMembersNames.index(match[0])
                        if idx not in matchedOgxIndices:
                            print(f"[ok] Matched Trello user {mTrello['fullName']} with EXPA user {ogx[idx].name}")

                            # Trello member has not been linked to EXPA member yet
                            matchedOgxIndices.append(idx)

                            # add info to EXPA member
                            ogx[idx].trelloId = mTrello["id"]
                            ogx[idx].trello = True

                            ogxMembers.append(ogx[idx])
                        else:
                            # Trello member is matched to EXPA user that was already linked
                            print("[error] Error: duplicate match for Trello user {}".format(mTrello["fullName"]))

                    else:
                        # No name match found between Trello member and EXPA members
                        print("[warning] No EXPA match for Trello user {}".format(mTrello["fullName"]))

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
                    # extract data from card description
                    to = {
                        "first_name": card["name"].split(" ")[0],
                        "name": card["name"]
                    }
                    for info in card["desc"].split("\n"):
                        split = info.split(":")
                        to[split[0].strip().lower()] = split[1].strip()

                    # email subject
                    subject = "Bienvenue | AIESEC"

                    # email headers
                    headers = {
                        "Reply-To": f"{member.name} <{member.aiesec_email}>"
                    }

                    # info
                    print(f"Sending email to {card['name']} <{to['email']}>")
                    email = Email(template="templates/ogxbooth.html")
                    email.send(member, to, subject, headers)

                    # move card to next list
                    self.trello.moveCardToList(card["id"], self.trello.listFirstEmailSent)
