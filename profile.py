#Use to display the Report like sherlock does
import termcolor
import json
import requests

class Profile:
    # check username with login list json, hash password to check if it matches
    def __init__(self, firstName, lastName, phoneNumber, email, username, address, zipCode, domain, ip):
        #Make sure to add that if a value is set to None, don't try to send it through the api's
        self.name = (firstName, lastName)
        self.phoneNumber = phoneNumber
        self.email = email
        self.username = username
        #Might need to change address into a tuple or array with street, zip code, city, state, etc.
        self.address = address
        #Might be depricated for address tuple/array
        self.zipCode = zipCode
        self.domain = domain
        self.ip = ip
    class Report:
        def __init__(self, name, phoneNumber, email, username, address, zipCode, domain, ip):
            self.name = (firstName, lastName)
            self.phoneNumber = phoneNumber
            self.email = email
            self.username = username
            self.address = address
            self.zipCode = zipCode
            self.domain = domain
            self.ip = ip
            self.report = 
            {
                "name": [],
                "phoneNumber": [],
                "email": [],
                "username": [],
                "address": [],
                "zipCode": [],
                "domain": [],
                "ip": [],
                "allOutput": []
            }
        
        def buildReport(self):
            #cycle through the api's and add to the report dictionary
            apiList = json.loads("url_query.json")
            for x in apiList["PhoneNumber"]:
                termcolor
                split = x.split(";")
                numberAdded = split[0] + self.phoneNumber + split[1]
                output = request.get(numberAdded)
                self.report["allOutput"].append(output)
                #need to add more specific variables for report
                #for now just add the reigon of the phone number to the address
                self.report[""]
