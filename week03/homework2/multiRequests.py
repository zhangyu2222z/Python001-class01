import requests
from concurrent.futures import ThreadPoolExecutor
import json
import configparser
import pymysql
import threading
import time

# 爬取数据，解析，入库
def getJson(url, pageNum, headers, infoList, config, mainUrl):
    global showId
    global cnt
    # 组装数据请求所需参数，第一页单独处理
    if pageNum == 0:
        showId = ''
        cnt = 0
        payload = {'first':'True', 'pn':'1', 'kd':'Python 工程师'}
    else:
        payload = {'first':'false', 'pn':str(pageNum+1), 'kd':'Python 工程师','sid':showId}
    session = requests.session()
    # 先拿到搜索页面的cookie
    session.get(mainUrl, headers=headers, timeout=3)
    cookie = session.cookies
    # 在将拿到的cookie放入此次数据请求中才能拿到数据，否则被反爬
    response = session.post(url,  headers = headers, data = payload, cookies = cookie)
    resultStr = response.text
    # print(json.loads(resultStr).get('msg'))
    # 解析回来的json数据
    showId = json.loads(resultStr).get('content').get('showId')
    infoDictList = json.loads(resultStr).get('content').get('positionResult').get('result')
    dataLen = int(json.loads(resultStr).get('content').get('positionResult').get('resultSize'))
    # 如果超过此次回来数据和计数器的和 超过 100 则自动截取到达第100的步长
    if (cnt + dataLen) > 100:
        dataLen = 100 - cnt
    # print(f'{cnt} + {dataLen}')
    for i in range(dataLen):
        item = infoDictList[i]
        # 到了第100条就跳出，重置计数，和请求所需数据id
        if cnt > 100:
            cnt = 0
            showId = ''
            break
        res = [item['positionName'], item['city'], item['salary']]
        # 判断去重
        if res not in infoList:
            infoList.append(res)
            # 入库
            conn = pymysql.connect(host = config.get('mysql', 'host'), port = int(config.get('mysql', 'port')), 
                user = config.get('mysql', 'user'), password = config.get('mysql', 'password'), db = config.get('mysql', 'db'))
            try:
                cur = conn.cursor()
                sqlStr = "INSERT INTO t_position_info(pos_name, area, salary) VALUES('%s', '%s', '%s') " %(item['positionName'], item['city'], item['salary'])
                cur.execute(sqlStr)
                cur.close()
                conn.commit()
            except Exception as e: 
                conn.rollback()
                print(e)
            finally:
                conn.close()
        # 每条数据计数+1
        cnt += 1

if __name__ == '__main__':
    # db配置
    config = configparser.ConfigParser()
    config.read('./homework2/properties.conf', encoding='utf-8')

    infoList = []
    # 数据请求url
    urlList = ['https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false', 
        'https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false', 
        'https://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false', 
        'https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'
        ]
    # 搜索页页面url，用来每次访问拿cookie，否则被反爬
    mainUrls = ['https://www.lagou.com/jobs/list_Python%20%E5%B7%A5%E7%A8%8B%E5%B8%88/p-city_2?px=default#filterBox',
                 'https://www.lagou.com/jobs/list_Python%20%E5%B7%A5%E7%A8%8B%E5%B8%88/p-city_3?px=default#filterBox',
        'https://www.lagou.com/jobs/list_Python%20%E5%B7%A5%E7%A8%8B%E5%B8%88/p-city_213?px=default#filterBox',
        'https://www.lagou.com/jobs/list_Python%20%E5%B7%A5%E7%A8%8B%E5%B8%88/p-city_215?px=default#filterBox'
        ]
    # 计数，每个地区100个
    cnt = 0
    # 分页id
    showId = ''
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'https://www.lagou.com/jobs/list_Python%20%E5%B7%A5%E7%A8%8B%E5%B8%88/p-city_3?px=default',
        # 'Cookie':'JSESSIONID=ABAAAECAAEBABIID9252A43743CA00F51124DF76AD80D57; WEBTJ-ID=20200712124813-173415a25033c7-020e9509e579fd-3b634404-1327104-173415a2504836; RECOMMEND_TIP=true; _ga=GA1.2.196054656.1594529294; _gid=GA1.2.533671658.1594529294; user_trace_token=20200712124811-83474279-45c7-4431-bf57-7c55ac172417; LGUID=20200712124811-d25af6f4-be93-4065-85be-cef4de45b986; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22173415ba4c11b4-0e935238df3c94-3b634404-1327104-173415ba4c47fd%22%2C%22%24device_id%22%3A%22173415ba4c11b4-0e935238df3c94-3b634404-1327104-173415ba4c47fd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; X_MIDDLE_TOKEN=a0de168699e6e7d15ebf40f963557da3; index_location_city=%E6%B7%B1%E5%9C%B3; PRE_UTM=; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1594529294,1594540151; LGSID=20200712154908-f7a3122b-a4d2-4f34-aecd-8045857221bc; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D37kY9kKkEfVzFCjJERc1hqMSUT9tGvL5gqvuoY2c%5Fye%26wd%3D%26eqid%3Dd4ce99c900002acc000000035f0ac070; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; gate_login_token=07f1afbd653ea553f6de67b6868ca35b637081a2130707fa1b524f72390a61d4; _putrc=0523EA4274C746BC123F89F2B170EADC; login=true; unick=%E7%94%A8%E6%88%B74157; privacyPolicyPopup=false; hasDeliver=0; _gat=1; X_HTTP_TOKEN=8bf05dc99382f8b3166145495194295760040a6147; TG-TRACK-CODE=index_navigation; SEARCH_ID=33d6948bbb36492cabb3739a8789c1f8; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1594541814; LGRID=20200712161651-9de857be-ffae-49a8-bfcc-46bd906f731a',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}  
    with ThreadPoolExecutor(max_workers=5) as t:
        for num in range(len(urlList)):
            for i in range(7):
                # 等几秒，降低频率
                time.sleep(3)
                t.submit(getJson, urlList[num], i, headers, infoList, config, mainUrls[num])