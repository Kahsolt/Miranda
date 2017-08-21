#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# author:   kahsolt
# date:     2017-08-17

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, redirect, url_for
from Miranda.settings import *

app = Flask(__name__)

MODE = MODE_NORMAL


@app.route("/teahcer/signIn/state", methods=['GET'])
def mode():
    global MODE

    mode = request.args.get('mode')
    if mode in [MODE_NORMAL, MODE_IDEL, MODE_COLLECT]:
        MODE = mode
        return redirect(url_for('index'))
    else:
        return MODE


@app.route("/teacher/signIn/input", methods=['GET'])
def id():
    sid = request.args.get('stuNum')
    if sid:
        return 'Student %s signed in successfully!' % sid
    return 'Wrong param..'


@app.route("/")
def index():
    global MODE
    html = '<h3>Current mode: <span style="color: red;">%s<span> </h3>' % MODE
    html += '<hr/>'
    html += MODE != MODE_IDEL \
            and '<p><a href="/teahcer/signIn/state?mode=free">Switch to Free mode</a></p>' \
            or '<p>Switch to Free mode</p>'
    html += MODE != MODE_NORMAL \
            and '<p><a href="/teahcer/signIn/state?mode=signIn">Switch to SignIn mode</a></p>' \
            or '<p>Switch to SignIn mode</p>'
    html += MODE != MODE_COLLECT \
            and '<p><a href="/teahcer/signIn/state?mode=enter">Switch to Enter mode</a></p>' \
            or '<p>Switch to Enter mode</p>'
    return html


if __name__ == "__main__":
   app.run(debug=True)

