#! /usr/bin/env python
# -*- coding: utf-8 -*-
from ext.dbBase import PG
from ext.FaceAndBase import FindAddFace

db = PG()
face = FindAddFace()

db.setup_db()
print('База данных сконфигурирована')

face.fill_base()

print('База данных заполнена')
