#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# author:   kahsolt
# date:     2017-08-17

import requests

from Miranda.settings import *


def post_id(id):
    if not isinstance(id, str):
        return None

    try:
        resp = requests.get('%s%s' % (SEND_URL, id))
        print '[Messager] send id %s, and resp is "%s"' % (id, resp.content)
        return True
    except:
        return False


def get_mode():
    mode = None
    try:
        mode = int(requests.get(MODE_URL).text)
    except:
        print('[Messager] Server crashed... X(')
    return mode