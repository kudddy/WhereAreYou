#! /usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from ext.Pickler import work_with_pickle
import dlib
import face_recognition
import numpy as np
import cv2
from time import sleep
import os
from ext.Helper import url_to_date

from ext.FaceAndBase import FindAddFace


class RecursionRequests:
    def __init__(self):
        self.request = requests
        self.max_depth = 10
        self.iterator = 0

    def start_pulling(self, url):
        if self.max_depth > self.iterator:
            try:
                response = self.request.get(url, verify=False)
            except Exception as e:
                print('Проблемы, заходим в итератор')
                print(str(e))
                self.iterator = self.iterator + 1
                sleep(10)
                return self.start_pulling(url)
            return response
        else:
            self.iterator = 0
            return -1


class MakeEncoders:
    def __init__(self):
        self.req = RecursionRequests()
        self.global_dict = {}
        self.step = 0
        self.face = FindAddFace()

    def get_past_date(self):
        date = self.face.db.easy_select_query('SELECT date FROM vectors order by date desc limit 1')
        return list(date)[0][0]

    def get_url(self):
        url = 'https://img1.night2day.ru/1/gal/'
        page = self.req.start_pulling(url)
        date_old = self.get_past_date()
        if page == -1:
            pass
        else:
            soup = BeautifulSoup(page.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                url_construct = url + a['href'] + '/norm'
                page = requests.get(url_construct)
                soup = BeautifulSoup(page.text, 'html.parser')
                for b in soup.find_all('a', href=True):
                    if b['href'].endswith('jpg'):
                        local_dict = {
                            'dir_name': a['href'],
                            'pic_name': b['href'],
                            'full_name_url': url_construct + '/' + b['href']
                        }
                        date_new = url_to_date(local_dict['full_name_url'])
                        if date_new > date_old:
                            yield local_dict

    def get_encoders_by_url(self, url: str):
        local_dict = {}
        print(url)
        response = self.req.start_pulling(url)
        if response == -1:
            return local_dict
        else:
            image = np.asarray(bytearray(response.content), dtype="uint8")
            if len(image) > 0:
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                face_detector = dlib.get_frontal_face_detector()
                try:
                    detected_faces = face_detector(image, 1)
                    for i, face_rect in enumerate(detected_faces):
                        crop = image[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]
                        encodings = face_recognition.face_encodings(crop)
                        if len(encodings) > 0:
                            re_url = url + '_{}'.format(i)
                            local_dict.update({re_url: encodings})
                            self.face.add_face((re_url, url_to_date(re_url), encodings))
                            print('добавили лицо')

                except Exception as e:
                    print('мы тут')
                    print(e)

        return local_dict

    def main(self):
        try:
            arr = []
            url_generator = self.get_url()
            for url in tqdm(url_generator):
                arr.append(url)
                local = self.get_encoders_by_url(url['full_name_url'])
                if len(local) > 0:
                    self.global_dict.update(local)
                self.step = self.step + 1
            work_with_pickle.dump_pickle_file(self.global_dict, 'encoders.pickle')
        except Exception as e:
            print('пиздец')
            print(str(e))
            print(self.step)
            work_with_pickle.dump_pickle_file(self.global_dict, 'encoders_{}.pickle'.format(len(os.listdir())))


class UpdateMeForever:
    def __init__(self, timer=64*60*60):
        self.worker = MakeEncoders()
        self.timer = timer

    def check_updades(self):
        while True:
            self.worker.main()
            sleep(self.timer)
