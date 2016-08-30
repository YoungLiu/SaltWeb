#!/usr/bin/env python
# -*- coding:utf-8 -*-
from saltapi import *

if __name__ == "__main__":
    user = user_session()
    user.set_auth_token()
    print user.auth_token
    print test_target(user.auth_token, "*")