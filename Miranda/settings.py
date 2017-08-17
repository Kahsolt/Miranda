#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# author:   kahsolt
# date:     2017-08-17

import os

# Paths
MIRANDA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES_PATH = os.path.join(MIRANDA_BASE, 'res')
PHOTO_PATH = os.path.join(MIRANDA_BASE, 'lib')
TMP_PATH = os.path.join(MIRANDA_BASE, 'tmp')

# Server Urls
SERVER_BASE = 'http://localhost:5000'
SEND_URL = SERVER_BASE + '/id/'
MODE_URL = SERVER_BASE + '/mode/0'

# Window GUI configs
WINDOW_WIDTH = 1366

# Mode Consts
MODE_IDEL = 1
MODE_NORMAL = 2
MODE_COLLECT = 3

# Miranda behavior configs
POLLING_INTERVAL = 5
TMPCLEAN_INTERVAL = 60
CAPTURE_INTERVAL = 0.1
FEEDBACK_SHOWTIME = 1.5
CONFIDENCE_THRESHOLD = 80
