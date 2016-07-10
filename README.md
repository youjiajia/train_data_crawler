# 高铁时刻表, 高铁班次    

从去哪儿网爬取高铁的时刻表, 高铁班次，高铁票价信息并保存在文件里面。  

** 如果你只是想用数据， 请查看data里面的文件，避免再次爬取减少服务器压力 **。  


## 使用方法  
pip install -r requirements.txt  
python3 crawler.py
python3 secondcrawler.py
python3 jsonparse.py > data/火车班次列表
