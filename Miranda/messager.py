#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# author:   kahsolt
# date:     2017-08-17

import pycurl, io
# import requests # This may NOT work!!

from Miranda.settings import *


def curl(abs_url, method = "GET", data = ''):
    try:
        s = io.BytesIO()
        c = pycurl.Curl()
        if method == "GET":
            # print("[%s] %s ?%s" % (method, abs_url, data))
            c.setopt(pycurl.URL, '%s?%s' % (abs_url, data))
        c.setopt(pycurl.TIMEOUT, 30)
        c.setopt(pycurl.CONNECTTIMEOUT, 30)
        c.setopt(pycurl.CUSTOMREQUEST, method)
        c.setopt(pycurl.WRITEFUNCTION, s.write)
        c.perform()
        c.close()
        return s.getvalue().decode('utf8') + '\n'
    except Exception as e:
        print(e)
        return '<Error>'


def get_mode():
    mode = None
    try:
        mode = curl(abs_url=MODE_URL).strip(' \n\r\0')
        # mode = requests.get(MODE_URL).text
    except:
        print('[Messager] Server crashed... X(')
    return mode


def post_id(id):
    if not isinstance(id, str):
        return None

    try:
        resp = curl(abs_url=SEND_URL, data='stuNum=%s' % id).strip(' \n\r\0')
        # resp = requests.get(SEND_URL, params={'stuNum': id})
        print '[Messager] send id %s, and resp is "%s"' % (id, resp)
        return True
    except:
        return False

