#Use to display the Report like sherlock does
import termcolor

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
        def __init__(self, firstName, lastName, phoneNumber, email, username, address, zipCode, domain, ip):

    #add function to save to db, do a report, display report
