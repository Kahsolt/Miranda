#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 01 10:00:31 2017

@author: wanggd
@rearrange: kahsolt
"""

import os
import requests
import mimetypes

from Miranda.settings import *

API_URL = 'https://api-cn.faceplusplus.com/facepp/v3/compare'
API_KEY = '7czGl-WWMO88mUMjMXspnKFL6rQIuCp4'
API_SECRET = 's9EJmZhlK3X84EtbKzv5V7Nh0TKFda7p'
API_AUTH = {
    'api_key': API_KEY,
    'api_secret': API_SECRET,
}
# face_set_token = u'7762386b14d65571266c05a5edd2f630'


def post_images(img_path1, img_path2):
    try:
        files = {
            'image_file1': (
                os.path.basename(img_path1),
                open(img_path1, 'rb'),
                mimetypes.guess_type(img_path1)[0]
            ),
            'image_file2': (
                os.path.basename(img_path2),
                open(img_path2, 'rb'),
                mimetypes.guess_type(img_path2)[0]
            ),
        }
        return requests.post(API_URL, files = files, data = API_AUTH).json()
    except:
        print('[API] network failure perhaps... X(')
        return None


def check_match(img_path1, img_path2):
    if not os.path.isfile(os.path.join(PHOTO_PATH, img_path1)) or not os.path.isfile(os.path.join(PHOTO_PATH, img_path1)):
        print('[API] No your photos... :(')
        return False

    response = post_images(img_path1, img_path2)
    return response is not None and response.get('confidence') > CONFIDENCE_THRESHOLD or False