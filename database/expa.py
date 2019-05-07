#!/usr/bin/python
# -- coding: utf-8 --

from person import Person
import datetime
import urllib
import json

class Expa:
    """ Information relative to a person wanting to leave on exchange.
    """

    def __init__(self, token):
        """
        Initialises the person
        """

        self.token = token

    @staticmethod
    def expa_dater(day, month, year):       # function making the conversion to the date format wanted in the expa URL
        return day + "%2F" + month + "%2F" + year

    @staticmethod
    def trello_dater(date):  # function converting date from YYYY-MM-DD to MM/DD/YYYY

        if date == None:  # to avoid working on Nonetype objects (split, reverse, etc.)
            return None

        newdate = date.split("-")  # removes '-' from string and creates list of strings of numbers
        newdate.reverse()  # reverses do ['DD','MM','YYYY'] format

        return newdate[1] + '/' + newdate[0] + '/' + newdate[2]  # Trello uses american date formatting


    def get_url(self):        # function creating the URL to pull SIGN UP data - following the GIS AIESEC EXPA API guidelins

        # today's date
        d = datetime.datetime.today()
        # converted into ['MM', 'DD', 'YYYY'] format that our lambda function loves
        end_date = [d.strftime('%d'), d.strftime('%m'), d.strftime('%Y')]

        url1 = "https://gis-api.aiesec.org/v2/people?access_token="
        start_date = ['01', '02', '2019']
        url2 = '&page=1&per_page=400&filters[registered]%5Bfrom%5D=' + Expa.expa_dater(*start_date) +\
               '&filters[registered]%5Bto%5D=' + Expa.expa_dater(*end_date) + '&filters[is_aiesecer]=false'
        final_url = url1 + self.token + url2

        return  final_url


    def get_data(self):        # function pulling the datas from the GIS AIESEC EXPA API and creating a list of people

        # pull data from URL
        fp = urllib.urlopen(self.get_url())
        mybytes = fp.read()

        data = mybytes.decode("utf8")
        fp.close()

        print(data)

        # converting the JSON file to a readable python dictionary
        datastore = json.loads(data)

        print(datastore)

        # make database
        people = []

        for i in range(len(datastore['data'])):
            if datastore['data'][i]['first_name'] == 'deleted':  # We skip people who have been deleted
                continue
            name = datastore['data'][i]['first_name'] + ' ' + datastore['data'][i]['last_name'] #We care about the full name
            id = datastore['data'][i]['id']
            email = datastore['data'][i]['email']
            dob = Expa.trello_dater(datastore['data'][i]['dob'])  # dated in trello format

            if dob == None:  # can't give None as argument to Trello API - needs str
                dob = 'N/A'

            cc = datastore['data'][i]['country_code']
            p = datastore['data'][i]['phone']

            if cc == None or not isinstance(cc, str):  # same logic as for DOB
                if p == None or not isinstance(p, str):
                    phone = 'N/A'
                else:
                    phone = p
            else:
                if cc in p[0:4]:
                    phone = p
                else:
                    phone = cc + p

            sud = Expa.trello_dater(datastore['data'][i]['created_at'][0:10])
            if sud == None:
                sud = 'N/A'
            link = "https://expa.aiesec.org/people/" + str(id)  # link to person on expa for retrieving additional info

            status = datastore['data'][i]['status']

            # adds manager only if this is NOT Daniella (VP OGX) (she is appointed automatically )
            managers = []
            for member in datastore['data'][i]['managers']:
                managers.append(str(member['id']))

            people.append(Person(name, id, email, dob, phone, sud, link, status, managers))  # adds person to people list



        print("DATABASE COUNT :::: " + str(len(people)) + " SIGN UPS SINCE FEB 1 2019")


        for x in range(len(people)):
            print people[x],

        return people


    def get(self, ):
       """
       Get's all information from Expa
       :return:
       """
       pass


