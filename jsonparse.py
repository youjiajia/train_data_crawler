#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# yjj @  2016-03-28 10:24:31

import json

JSON_FILE = 'data/火车班次json数据'

def getCode(text):
    result = json.loads(text)
    return next(result['ticketInfo'].keys().__iter__())
def main():
    text_list = open(JSON_FILE,'r').readlines()
    for text in text_list:
        print(getCode(text))

if __name__ == '__main__':
    main()
