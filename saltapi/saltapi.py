#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import requests

base_url = "http://127.0.0.1:5417"


class user_session:
    def __init__(self):
        '''
        Initializer. username:yliu password:FR332016$
        '''
        self.auth_token = None
        self.user_name = "yliu"
        self.password = "FR332016$"

    def set_auth_token(self, url=base_url):
        '''
        sets instance variable for auth_token that allows x-auth-token header
        authentication with salt-api. Optionally takes user_pass(str).
        '''
        url += '/login'
        data = {}
        data['username'] = self.user_name
        data['eauth'] = 'pam'
        data['password'] = self.password
        headers = {'accept':'application/json'}
        r = requests.post(url, headers=headers, data=data, verify=False)

        try:
            self.auth_token = r.json()["return"][0]["token"]
        except:
            print('Auth error.')


def cmd_run(password, user, target, cmd):
    '''
    Runs cmd.run from cmd parameter.
    Returns dict of results per minion.
    '''
    url = base_url + '/run'
    data = {}
    data['username'] = user
    data['tgt'] = target
    data['client'] = 'local'
    data['eauth'] = 'pam'
    data['password'] = password
    data['fun'] = 'cmd.run'
    data['arg'] = cmd

    r = requests.post(url, data=data, verify=False)

    if r.status_code != 200:
        return 'Status code ' + str(r.status_code) + ', something went wrong.\n'
    else:
        return r.json()['return'][0]


def token_cmd_run(auth_token, target, cmd):
    '''
    Runs cmd.run from state parameter. Returns dict of results per minion.
    '''
    headers = {'Accept': 'application/json', 'X-Auth-Token': auth_token}
    data = {'tgt': target, 'client': 'local', 'fun': 'cmd.run', 'arg': cmd}

    r = requests.post(base_url, headers=headers, data=data, verify=False)

    if r.status_code != 200:
        return 'Status code ' + str(r.status_code) + ', something went wrong.\n'
    else:
        return r.text


def print_cmd_run(cmd):
    '''
    prints returned dict from cmd_run function
    '''
    if type(cmd) == str or type(cmd) == unicode:
        print(cmd)
    else:
        for minion in cmd:
            print('*** ' + minion + ' ***\n')
            print(cmd[minion] + '\n')
            print('-' * 10 + '\n')


def get_minions(auth_token, url=base_url):
    '''
    returns dict of minions that were connected when function was run, uses
    x-auth-token header value for authentication.
    '''
    url += '/minions'
    headers = {'X-Auth-Token': auth_token, 'Accept': 'application/json'}
    r = requests.get(url, headers=headers, verify=False)
    minions = r.json()['return'][0]
    return minions

def print_minions(minions):
    '''
    prints dict of minions from get_minions function.
    '''
    print('Registered minions:\n')
    for minion in minions:
        print('* ' + minion)
        print('  Kernel release: ' + minions[minion]['kernelrelease'])
    print('-' * 10 + '\n')

def token_run_state(auth_token, target, state, url=base_url):
    '''
    runs a state.sls where target is the path to the state. pillar can be a
    string in the form of pillar='pillar={"value1": "string"}'.  returns dict with
    return information from the salt-api about the states run from the state file
    specified.
    '''
    headers = {'Accept': 'application/json', 'X-Auth-Token': auth_token}
    data = {}
    data['tgt'] = target
    data['client'] = 'local'
    data['fun'] = 'state.sls'
    data['arg'] = [state]

    r = requests.post(url, headers=headers, data=data, verify=False)

    if r.status_code != 200:
        return 'Status code ' + str(r.status_code) + ', something went wrong.\n'
    else:
        return r.text


def print_run_state(state):
    '''
    prints dict from run_state function
    '''
    if type(state) == str or type(state) == unicode:
        print(state)
    else:
        for minion in state:
            print('*** ' + minion + ' ***\n')
            for item in state[minion]:
                try:
                    comment = state[minion][item]['comment']
                    result = str(state[minion][item]['result'])
                    print('State: ' + item)
                    print('Comment: ' + comment)
                    print('Result: ' + result + '\n')
                except:
                    print(state[minion][0] + '\n')


def test_target(auth_token, target, url=base_url):
    '''
    tests which minions will match a target expression
    '''
    headers = {'Accept': 'application/json', 'X-Auth-Token': auth_token}
    data = {'client': 'local', 'tgt': target, 'fun': 'test.ping'}
    r = requests.post(url, headers=headers, data=data, verify=False)
    return r.text
