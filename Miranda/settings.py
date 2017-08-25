#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# author:   kahsolt
# date:     2017-08-17

# Server urls
SERVER_BASE = 'http://219.224.166.2:8011'
SEND_URL = SERVER_BASE + '/teacher/signIn/input'
MODE_URL = SERVER_BASE + '/teacher/signIn/state'

# Mode consts defined by server
MODE_IDEL = 'free'
MODE_NORMAL = 'signIn'
MODE_COLLECT = 'record'

# Miranda behavior configs
WINDOW_WIDTH = 1366
MODEUPDATE_INTERVAL = 5
TMPCLEAN_INTERVAL = 300
CAPTURE_INTERVAL = 0.1
DETECT_INTERVAL = 0.1
FEEDBACK_SHOWTIME = 1500
OPENCV_WAITKEY_TIME = 10
CONFIDENCE_THRESHOLD = 80
