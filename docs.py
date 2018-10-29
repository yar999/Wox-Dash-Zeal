#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
from sqlite3 import connect
from json import load

dbpath = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'docspath.json'))

with open(dbpath) as f:
    dbpath = load(f)

dbpath = dbpath['path']
dbs = (os.path.join(dbpath, d, 'Contents', 'Resources', 'docSet.dsidx')
       for d in os.listdir(dbpath))

jg = []


def searchdocs(db, query):
    with connect(db) as conn:
        conn.text_factory = str
        cur = conn.cursor()
        sql = "select name as score from searchIndex where name like ? order by length(name) limit 30"
        c = cur.execute(sql, ('%'+query+'%',))
        res = c.fetchall()
        if len(res) > 0:
            pl = db.split(os.path.sep)[4].split('.')[0]
            img = os.path.join(dbpath, db.split(
                os.path.sep)[4], 'icon@2x.png')
            for r in res:
                for s in r:
                    jg.append({
                        "pl": pl,
                        "img": img,
                        'res': s
                    })


def search(query):

    for db in dbs:
        # only query specified db
        # eg:
        # rust:alloc , only query rust db
        # rust,python: sys, query rust and python db
        if ":" in query:
            head, tail = query.split(':', 1)
            head = re.sub(r'(\w+)(\d+)', r'\1_\2', head)
            for k in head.split(','):
                if (k+'.docset').lower() in db.lower():
                    searchdocs(db, tail)
        else:
            searchdocs(db, query)

    return jg


if __name__ == '__main__':
    from sys import argv
    from pprint import pprint
    pprint(search(argv[1]))
