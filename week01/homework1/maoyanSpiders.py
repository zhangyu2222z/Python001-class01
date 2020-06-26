# 安装并使用 requests、bs4 库，爬取猫眼电影的前 10 个电影名称、电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。
# 安装命令：pip install requests
#           pip install bs4
import random
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# 抓取目标页面内容
def getPageContent():
    pageUrl = 'https://maoyan.com/films?showType=3'
    headers = {
        'Referer': 'https://u.geekbang.org/lesson/18?article=252019',
        'Cookie':'__mta=44439323.1593145138428.1593159946612.1593163905352.3; uuid_n_v=v1; uuid=23F8EC30B76411EAA2F937AFDFBC83F68905F9E8465D4E31AF7DFCAA143694B9; _csrf=4f32d2a4860976025ab6bfb7ea6f66c1d210da49888a3483b9944eda2fc56c65; mojo-uuid=52400eb8e81e626cd376f2f156175e87; _lxsdk_cuid=172eed99c32c8-081bfffd57c6c9-3b634404-144000-172eed99c32c8; _lxsdk=23F8EC30B76411EAA2F937AFDFBC83F68905F9E8465D4E31AF7DFCAA143694B9; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593145138,1593159946,1593165477,1593166927; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593166927; __mta=44439323.1593145138428.1593163905352.1593166927463.4; _lxsdk_s=172f04af11d-5dc-bff-d10%7C%7C1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}  
    response = requests.get(pageUrl, headers=headers)
    content = response.text
    print(response.status_code)
    return content

# 解析页面内容获取所需信息
def parseHtml(content):
    tags = bs(content, 'html.parser')
    dlElems = tags.find_all('div', attrs={'class':'movie-hover-info'})
    movieCsvContent = [];
    for i in range(0, 10):
        subElems = dlElems[i].find('span', attrs={'class':'hover-tag'})
        movieTitle = subElems.find_parent().get('title').replace("\n", "").replace(" ", "")
        movieType = subElems.find_parent().text.replace("\n", "").replace(" ", "")
        dateElem = dlElems[i].find('div', attrs={'class':'movie-hover-title movie-hover-brief'})
        movieDateTime = dateElem.text.replace("\n", "").replace(" ", "")
        movieInfo = [movieTitle, movieType, movieDateTime]
        movieCsvContent.append(movieInfo)
    return movieCsvContent
    
# 写入csv文件
def writeCsv(contentList):
    pd.DataFrame(data = movieCsvContent).to_csv('./Python001-class01/week01/homework1/movieInfo.csv', encoding='utf8', index=False, header=False)

# 执行块
cnt = getPageContent()
movieCsvContent = parseHtml(cnt)
writeCsv(movieCsvContent)







