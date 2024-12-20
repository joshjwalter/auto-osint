import requests
import json
import cryptography




def login():
    password = input("Password: ")
    if password == "7933":
        main()
    else:
        print("Password incorrect, try again")
        login()

def main():
    print("""
  ___        _              _____ _____ _____ _   _ _____ 
 / _ \      | |            |  _  /  ___|_   _| \ | |_   _|
/ /_\ \_   _| |_ ___ ______| | | \ `--.  | | |  \| | | |  
|  _  | | | | __/ _ \______| | | |`--. \ | | | . ` | | |  
| | | | |_| | || (_) |     \ \_/ /\__/ /_| |_| |\  | | |  
\_| |_/\__,_|\__\___/       \___/\____/ \___/\_| \_/ \_/  
     By Joshua Walter                                                     
                                                          
    """)    
    mode = input("Which mode would you like to use:\n1) New Report\n2) Continue Report\n 3) View Finished Reports\n 4) Custom Search")
#    match mode:
#        case "1":
            # ask for email phone number etc.
            # consider making a class/object
            # profile = buildProfile()
            # use the info from build profile to make report
            # report() maybe add this function to a seperate file

