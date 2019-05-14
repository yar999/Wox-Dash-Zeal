#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
import re

from wox import Wox, WoxAPI
from json import load, dump
from docs import search


class Main(Wox):

    @property
    def aliasfile(self):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), 'alias.json'))

    def zeal(self, query):
        os.startfile("dash://{}".format(query))

    def setk(self, key, value):
        with open(self.aliasfile, 'r+') as f:
            alias = load(f)
            alias[key] = value
            f.seek(0)
            f.truncate()
            dump(alias, f, indent=4)
            WoxAPI.show_msg('set alias', '{}={}'.format(key, value))

    def delk(self, key):
        with open(self.aliasfile, 'r+') as f:
            alias = load(f)
            alias.pop(key)
            f.seek(0)
            f.truncate()
            dump(alias, f, indent=4)
            WoxAPI.show_msg('remove alias', '{}'.format(key))

    def listk(self):
        with open(self.aliasfile, 'r+') as f:
            alias = load(f)
            return alias

    def query(self, query):

        jg = []

        res = {"Title": "Zeal",
               "IcoPath": "Images/Zeal.png"}

        alias = self.listk()

        qsl = re.split(r'\s|=', query)
        key = qsl[0]

        if len(qsl) > 0 and key not in ('~list', '~set', '~del', '~help'):

            # repalce alias in key when ':' in key
            if ':' in key:
                head, tail = query.split(':', 1)
                headl = head.split(',')
                for n in range(len(headl)):
                    if headl[n] in alias:
                        headl[n] = alias[headl[n]]

                query = ','.join(headl) + ':' + tail.lstrip()

            sres = search(query)
            for sr in sres:
                pl = sr['pl']
                dcsid = sr['dcsid']

                jg.append({
                    'Title': sr['res'],
                    'SubTitle': pl,
                    'IcoPath': sr['img'],
                    'JsonRPCAction': {"method": "zeal",
                                      "parameters": [dcsid+':'+sr['res']],
                                      "dontHideAfterAction": False}
                })

            return jg

        if key == '~list':
            for k, v in self.listk().items():
                jg.append({
                    'Title': k+' -> '+v,
                    'IcoPath': "Images/Zeal.png",
                })

            return jg

        if key == '~help':
            jg.append({"Title": "set query alias",
                       "IcoPath": "Images/Zeal.png", "SubTitle": "z ~set py3=python3"})
            jg.append({"Title": "del query alias",
                       "IcoPath": "Images/Zeal.png", "SubTitle": "z ~del py3"})
            jg.append({"Title": "list query alias",
                       "IcoPath": "Images/Zeal.png", "SubTitle": "z ~list"})
            return jg

        if key == '~del' and len(qsl) == 2:
            res["SubTitle"] = "del query alias {}".format(qsl[1])
            res["JsonRPCAction"] = {"method": "delk",
                                    "parameters": [qsl[1]],
                                    "dontHideAfterAction": False}
            jg.append(res)
            return jg

        if key == '~set' and len(qsl) == 3:
            res["SubTitle"] = "set query alias {}={}".format(qsl[1], qsl[2])
            res["JsonRPCAction"] = {"method": "setk",
                                    "parameters": [qsl[1], qsl[2]],
                                    "dontHideAfterAction": False}
            jg.append(res)
            return jg


if __name__ == "__main__":
    Main()
