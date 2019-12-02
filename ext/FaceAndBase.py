#! /usr/bin/env python
# -*- coding: utf-8 -*-
from ext.dbBase import PG
import dlib
import face_recognition
import cv2
import requests
import numpy as np
from ext.Pickler import work_with_pickle as pcl
from tqdm import tqdm
from ext.Helper import url_to_date

class FindAddFace:
    def __init__(self):
        self.db = PG()

    def add_face(self, tpl):
        # Loop through each face we found in the image
        # Detected faces are returned as an object with the coordinates
        # of the top, left, right and bottom edges
        target = tpl[0]
        date = tpl[1]
        encodings = tpl[2]

        if len(tpl) > 0:
            query = "INSERT INTO vectors (file, date,  vec_low, vec_high) VALUES ('{}','{}', CUBE(array[{}]), CUBE(array[{}]));".format(
                target, date,
                ','.join(str(s) for s in encodings[0][0:64]),
                ','.join(str(s) for s in encodings[0][64:128]),
            )
            self.db.easy_insert_query(query)
        else:
            pass

    def find_face(self, url):
        # Create a HOG face detector using the built-in dlib class
        response = requests.get(url, verify=True)

        image = np.asarray(bytearray(response.content), dtype="uint8")
        if len(image) > 0:
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        else:
            return -1
        face_detector = dlib.get_frontal_face_detector()

        # Run the HOG face detector on the image data
        detected_faces = face_detector(image, 1)
        if len(detected_faces) > 0:
            # Loop through each face we found in the image
            for i, face_rect in enumerate(detected_faces):
                # Detected faces are returned as an object with the coordinates
                # of the top, left, right and bottom edges
                print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(),
                                                                                         face_rect.right(), face_rect.bottom()))
                crop = image[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]
                threshold = 0.6
                encodings = face_recognition.face_encodings(crop)
                if len(encodings) > 0:
                    query = "SELECT file FROM vectors ORDER BY " + \
                            "(CUBE(array[{}]) <-> vec_low) + (CUBE(array[{}]) <-> vec_high) ASC LIMIT 50;".format(
                                ','.join(str(s) for s in encodings[0][0:64]),
                                ','.join(str(s) for s in encodings[0][64:128]),
                            )
                    query_1 = "SELECT file FROM vectors WHERE sqrt(power(CUBE(array[{}]) <-> vec_low, 2) + power(CUBE(array[{}]) <-> vec_high, 2)) <= {} ".format(
                        ','.join(str(s) for s in encodings[0][0:64]),
                        ','.join(str(s) for s in encodings[0][64:128]),
                        threshold,
                    ) + \
                              "ORDER BY sqrt(power(CUBE(array[{}]) <-> vec_low, 2) + power(CUBE(array[{}]) <-> vec_high, 2)) ASC LIMIT 10".format(
                                  ','.join(str(s) for s in encodings[0][0:64]),
                                  ','.join(str(s) for s in encodings[0][64:128]),
                              )
                    row = self.db.easy_select_query(query_1)
                    return row
                else:
                    print("No encodings")
                    return -1
        else:
            return -1

    def fill_base(self):
        encoders = pcl.get_pickle_file('encoders.pickle')
        for k, v in tqdm(encoders.items()):
            tupl = (k, url_to_date(k), v)
            self.add_face(tupl)
        print('Загрузка прошла успешно')








