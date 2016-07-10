#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @  ramwin@qq.com2016-03-28 10:41:20

import requests
url = 'http://train.qunar.com/qunar/checiSuggest.jsp'
params = {
    'include_coach_suggest': False,
    'lang': 'zh',
    'q': 'G96',
    'sa': True,
    'format': 'json',
}

def getSuggets(train_number='G96'):
    ''' 输入: 车次号 G96
        输出: 
response = requests.get(url,params=params,
        headers={'Content-Type':'application/json'})
print(response.text)
print(response.status_code)
