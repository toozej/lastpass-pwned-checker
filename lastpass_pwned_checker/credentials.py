#!/usr/bin/env python
''' Module for safely obtaining LastPass credentials
'''
import os
import json

class CredsError(Exception):
    ''' Custom error for credentials
    '''
    def __init__(self, *args, **kwargs):
        super(CredsError).__init__(self, *args, **kwargs)

class Credentials(object):
    ''' Simple class for obtaining credentials as safely as possible
    '''
    def __init__(self, creds_path=None):
        ''' Initialize object
        '''
        self._creds = creds_path
        self._user = None
        self._pass = None
    def get(self):
        ''' Get credentials from file or env vars
            Report errors in order of preference: file, envvar
        '''
        try:
            if self._creds:
                self.user, self.password = self._json_creds()
            else:
                self.user, self.password = self._env_creds()
            return self.user, self.password
        except KeyError:
            raise CredsError('Credentials file is missing necessary key/value \
pairs.')
        except IOError:
            raise CredsError('Unable to read credentials file.')
    @property
    def user(self):
        ''' Propertize password
        '''
        return self._user
    @user.setter
    def user(self, usr):
        ''' Allow property to be set
        '''
        self._user = usr
        return self._user
    @property
    def password(self):
        ''' Propertize password
        '''
        return self._pass
    @password.setter
    def password(self, pswd):
        ''' Allow property to be set
        '''
        self._pass = pswd
        return self._pass
    def _json_creds(self):
        ''' Get credentials from json file
        '''
        with open(self._creds) as data:
            creds = json.loads(data.read())
        return creds['username'], creds['password']
    @staticmethod
    def _env_creds():
        ''' Get credentials from env vars
        '''
        user = os.environ.get('LPPC_USER')
        password = os.environ.get('LPPC_PASS')
        if not user and password:
            raise CredsError('No credentials file given and environment \
variables unset.')
        return user, password
