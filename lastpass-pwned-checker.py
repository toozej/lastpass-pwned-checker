#!/usr/bin/env python
# coding: utf-8
import json
import os
from lastpass import (
    Vault,
    LastPassIncorrectYubikeyPasswordError,
    LastPassIncorrectGoogleAuthenticatorCodeError
)

with open(os.path.join(os.path.dirname(__file__), 'credentials.json')) as f:
    credentials = json.load(f)
    username = str(credentials['username'])
    password = str(credentials['password'])

try:
    # First try without a multifactor password
    vault = Vault.open_remote(username, password)
except LastPassIncorrectGoogleAuthenticatorCodeError as e:
    # Get the code
    multifactor_password = input('Enter Google Authenticator code:')

    # And now retry with the code
    vault = Vault.open_remote(username, password, multifactor_password)
except LastPassIncorrectYubikeyPasswordError as e:
    # Get the code
    multifactor_password = input('Enter Yubikey password:')

    # And now retry with the code
    vault = Vault.open_remote(username, password, multifactor_password)

# open a list of newline separated pwned site URLs from a textfile into a []
with open(os.path.join(os.path.dirname(__file__), 'pwned_list.txt')) as f:
    pwned_sites = f.read().splitlines()

print("The following sites might be pwned, you should investigate: \n")

# cycle through the accounts in the LastPass vault and compare to pwned sites
for index, i in enumerate(vault.accounts):
    try:
        # if it's there, remove http[s]:// from the site name in lastpass
        domain_name = (i.url).split("://")[1]
    except IndexError:
        # if there's no http[s]:// infront of the site name, set it as is
        domain_name = i.url
    for site in pwned_sites:
        if site in domain_name:
            print("{}".format(i.url))


