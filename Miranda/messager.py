#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# author:   kahsolt
# date:     2017-08-17

import requests

from Miranda.settings import *


def get_mode():
    mode = None
    try:
        mode = requests.get(MODE_URL).text
    except:
        print('[Messager] Server crashed... X(')
    return mode


def post_id(id):
    if not isinstance(id, str):
        return None

    try:
        resp = requests.get(SEND_URL, data={'stuNum': id})
        print '[Messager] send id %s, and resp is "%s"' % (id, resp.content)
        return True
    except:
        return False
