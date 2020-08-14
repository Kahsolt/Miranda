#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 01 09:57:14 2017

@author: wanggd
@rearrange: kahsolt
"""

import os, sys
import cv2
import time
import logging
import threading
import requests
import mimetypes

from Tkinter import *

MIRANDA_BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(MIRANDA_BASE)
from Miranda.settings import *

# Paths
DATA_BASE = os.path.join(MIRANDA_BASE, 'data')
CASCADE_PATH = os.path.join(DATA_BASE, 'cascade')
LIB_PATH = os.path.join(DATA_BASE, 'lib')
TMP_PATH = os.path.join(DATA_BASE, 'tmp')
LOG_PATH = os.path.join(DATA_BASE, 'log')

CASCADE_FILE = os.path.join(CASCADE_PATH, 'haarcascade_frontalface_default.xml')

# Logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.join(LOG_PATH, 'miranda.log'), mode='a+')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s <%(filename)s:%(lineno)d> %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


# Tkinter GUI
class Application(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        APP_WIDTH, APP_HEIGHT = 15, 75
        X, Y = (WINDOW_WIDTH / 2 - APP_WIDTH / 2), 5
        self.master.minsize(APP_WIDTH, APP_HEIGHT)
        self.master.maxsize(APP_WIDTH, APP_HEIGHT)
        self.master.geometry('%dx%d+%d+%d' % (APP_WIDTH, APP_HEIGHT, X, Y))
        self.master.wm_attributes('-topmost', 1)    # effective on Windows only...
        self.master.title('签到系统')
        self.label_info = Label(self, text='请输入学号：')
        self.label_info.pack(fill=BOTH)
        self.entry_id = Entry(self)
        self.entry_id.pack(fill=BOTH)
        self.button_confirm = Button(self, text='确定', command=self.sign_in)
        self.button_confirm.pack(fill=BOTH)
        self.pack()

        cv2.namedWindow('FaceDetect', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('FaceDetect', cv2.WND_PROP_AUTOSIZE, cv2.CV_WINDOW_AUTOSIZE)
        self.face_cascade = cv2.CascadeClassifier(CASCADE_FILE)
        self.webcam = None
        for i in range(1000):
            if cv2.VideoCapture(i).isOpened():
                self.webcam = cv2.VideoCapture(i)
                break
        if self.webcam is None:
            logger.info('[WebCam] No webcam detected :(')
            self.quit()

        self.ID = None
        self.mode = MODE_IDEL

        self.tmp_cleaner = threading.Timer(TMPCLEAN_INTERVAL, self.clean_tmp)
        self.tmp_cleaner.start()
        self.mode_updater = threading.Timer(MODEUPDATE_INTERVAL, self.update_mode)
        self.mode_updater.start()
        self.main = threading.Thread(target=self.main_loop)
        self.main.start()

    # GUI Event Handlers
    def sign_in(self):
        text = self.entry_id.get()
        if text is not None and text != '':
            logger.info('[Input] received input %s' % text)
            self.ID = text
            self.entry_id.delete('0', 'end')

    # Background Main Loop
    def main_loop(self):
        # Auxiliary functions
        def draw_tick(img):
            point1 = (int(img.shape[0] / 3), int(img.shape[1] / 2))
            point2 = (int(2 * img.shape[0] / 3), int(2 * img.shape[1] / 3))
            point3 = (int(img.shape[0]), int(img.shape[1] / 6))
            cv2.line(img, point1, point2, (0, 255, 0), 8)
            cv2.line(img, point2, point3, (0, 255, 0), 8)

        def draw_cross(img):
            point1 = (int(img.shape[0] / 2), int(img.shape[1] / 4))
            point2 = (int(img.shape[0]), int(2 * img.shape[1] / 3))
            point3 = (int(img.shape[0]), int(img.shape[1] / 4))
            point4 = (int(img.shape[0] / 2), int(2 * img.shape[1] / 3))
            cv2.line(img, point1, point2, (0, 0, 255), 8)
            cv2.line(img, point3, point4, (0, 0, 255), 8)

        def draw_rectangle(img, face):
            for x, y, w, h in face:
                cv2.rectangle(img, (x, y), (x + w, y + h), 255, 2)

        def detect_face(img):
            face = []
            try:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                face = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            except:
                logger.warn('[Detect] Failed to detect face.')
            return face

        def check_match(img_path1, img_path2):
            if not os.path.isfile(os.path.join(LIB_PATH, img_path1)) or not os.path.isfile(os.path.join(LIB_PATH, img_path2)):
                logger.warn('[Photo] No your photos or records... :(')
                return False

            resp = self.post_images(img_path1, img_path2)
            if resp is not None and resp.get('confidence') > CONFIDENCE_THRESHOLD:
                return True
            else:
                logger.debug('[API] Json resp: %s', resp)
                return False

        # Loop Body
        loop = True
        while loop:
            if self.mode == MODE_IDEL:
                logger.info('[Mode] Switching to mode Idle')

                while self.mode == MODE_IDEL and loop:
                    ret, img = self.webcam.read()
                    if ret:
                        cv2.imshow('FaceDetect', img)
                        if cv2.waitKey(OPENCV_WAITKEY_TIME) & 0xFF == 27:
                            loop = False
                            break

            elif self.mode == MODE_COLLECT:
                logger.info('[Mode] Switching to mode Collect')

                start_time = time.time()
                face = []
                image_collected = None
                while self.mode == MODE_COLLECT and loop:
                    ret, img = self.webcam.read()
                    if ret:
                        if len(face) == 0:
                            face = detect_face(img)
                        elif time.time() - start_time >= DETECT_INTERVAL:
                            face = detect_face(img)
                            start_time = time.time()
                        if len(face) != 0:
                            image_collected = img.copy()
                            draw_rectangle(img, face)

                        cv2.imshow('FaceDetect', img)
                        if cv2.waitKey(OPENCV_WAITKEY_TIME) & 0xFF == 27:
                            loop = False
                            break

                    if image_collected is not None and isinstance(self.ID, str):
                        logger.info('[Collect] Collected photo of %s' % self.ID)
                        cv2.imwrite(os.path.join(LIB_PATH, '%s.jpg' % self.ID), image_collected)

                        draw_tick(image_collected)
                        cv2.imshow('FaceDetect', image_collected)
                        if cv2.waitKey(FEEDBACK_SHOWTIME) & 0xFF == 27:
                            loop = False

                        self.ID = None
                        face = []
                        image_collected = None

            elif self.mode == MODE_NORMAL:
                logger.info('[Mode] Switching to mode Normal')

                start_time = time.time()
                face = []
                face_detected = False
                photo_current_path = None
                photo_db_path = None
                while self.mode == MODE_NORMAL and loop:
                    ret, img = self.webcam.read()
                    if ret:
                        if len(face) == 0:
                            face = detect_face(img)
                        elif time.time() - start_time >= DETECT_INTERVAL:
                            face = detect_face(img)
                            start_time = time.time()
                        if len(face) != 0:
                            if isinstance(self.ID, str):
                                photo_current_path = os.path.join(TMP_PATH, '%s_%d.jpg' % (self.ID, int(time.time())))
                                photo_db_path = os.path.join(LIB_PATH, '%s.jpg' % self.ID)
                                cv2.imwrite(photo_current_path, img)
                                face_detected = True
                            else:
                                draw_rectangle(img, face)

                        cv2.imshow('FaceDetect', img)
                        if cv2.waitKey(OPENCV_WAITKEY_TIME) & 0xFF == 27:
                            loop = False
                            break

                    if face_detected:
                        if check_match(photo_db_path, photo_current_path):
                            draw_tick(img)
                            self.post_id(self.ID)
                        else:
                            draw_cross(img)

                        cv2.imshow('FaceDetect', img)
                        if cv2.waitKey(FEEDBACK_SHOWTIME) & 0xFF == 27:
                            loop = False

                        self.ID = None
                        face_detected = False

        # Loop Exit
        logger.info('[Sys] Shutting down...')
        self.tmp_cleaner.cancel()
        self.mode_updater.cancel()
        self.webcam.release()
        cv2.destroyAllWindows()
        self.quit()

    # Http APIs
    def post_images(self, img_path1, img_path2):
        API_URL = 'https://api-cn.faceplusplus.com/facepp/v3/compare'
        API_KEY = '7czGl-WWMO88mUMjMXspnKFL6rQIuCp4'
        API_SECRET = 's9EJmZhlK3X84EtbKzv5V7Nh0TKFda7p'
        API_AUTH = {
            'api_key': API_KEY,
            'api_secret': API_SECRET,
        }
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
            return requests.post(API_URL, files=files, data=API_AUTH).json()
        except:
            logger.error('[API] network failure perhaps... X(')
            return None

    def get_mode(self):
        mode = None
        try:
            mode = requests.get(MODE_URL).text
        except:
            logger.error('[Messager] Server crashed ??')
        return mode

    def post_id(self, id):
        try:
            resp = requests.get(SEND_URL, params={'stuNum': id})
            logger.info('[Messager] Sent "%s", received "%s"' % (id, resp))
            return resp == 'success'
        except:
            logger.error('[Messager] Server crashed ??')
            return False

    # Timer tickers
    def update_mode(self):
        mode = self.get_mode()
        if mode and mode != self.mode:
            if mode not in [MODE_IDEL, MODE_NORMAL, MODE_COLLECT]:
                logger.info('[Mode] Unknown sever requirement: ' + mode)
            else:
                self.mode = mode
                logger.info('[Mode] Server require changing mode to: ' + self.mode)

        self.mode_updater = threading.Timer(MODEUPDATE_INTERVAL, self.update_mode)
        self.mode_updater.start()

    def clean_tmp(self):
        try:
            for tmp in os.listdir(TMP_PATH):
                if tmp.endswith('.jpg'):
                    os.remove(os.path.join(TMP_PATH, tmp))
            logger.info('[Tmp] Tmp files cleaned :D')
        except:
            logger.info('[Tmp] Cannot clean tmp files... :L')

        self.tmp_cleaner = threading.Timer(TMPCLEAN_INTERVAL, self.clean_tmp)
        self.tmp_cleaner.start()


def run():
    logger.info('[Sys] Starting up...')
    tk = Tk()
    app = Application(tk)
    app.mainloop()
    app.destroy()
    app.quit()
    logger.info('[Sys] Bye.')


if __name__ == '__main__':
    run()