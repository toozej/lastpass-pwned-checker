#!/usr/bin/env python
''' Module for checking LastPass account against list of suspected-pwned sites
'''
from lastpass import (
    Vault,
    LastPassIncorrectYubikeyPasswordError,
    LastPassIncorrectGoogleAuthenticatorCodeError
)

class Checker(Vault):
    ''' Polymorph of Vault to give it site-checking features
    '''
    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self._sites = []
    @classmethod
    def safe_open(cls, user, password):
        ''' Create a class instance from credentials, taking MFA into
            consideration
        '''
        try:
            # First try without a multifactor password
            # pylint: disable=no-member
            vault = cls.open_remote(user, password)
        except LastPassIncorrectGoogleAuthenticatorCodeError:
            # Get the code
            multifactor_password = input('Enter Google Authenticator code:')

            # And now retry with the code
            # pylint: disable=no-member
            vault = cls.open_remote(user, password, multifactor_password)
        except LastPassIncorrectYubikeyPasswordError:
            # Get the code
            multifactor_password = input('Enter Yubikey password:')
            # And now retry with the code
            # pylint: disable=no-member
            vault = cls.open_remote(user, password, multifactor_password)
        return vault
    def compare_pwned(self, pwnd_sites):
        ''' Compare accounts to pwned sites list
        '''
        return [site
                for item in self.accounts
                for site in pwnd_sites
                if site in item.url]
