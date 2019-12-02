#! /usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2


class PG:
    def __init__(self):
        self.con = psycopg2.connect("user='user' password='pass' host='localhost' dbname='db' port='5434'")

    def easy_insert_query(self, query):
        cursor = self.con.cursor()
        try:
            cursor.execute(query)
            self.con.commit()
        except Exception as e:
            print(e)
        cursor.close()

    def easy_select_query(self, query):
        cursor = self.con.cursor()
        try:
            cursor.execute(query)
            row = cursor.fetchall()
        except Exception as e:
            print(e)
            row = -1
        cursor.close()
        return row

    def setup_db(self):
        cursor = self.con.cursor()
        cursor.execute("create extension if not exists cube;")
        cursor.execute("drop table if exists vectors")
        cursor.execute("create table vectors (id serial, file varchar, date timestamp, vec_low cube, vec_high cube);")
        cursor.execute("create index vectors_vec_idx on vectors (vec_low, vec_high);")
        self.con.commit()
        cursor.close()

    def __del__(self):
        if self.con is not None:
            print('Соединение закрыто')
            self.con.close()
