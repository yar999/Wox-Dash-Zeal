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


def searchdocs(d, query):
    with connect(d) as conn:
        conn.text_factory = str
        cur = conn.cursor()
        sql = "select name from searchIndex where name like ? order by name limit 30"
        c = cur.execute(sql, ('%'+query+'%',))
        res = c.fetchall()
        if len(res) > 0:
            pl = d.split(os.path.sep)[4].split('.')[0]
            img = os.path.join(dbpath, d.split(
                os.path.sep)[4], 'icon@2x.png')
            for r in res:
                for s in r:
                    jg.append({
                        "pl": pl,
                        "img": img,
                        'res': s
                    })


def search(query):

    for d in dbs:
        # only query specified db
        # eg: rust:alloc , only query rust db
        if ":" in query:
            one = query.split(':', 1)[0]

            # pythonx db is python_x
            m = re.match(r'(\w+)(\d+)', one)
            if m:
                one = "{}_{}".format(m.group(1), m.group(2))

            if one.lower() not in d.lower():
                continue

            query = query.split(':', 1)[1]
            searchdocs(d, query)
            break
        else:
            searchdocs(d, query)

    return jg


if __name__ == '__main__':
    from sys import argv
    from pprint import pprint
    pprint(search(argv[1]))
