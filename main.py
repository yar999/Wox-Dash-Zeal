#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
from wox import Wox, WoxAPI
from json import load, dump
import re


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

        qsl = re.split(r'\s|=', query)

        alias = self.listk()
        key = qsl[0]

        if len(query) > 0 and key in alias:
            query = query.replace(key, alias[key], 1)

        if ':' in key:
            one = key.split(':')[0]
            if one in alias:
                query = query.replace(one, alias[one], 1)

        res["SubTitle"] = "Get Zeal docs for {}".format(query)
        res["JsonRPCAction"] = {"method": "zeal",
                                "parameters": [query],
                                "dontHideAfterAction": False}

        if qsl[0] == '~list':
            for k, v in self.listk().items():
                jg.append({
                    'Title': k+' -> '+v,
                    'IcoPath': "Images/Zeal.png",
                })

            return jg

        if qsl[0] == '~help':
            jg.append({"Title": "set query alias",
                       "IcoPath": "Images/Zeal.png", "SubTitle": "z set py3=python3"})
            jg.append({"Title": "del query alias",
                       "IcoPath": "Images/Zeal.png", "SubTitle": "z del py3"})
            jg.append({"Title": "list query alias",
                       "IcoPath": "Images/Zeal.png", "SubTitle": "z list a"})
            return jg

        if qsl[0] == '~del' and len(qsl) == 2:
            res["SubTitle"] = "del query alias {}".format(qsl[1])
            res["JsonRPCAction"] = {"method": "delk",
                                    "parameters": [qsl[1]],
                                    "dontHideAfterAction": False}

        if qsl[0] == '~set' and len(qsl) == 3:
            res["SubTitle"] = "set query alias {}={}".format(qsl[1], qsl[2])
            res["JsonRPCAction"] = {"method": "setk",
                                    "parameters": [qsl[1], qsl[2]],
                                    "dontHideAfterAction": False}

        jg.append(res)
        return jg


if __name__ == "__main__":
    Main()
