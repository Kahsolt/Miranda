#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# author:   kahsolt
# date:     2017-08-17

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from Miranda.settings import *

app = Flask(__name__)

MODE = MODE_NORMAL

@app.route("/mode/<string:mode>")
def mode(mode):
    global MODE
    if mode in [MODE_NORMAL, MODE_IDEL, MODE_COLLECT]:
        MODE = mode
    return MODE


@app.route("/id/<string:id>")
def id(id):
    return 'Acknowledged id: %s :)' % (id)


if __name__ == "__main__":
   app.run(debug=True)