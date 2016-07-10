# -*- coding: utf-8 -*-
# yjj @ 2016-04-07 11:41:11

import datetime, requests, time, json, logging, os

from requests.exceptions import Timeout

URL = 'http://train.qunar.com/qunar/checiInfo.jsp'
DEFAULT_DATE = datetime.datetime.now() + datetime.timedelta(30,0,0)
DEFAULT_DATE_STR = DEFAULT_DATE.strftime('%Y-%m-%d') # 默认查询30天后的时刻表

logging.basicConfig(level=logging.WARN,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='./log/crawler.log',
                filemode='a')

def getotherinfo(train_number = 'G24'):
    ''' 输入: 高铁班次: G24， 
              日期: '2016-04-30';
        获取所有班次类似车次为 GXX/GXX 的车次信息写入‘其他火车班次列表’
    '''
    logging.info('getotherinfo')
    url = 'http://train.qunar.com/qunar/checiSuggest.jsp?callback=jQuery17208000492092391186_1460000280989&include_coach_suggest=true&lang=zh&q='+train_number+'&sa=true&format=js&_=1460000429009'
    try: 
        response = requests.get(url=url, timeout=10)
    except Timeout:
        logging.error('无法从服务器获取数据')
        logging.error('url: '+url)
        return None
    results=json.loads('{'+response.text.split('({')[1].split('})')[0]+'}')['result']
    for result in results:
        opendatafile = open('./data/其他火车班次列表','r')
        lines=opendatafile.readlines()
        if ('/' in result['key']) & (result['key']+'\n' not in lines):
            gotfile = open('./data/其他火车班次列表','a')
            gotfile.write(result['key'])
            gotfile.write('\n')
            gotfile.close()
        opendatafile.close()
def getinfo(train_number = 'G99', date=DEFAULT_DATE_STR):
    ''' 输入: 高铁班次: G11， 
              日期: '2016-04-30';
        输出: { # 输出格式暂时不修改, 
            'train_number':'G1',
            'date': '2016-04-21',
            'schedule': [
                ["站次","站名","到达时间", "开车时间","停车时间","里程"]
                    # 起始站的到达时间， 终点站的开车时间， 二者的停车时间都为 "-"
                [],  # 第一个数据是起始站
                [],  # 中间的数据是停靠站
                [],  # 中间的数据是停靠站
                [],  # 中间的数据是停靠站
                ,...,
                [],  # 最后一个数据是终点站
            ]
        }
    '''
    logging.info('getinfo')
    params = {
        'method_name': 'buy',
        'ex_track': '',
        'q': train_number,
        'date': date.replace('-',''),
        'format': 'json',
        'cityname': 123456,
        'ver': int(time.time()*1000),
    }
    url = URL
    try: 
        response = requests.get(url=url,params=params,
                headers={'Content-Type':'application/json'}, timeout=10)
    except Timeout:
        logging.error('无法从服务器获取数据')
        logging.error('url: '+url)
        logging.error(params)
        return None
    result = json.loads(response.text)
    if result== {'count':0}:
        logging.error('无法获取该火车班次，班次为'+train_number)
        return None
    return response.text
def main(start=1,getstart=1):
    notrainfile=open('./data/不存在的火车车次','r')
    start=start-1
    getstart=getstart-1
    notrainlines=notrainfile.readlines()[start:]
    notrainnum=0
    for line in notrainlines:
        if 0 <= datetime.datetime.now().hour <= 6:
            time.sleep(2)   # 凌晨服务器压力小2秒一次，一晚上就能爬完
        else:
            time.sleep(6)   # 6秒一次，不要太快
        notrainnum += 1
        print '共'+str(len(notrainlines))+'条不存在的高铁,现在查询第'+str(notrainnum)+'条数据'
        result=getotherinfo(line[0:-1])
    notrainfile.close()
    gotbancifile = open('./data/其他火车班次列表','r')
    lines=gotbancifile.readlines()[getstart:]
    n=0
    for line in lines:
        if 0 <= datetime.datetime.now().hour <= 6:
            time.sleep(2)   # 凌晨服务器压力小2秒一次，一晚上就能爬完
        else:
            time.sleep(6)   # 6秒一次，不要太快
        n += 1
        print '共'+str(len(lines))+'条数据,现在开始获取第'+str(n)+'条数据'
        result=getinfo(line[0:-1])
        if result:
            gotfile = open('./data/火车班次json数据','a')
            gotfile.write(result.encode('utf-8'))
            gotfile.write('\n')
            gotfile.close()
            gotfile = open('./data/火车班次列表','a')
            gotfile.write(line[0:-1])
            gotfile.write('\n')
            gotfile.close()
    gotbancifile.close()
if __name__ == '__main__':
    start=str(datetime.datetime.now())
    if len(os.sys.argv) > 1:
        start = int(os.sys.argv[1])
        getstart = int(os.sys.argv[2])
        print('输入了参数 '+str(start)+'和'+str(getstart)+' 爬虫将会从该行开始抓取')
        main(start,getstart)
    else:
        print('爬虫脚本已启动, 使用"tail -f ./data/火车班次json数据" 可以实时查看抓取的数据,开始时间为'+start)
        main()
    end=str(datetime.datetime.now())
    print('抓取完毕，请进入data文件夹查看数据， 进入log文件夹查看日志,开始时间为'+start+'结束时间为'+end)
