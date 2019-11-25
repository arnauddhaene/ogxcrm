#!/usr/bin/python
# -- coding: utf-8 --

import datetime
import time
import xlwt
from database.person import Person
from database.apiService import ApiService

from xlutils.copy import copy
from xlrd import open_workbook

class ExpaService(ApiService):
    """
    API service for AIESEC resources
    """

    def __init__(self, token):
        """
        :param token: AIESEC expa token
        """

        baseUrl = "https://gis-api.aiesec.org/v2"
        params = { "access_token": token }

        super().__init__(baseUrl, params)

        # Init some useful constants
        self.mc_id = 1558
        self.city_id = 6104
        self.committee_id = 869
        self.term_19_20_id = 10783

        self.members = []
        self.nonmembers = []

    @staticmethod
    def toExpaDate(day, month, year):
        """
        Returns a date in the format wanted by the EXPA API
        """

        return day + "%2F" + month + "%2F" + year

    @staticmethod
    def toTrelloDate(date):
        """
        Converts date from YYYY-MM-DD to MM/DD/YYYY (Trello format)
        """

        # safety check
        if date is None:
            return None

        # split date into ['YYYY', 'MM', 'DD']
        pieces = date.split("-")
        # shift first value ('YYYY') to last position
        # pieces is now ['MM', 'DD', 'YYYY']
        pieces.insert(2, pieces.pop(0))

        return "/".join(pieces)

    @staticmethod
    def jsonToPerson(json):
        """
        Converts a json response into a Person object

        :param json: JSON representation from API
        :returns: a Person object
        """

        if json['first_name'] == 'deleted':
            # we skip people who have been deleted
            return None

        # validate a given country code and phone number
        # cc or phone might be None
        def jsonToPhone(cc, p):
            phone = ""
            if cc:
                phone = cc
            if p:
                phone += p

            if not phone:
                return 'N/A'
            else:
                return phone

        # build person
        person = {
            # expa id
            'id'                : json['id'],
            # first name
            "first_name"        : json["first_name"],
            # name
            'name'              : json['full_name'],
            # email
            'email'             : json['email'],
            # date of birth
            'dob'               : ExpaService.toTrelloDate(json['dob']) or 'N/A',
            # phone
            'phone'             : jsonToPhone(json['country_code'], json['phone']),
            # sign-up date
            'sud'               : ExpaService.toTrelloDate(json['created_at'][0:10]) or 'N/A',
            # expa link
            'link'              : f"https://expa.aiesec.org/people/{id}",
            # status
            'status'            : json['status'],
            # managers
            'managers'          : [str(member['id']) for member in json['managers']]
        }

        return Person(**person)

    @staticmethod
    def jsonToMember(member, person):
        """
        Converts a member into a Person object

        :param member: JSON representation of member from API
        :param person: Person object of person from API
        :returns: a Person object
        """

        if member['person']['first_name'] == 'deleted' or person.first_name == 'deleted':
            # we skip people who have been deleted
            return None

        member = {
            # expa id
            "id"                : member["id"],
            # first name
            "first_name"        : member["person"]["first_name"],
            # full name
            "name"              : member["person"]["full_name"],
            # EXPA email address
            "email"             : member["person"]["email"],
            # AIESEC email address
            "aiesec_email"      : member["person"]["aiesec_email"],
            # date of birth
            "dob"               : member["person"]["dob"],
            # phone number
            "phone"             : person.phone,
            # date they joined AIESEC
            "sud"               : ExpaService.toTrelloDate(member["created_at"][0:10]),
            # URL to expa profile
            "link"              : "https://expa.aiesec.org/people/{}".format(member["id"]),
            # status
            'status'            : person.status,
            # team name
            "team"              : member["team"]["title"],
            # role within their team, e.g., VP or Member
            "role"              : member["role"],
            # name of their role, e.g., Data Analyst
            "role_name"         : member["name"]
        }

        return Person(**member)

    def getNonMemberPeople(self):
        """
        Get all people from EXPA API that are not members
        """

        if not self.nonmembers:
            # generate params for API
            d = datetime.datetime.today()
            start_date = ExpaService.toExpaDate('01', '02', '2019') # first use of this tool
            end_date = ExpaService.toExpaDate(d.strftime('%d'), d.strftime('%m'), d.strftime('%Y'))

            # define endpoint and params
            url = "/people"
            params = {
                "page": 1,
                "per_page": 20,
                "filters[registered][from]": start_date,
                "filters[registered][to]": end_date,
                "filters[is_aiesecer]": "false"
            }

            # load first page of results
            result = self.get(url, params)
            nPages = result["paging"]["total_pages"]
            print(f"There are {nPages} pages, totalling {nPages * 20} people")


            # fill people array with first values
            people = result["data"]
            if nPages > 1:
                # get other pages
                for page in range(2, nPages + 1):
                    print(f"Loading page {page}")
                    params["page"] = page
                    response = self.get(url, params)
                    people.extend(response["data"])

            # make objects
            peopleObjs = []
            for json in people:
                # convert JSON to object
                person = self.jsonToPerson(json)
                if person:
                    peopleObjs.append(person)

            self.nonmembers = peopleObjs

        return self.nonmembers

    def getNonMemberPerson(self, personId):
        """
        Get a specific person's data from the EXPA API using his EXPA ID

        :param personId: the person's id
        :return: a Person object of that person
        """

        if not self.nonmembers:
            self.getNonMemberPeople()

        for person in self.nonmembers:
            if person.id == personId:
                return person

        return None

    def getAllMembers(self):
        """
        Get all people from EXPA API that are members
        """

        if not self.members:

            # define endpoint and params
            url = "/people"
            params = {
                "page": 1,
                "filters[is_aiesecer]": "true"
            }

            # load first page of results
            result = self.get(url, params)
            nPages = result["paging"]["total_pages"]

            # fill people array with first values
            members = result["data"]
            if nPages > 1:
                # get other pages
                for page in range(2, nPages + 1):
                    params["page"] = page
                    members.extend(self.get(url, params)["data"])

            # make objects
            memberObjs = []
            for json in members:
                # convert JSON to object
                person = self.jsonToPerson(json)
                if person:
                    memberObjs.append(person)

            self.members = memberObjs

        return self.members

    def getMember(self, personId):
        """
        Get a specific member's data from the EXPA API using his EXPA ID

        :param personId: the person's id
        :return: a Person object of that person
        """

        if not self.members:
            self.getAllMembers()

        for person in self.members:
            if person.id == personId:
                return person

        return None

    def getCommittee(self, committee_id):
        return self.get("/committees/{}".format(committee_id))
    def getCurrentCommittee(self):
        return self.getCommittee(self.committee_id)

    def getTerms(self, committee_id):
        return self.get("/committees/{}/terms".format(committee_id))
    def getCurrentTerms(self):
        return self.getTerms(self.committee_id)

    def getCities(self, mc_id):
        return self.get("/cities", { "filters[mc_id]": mc_id })
    def getSwissCities(self):
        return self.getCities(self.mc_id)

    def getCommitteeMembers(self, committee_id, term_id):
        return self.get("/committees/{}/terms/{}/members".format(committee_id, term_id))
    def getCurrentCommitteeMembers(self):
        return self.getCommitteeMembers(self.committee_id, self.term_19_20_id)

    def getTeams(self, committee_id, term_id):
        return self.get("/committees/{}/terms/{}/teams".format(committee_id, term_id))
    def getCurrentTeams(self):
        return self.getTeams(self.committee_id, self.term_19_20_id)

    def getTeamMembers(self, team_id):
        return self.get("/teams/{}/positions".format(team_id))

    def getAllCurrentMembers(self, verbose=False):
        """
        Get all current members
        """

        ids = []
        members = []

        # get all current teams
        if verbose: print("Fetching teams\n")
        teams = self.getCurrentTeams()["data"]

        for team in teams:
            # get team members
            if verbose: print("Fetching members of team {}".format(team["title"]) + "\n================================")
            ms = self.getTeamMembers(team["id"])["data"]

            for m in ms:
                id = m["person"]["id"]
                if id in ids:
                    # EB members appear twice so we skip them if we've already processed them
                    if verbose: print("Duplicate person {}".format(m["person"]["full_name"]))
                    continue
                else:
                    ids.append(id)

                # get person obj for more info
                if verbose: print("Fetching info on {}".format(m["person"]["full_name"]))
                person = self.getMember(id)

                members.append(self.jsonToMember(m, person))

            if verbose: print("\n")

        return members

    def exportAllMembers(self, filename):
        headers = ["value", "email", "aiesec_email", "phone"]
        members = self.getAllMembers()
        memberIds = [ m.id for m in members ]
        comm = []

        # get all committee people
        terms = self.getTerms(self.committee_id)["data"]
        for term in terms:
            termId = term["id"]
            committee = self.getCommitteeMembers(self.committee_id, termId)["data"]
            comm.extend(committee)

        # only keep unique people
        # and add phone number
        members_clean = []
        ids_clean = []
        for person in comm:
            if person["id"] not in ids_clean:
                for member in members:
                    if person["id"] == member.id:
                        person["phone"] = member.phone
                members_clean.append(person)
                ids_clean.append(person["id"])

        self.toExcel(filename, headers, members_clean)

    def getEBSWorlwide(self):

        def is_token_valid(call, *args, tries=3):
            response = call(*args)
            if hasattr(response, "ok"):
                if not response.ok:
                    print(f"Error code {response.status_code}")
                    if response.status_code == 500 or response.status_code == 504:
                        time.sleep(2)
                        # timeout
                        if tries > 0:
                            return is_token_valid(call, *args, tries = tries-1)
                        else:
                            return { "data" : [] }
                    else:
                        # token expired
                        token = input("Enter new token: ")
                        self.set_params({ "access_token": token })
                        if tries > 0:
                            return is_token_valid(call, *args, tries = tries-1)
                        else:
                            return { "data" : [] }

            return response

        book_ro = open_workbook("lcs_eb_worldwide.xls")
        book = copy(book_ro)  # creates a writeable copy
        sheet = book.get_sheet(0)  # get a first sheet

        headers = [ "id", "first_name", "last_name", "full_name", "email", "aiesec_email", "role", "lc", "country" ]
        row_offset = 7818
        lcs_offset = 667

        # get all lcs
        # format is { "id": ..., "lc_id": ..., "city_id": ... }
        lcs = self.get("/city_lcs")
        n = len(lcs)
        for i, lc in enumerate(lcs):
            if i < lcs_offset:
                continue

            lc_id = lc["lc_id"]
            committee = is_token_valid(self.getCommittee, lc_id)
            if not "name" in committee:
                print("Skipping...")
                continue

            print(f"[{i+1}/{n}] Getting infos of LC {committee['name']}")

            terms = committee["terms"]
            last_term = terms[len(terms) - 1]

            print(f"Term: {last_term['short_name']}")

            teams = is_token_valid(self.getTeams, lc_id, last_term["id"])
            for team in teams["data"]:
                if team["title"] == "EB" or team["team_type"] == "eb":
                    # we found the eb
                    members = is_token_valid(self.getTeamMembers, team["id"])

                    for member in members["data"]:
                        person = {
                            'id'            : member["person"]["id"],
                            'first_name'    : member["person"]["first_name"],
                            'last_name'     : member["person"]["last_name"],
                            'full_name'     : member["person"]["full_name"],
                            'email'         : member["person"]["email"],
                            'aiesec_email'  : member["person"]["aiesec_email"],
                            'role'          : member["name"],
                            'lc'            : committee["name"],
                            'country'       : committee["country"]
                        }

                        for j in range(len(headers)):
                            key = headers[j]
                            sheet.write(row_offset, j, person[key] or " ")

                        row_offset += 1

                    book.save("lcs_eb_worldwide.xls")
                    print(f"Added {len(members['data'])} people")
                    print(f"Row offset: {row_offset}")

            print("")

    def getAndExportCurrentMembers(self, filename, verbose=False):
        headers = ["name", "sud", "team", "role", "performance", "link", "LDA", "email", "aiesec_email", "secondary_email", "phone", "dob", "university", "study_area", "study_year", "IXP"]
        members = self.getAllCurrentMembers(verbose=verbose)
        self.toExcel(filename, headers, members)

    def toExcel(self, filename, headers, data):
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet("Sheet 1")

        for j in range(len(headers)):
            key = headers[j]
            sheet.write(0, j, key) # write key as column title
            for i in range(len(data)):
                if isinstance(data[i], Person):
                    if hasattr(data[i], key):
                        sheet.write(i+1, j, getattr(data[i], key) or " ")
                    else:
                        sheet.write(i+1, j, " ")
                elif key in data[i]:
                    sheet.write(i+1, j, data[i][key] or " ")
                else:
                    sheet.write(i+1, j, " ")

        book.save(filename)
