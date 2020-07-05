import scrapy
from scrapy.selector import Selector as sl
from maoyanmovie.items import MaoyanmovieItem
import re
import pretty_errors


class MaoyanmovieSpider(scrapy.Spider):
    name = 'maoyanMovie'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/']

    def start_requests(self):
        try:
            context = scrapy.Request(url='https://maoyan.com/films?showType=3', callback=self.parse, dont_filter=False)
            yield context
        except Exception as e:
            print(e)
        finally:
            yield ''
    
    def parse(self, response):
        dlElems = sl(response=response).xpath('//dl/dd')
        if dlElems != '' and dlElems != None :
            for i in range(1, 11):
                mainItem = {}
                # 类型:
                typeStr = str(dlElems.xpath('(//div[@class="movie-hover-title"][2]/span[@class="hover-tag"]/text())[1]')\
                    .extract()).strip('\\n\n[]\' ')
                # 上映时间:
                datetimeStr = str(dlElems.xpath('(//div[@class="movie-hover-title movie-hover-brief"]\
                    /span[@class="hover-tag"]/text())[1]').extract()).strip('\\n\n[]\' ')
                # 电影名称
                movieTitle = dlElems.xpath('(//div[@class="channel-detail movie-item-title"]/@title)[%d]' %i)
                # 电影类型
                movieType = dlElems.xpath('(//div[@class="movie-hover-title"][2]/text())[%d]' %(i*2))
                # 上映时间
                movieDatetime = dlElems.xpath('(//div[@class="movie-hover-title movie-hover-brief"]/text())[%d]' %(i*2))
                # 整成item形式
                mainItem['movieTitle'] = str(movieTitle.extract()).strip('\\n\n[]\' ')
                # 类型:爱情／动画／奇幻
                mainItem['movieType'] = typeStr + str(movieType.extract()).strip('\\n\n[]\' ')
                # 上映时间:2019-11-01
                mainItem['movieDatetime'] = datetimeStr + str(movieDatetime.extract()).strip('\\n\n[]\' ')
                yield mainItem
