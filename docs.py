#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
from sqlite3 import connect
from json import load
import xml.etree.ElementTree as et

dbpath = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'docspath.json'))

with open(dbpath) as f:
    dbpath = load(f)

dbpath = dbpath['path']
dbs = (os.path.join(dbpath, d, 'Contents', 'Resources', 'docSet.dsidx')
       for d in os.listdir(dbpath))

jg = []


def searchdocs(db, query):
    docroot = db.split(os.path.sep)[:-3]
    docroot[0] += os.path.sep
    pl = docroot[-1].split('.')[0]
    img = os.path.join(*docroot, 'icon@2x.png')

    # get bundle identifier
    infoplist = os.path.join(*docroot,'Contents','Info.plist')
    d = et.parse(infoplist).getroot().find('dict')
    dcsid = pl
    for i,e in enumerate(d):
        if e.tag == 'key' and e.text == 'CFBundleIdentifier':
            if d[i+1].tag == 'string':
                dcsid = d[i+1].text
    with connect(db) as conn:
        conn.text_factory = str
        cur = conn.cursor()
        sql = "select name as score from searchIndex where name like ? order by length(name) limit 30"
        c = cur.execute(sql, ('%'+query+'%',))
        res = c.fetchall()
        if len(res) > 0:
            for r in res:
                for s in r:
                    jg.append({
                        "pl": pl,
                        "img": img,
                        'res': s,
                        'dcsid': dcsid
                    })


def search(query):

    for db in dbs:
        # only query specified db
        # eg:
        # rust:alloc , only query rust db
        # rust,python: sys, query rust and python db
        if ':' in query:
            head, tail = query.split(':', 1)
            if not tail.startswith(':'):
                head = re.sub(r'(\w+)(\d+)', r'\1_\2', head)
                for k in head.split(','):
                    if (k+'.docset').lower() in db.lower():
                        searchdocs(db, tail)
            else:
                searchdocs(db, query)
        else:
            searchdocs(db, query)

    return jg


if __name__ == '__main__':
    from sys import argv
    from pprint import pprint
    pprint(search(argv[1]))
