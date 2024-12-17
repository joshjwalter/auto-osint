import requests
import json
import cryptography

def login():
    username = input("Username: ")
    password = input("Password: ")
    # check username with login list json, hash password to check if it matches
