#!/usr/bin/env python
# -*- coding:utf-8 -*-
from saltwrapper import *

if __name__ == "__main__":
    user = user_session()
    user.set_auth_token()
    print user.auth_token
    print str(get_minions(user.auth_token)).replace("u\"","\"").replace("u\'","\'")