#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 01 09:57:14 2017

@author: wanggd
@rearrange: kahsolt
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2
import time
import threading
from tkinter import *

from Miranda.settings import *
from Miranda import api
from Miranda import messager


# Global vars
ID = None
MODE = MODE_IDEL
cv2.namedWindow('FaceDetect', cv2.WND_PROP_FULLSCREEN)
face_cascade = cv2.CascadeClassifier(os.path.join(RES_PATH, 'haarcascade_frontalface_default.xml'))
# cv2.setWindowProperty('FaceDetect', cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)


# auxiliary functions
def draw_tick(img):
    point1 = (int(img.shape[0]/3), int(img.shape[1]/2))
    point2 = (int(2*img.shape[0]/3), int(2*img.shape[1]/3))
    point3 = (int(img.shape[0]), int(img.shape[1]/6))
    cv2.line(img, point1, point2 ,(0,255,0), 8)
    cv2.line(img, point2, point3 ,(0,255,0), 8)


def draw_cross(img):
    point1 = (int(img.shape[0]/2), int(img.shape[1]/4))
    point2 = (int(img.shape[0]), int(2*img.shape[1]/3))
    point3 = (int(img.shape[0]), int(img.shape[1]/4))
    point4 = (int(img.shape[0]/2), int(2*img.shape[1]/3))
    cv2.line(img, point1, point2 ,(0,0,255), 8)
    cv2.line(img, point3, point4 ,(0,0,255), 8)


def find_webcam():
    for i in range(1000):
        capInput = cv2.VideoCapture(i).isOpened()
        if capInput:
            return i
    return None


# Working mode functions
def mode_idle():
    global MODE
    print '[Mode] Switching to mode Idle'

    while MODE == MODE_IDEL:
        ret, img = capInput.read()
        cv2.imshow('FaceDetect', img)
        if cv2.waitKey(1) & 0xFF == 27:
            sys.exit(1)


def mode_collect():
    global ID, MODE
    print '[Mode] Switching to mode Collect'

    next_capture_time = time.time()
    face = []

    while MODE == MODE_COLLECT:
        image_collected = None

        ret, img = capInput.read()
        if next_capture_time < time.time():
            next_capture_time = time.time() + CAPTURE_INTERVAL
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(face) != 0:
            image_collected = img.copy()
            for x, y, w, h in face:
                cv2.rectangle(img, (x, y), (x + w, y + h), 255, 2)
        cv2.imshow('FaceDetect', img)
        if cv2.waitKey(1) & 0xFF == 27:
            sys.exit(1)

        if image_collected is not None and isinstance(ID, str):
            print '[Collect] collected photo of %s' % ID
            cv2.imwrite(os.path.join(PHOTO_PATH, '%s.jpg' % (ID)), image_collected)
            draw_tick(image_collected)

            start_time = time.time()
            while time.time() - start_time < FEEDBACK_SHOWTIME:
                cv2.imshow('FaceDetect', image_collected)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            ID = None


def mode_normal():
    global ID, MODE
    print '[Mode] Switching to mode Normal'

    next_capture_time = time.time()
    face = []

    while MODE == MODE_NORMAL:
        face_detected = False
        photo_current_path = None
        photo_db_path = None

        ret, img = capInput.read()
        if next_capture_time < time.time():
            next_capture_time = time.time() + CAPTURE_INTERVAL
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face = face_cascade.detectMultiScale(gray, 1.3, 5)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(face) != 0:
            if isinstance(ID, str):
                photo_current_path = os.path.join(TMP_PATH, '%s_%d.jpg' % (ID, int(time.time())))
                photo_db_path = os.path.join(PHOTO_PATH, '%s.jpg' % (ID))
                cv2.imwrite(photo_current_path, img)
                face_detected = True
            else:
                for x, y, w, h in face:
                    cv2.rectangle(img, (x, y), (x + w, y + h), 255, 2)
        cv2.imshow('FaceDetect', img)
        if cv2.waitKey(1) & 0xFF == 27:
            break

        if face_detected:
            if api.check_match(photo_db_path, photo_current_path):
                draw_tick(img)
                messager.post_id(ID)
            else:
                draw_cross(img)
            begin = time.time()
            while time.time() - begin < FEEDBACK_SHOWTIME:
                cv2.imshow('FaceDetect', img)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            ID = None


# Tkinter GUI
class Application(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        WIDTH = 150
        HEIGHT = 75
        X = WINDOW_WIDTH / 2 - WIDTH / 2
        Y = 5
        self.master.minsize(WIDTH, HEIGHT)
        self.master.maxsize(WIDTH, HEIGHT)
        self.master.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, X, Y))
        self.master.wm_attributes('-topmost', 1)  # 窗口置顶，仅win有效……
        self.master.title('签到系统')
        self.createWidgets()
        self.pack()

    def createWidgets(self):
        self.labelInfo = Label(self, text='请输入学号：')
        self.labelInfo.pack(fill=BOTH)
        self.nameInput = Entry(self)
        self.nameInput.pack(fill=BOTH)
        self.alertButton = Button(self, text='确定', command=self.sign_in)
        self.alertButton.pack(fill=BOTH)

    def sign_in(self):
        global ID
        _input = self.nameInput.get()
        if _input != '':
            ID = _input
            print '[Input] received input %s' % ID
        self.nameInput.delete('0','end')


# Loop main
def main_loop():
    global MODE

    while True:
        if MODE == MODE_NORMAL:
            mode_normal()
        elif MODE == MODE_COLLECT:
            mode_collect()
        else:
            mode_idle()

# Timer tickers
def update_mode():
    global MODE
    mode = messager.get_mode()
    if mode and mode != MODE:
        MODE = mode
        print '[Mode] server require changing mode to %d' % mode

    global mode_updater
    mode_updater = threading.Timer(POLLING_INTERVAL, update_mode)
    mode_updater.start()


def clean_tmp():
    tmps = os.listdir(TMP_PATH)
    try:
        for tmp in tmps:
            if tmp.endswith('.jpg'):
                os.remove(os.path.join(TMP_PATH, tmp))
        print '[Tmp] tmp files cleaned :D'
    except:
        print '[Tmp] cannot clean tmp files... :L'

    global tmp_cleaner
    tmp_cleaner = threading.Timer(TMPCLEAN_INTERVAL, clean_tmp)
    tmp_cleaner.start()


#############
# Main Entry
#
webcam = find_webcam()
if webcam is None:
    print '[WebCam] No webcam detected :('
    sys.exit(-1)
capInput = cv2.VideoCapture(webcam)

tk = Tk()
app = Application(tk)
tmp_cleaner = None
clean_tmp()
mode_updater = None
update_mode()
main = threading.Thread(target=main_loop)
main.start()
app.mainloop()

