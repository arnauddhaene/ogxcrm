#!/usr/bin/python
# -- coding: utf-8 --

import requests
import json
from html.parser import HTMLParser
import xlwt

class ApiService:
    """
    API request handler
    """

    def __init__(self, baseUrl, params):
        """
        Initialises a service to access data from an API

        :param baseUrl: base URL for requests
        :param params: map of request arguments to include in every request
        """

        self.baseUrl = baseUrl
        self.params = params

    def get(self, url, params={}, toJson=True):
        """
        GET a resource

        :param url: endpoint of resource
        :param params: optional request arguments
        """

        # create endpoint URL
        endpoint = self.baseUrl + url
        # add base params to request parameters
        query = dict(self.params, **params)

        result = requests.get(endpoint, query)
        return result.json() if (result.ok and toJson) else result

    def put(self, url, body, params={}, toJson=True):
        """
        PUT a resource

        :param url: endpoint of resource
        :param body: resource to PUT
        :param params: optional request arguments
        """

        # create endpoint URL
        endpoint = self.baseUrl + url
        # add base params to request parameters
        query = dict(self.params, **params)

        result = requests.put(endpoint, data=body, params=query)
        return result.json() if (result.ok and toJson) else result

    def post(self, url, body, params={}, toJson=True):
        """
        POST a resource

        :param url: endpoint of resource
        :param body: resource to POST
        :param params: optional request arguments
        """

        # create endpoint URL
        endpoint = self.baseUrl + url
        # add base params to request parameters
        query = dict(self.params, **params)

        result = requests.post(endpoint, body, query)
        return result.json() if (result.ok and toJson) else result

class TrelloService(ApiService):
    """
    API service for Trello resources
    """

    def __init__(self):
        baseUrl = "https://api.trello.com/1"
        params = {
            "key": "448b14b4374aaa9429f4a8b979936e2b",
            "token": "9f9de4286e6a5f627f083dc3ca8fdf6dceae7307a06c5e9dcedda4212491a4e3"
        }

        super().__init__(baseUrl, params)


class ExpaService(ApiService):
    """
    API service for AIESEC resources
    """

    def __init__(self, token):
        """
        :param token: AIESEC expa token
        """

        baseUrl = "https://gis-api.aiesec.org/v2"
        params = {
            "access_token": token
        }

        super().__init__(baseUrl, params)

        # Init some useful constants
        self.mc_id = 1558
        self.city_id = 6104
        self.committee_id = 869
        self.term_19_20_id = 10783

        self.people = []

    def getPerson(self, person_id):
        if not self.people:
            people = self.getAllPeople(1)
            pages = people["paging"]["total_pages"]

            self.people = people["data"]

            for page in range(2, pages + 1):
                self.people.extend(self.getAllPeople(page)["data"])

        for person in self.people:
            if person["id"] == person_id:
                return person

        return None

    def getAllPeople(self, page):
        return self.get("/people", { "page": page, "filters[is_aiesecer]": "true" })

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
        ids = []
        members = []
        # get all current teams
        if verbose: print("Fetching teams\n")
        teams = self.getCurrentTeams()["data"]
        for team in teams:
            team_name = team["title"]

            # get team members
            if verbose: print("Fetching members of team {}".format(team_name) + "\n================================")
            ms = self.getTeamMembers(team["id"])["data"]
            for m in ms:
                id = m["person"]["id"]
                if id in ids:
                    # EB members appear twice so we skip them if we've already processed them
                    if verbose: print("Duplicate person {}".format(m["person"]["full_name"]))
                    continue

                ids.append(id)
                # get person obj for more info
                if verbose: print("Fetching info on {}".format(m["person"]["full_name"]))
                person = self.getPerson(id)
                # build phone number
                phone = ""
                if person:
                    if person["country_code"]:
                        phone = person["country_code"]
                    if person["phone"]:
                        phone += person["phone"]
                # build member object
                member = {
                    # expa id
                    "id":           id,
                    # full name
                    "full_name":    m["person"]["full_name"],
                    # date they joined AIESEC
                    "join_date":    m["created_at"],
                    # team name
                    "team":         team_name,
                    # role within their team, e.g., VP or Member
                    "role":         m["role"],
                    # name of their role, e.g., Data Analyst
                    "role_name":    m["name"],
                    # URL to expa profile
                    "expa_url":     "https://expa.aiesec.org/people/{}".format(id),
                    # EXPA email address
                    "expa_email":   m["person"]["email"],
                    # AIESEC email address
                    "aiesec_email": m["person"]["aiesec_email"],
                    # phone number
                    "phone":        phone,
                    # date of birth
                    "dob":          m["person"]["dob"]
                }

                members.append(member)

            if verbose: print("\n")

        return members

    def getAndExportCurrentMembers(self, filename, verbose=False):
        headers = ["full_name", "join_date", "team", "role", "performance", "expa_url", "LDA", "expa_email", "aiesec_email", "secondary_email", "phone", "dob", "university", "study_area", "study_year", "IXP"]
        members = self.getAllCurrentMembers(verbose=verbose)
        self.toExcel(filename, headers, members)

    def toExcel(self, filename, headers, data):
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet("Sheet 1")

        for j in range(len(headers)):
            key = headers[j]
            sheet.write(0, j, key) # write key as column title
            for i in range(len(data)):
                if key in data[i]:
                    sheet.write(i+1, j, data[i][key] or " ")
                else:
                    sheet.write(i+1, j, " ")

        book.save(filename)

class ExpaLoginService(ApiService):
    """
    Login service for communication with the EXPA server
    """

    def __init__(self):
        """
        Init class
        Very useful comment indeed
        """
        super().__init__("https://auth.aiesec.org", {})

    def sign_in(self, email, pwd):
        """
        Sign in the user

        :param username: expa username
        :param pwd: expa password
        """

        endpoint = "/users/sign_in"
        authenticity_token = self.get_authenticity_token()
        body = {
            "utf8": "✓",
            "authenticity_token": authenticity_token,
            "user[email]": email,
            "user[password]": pwd,
            "commit": "Log in"

        }

        return self.post(endpoint, body, toJson=False)

    def get_authenticity_token(self):

        # retrieve sign in page
        content = self.get("/users/sign_in", toJson=False).text

        # parse page
        class MyHTMLParser(HTMLParser):
            def __init__(self):
                # initialize the base class
                HTMLParser.__init__(self)
                self.authenticity_token = None

            def handle_starttag(self, tag, attrs):
                if tag == "meta":
                    for attr in attrs:
                        if attr[0] == "csrf-token":
                            self.authenticity_token = attr[1]
                            break

        parser = MyHTMLParser()
        parser.feed(content)

        return parser.authenticity_token
