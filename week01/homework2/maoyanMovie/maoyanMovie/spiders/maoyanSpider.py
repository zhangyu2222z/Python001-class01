import scrapy
from scrapy.selector import Selector as sl
from maoyanMovie.items import MaoyanmovieItem

class MaoyanspiderSpider(scrapy.Spider):
    name = 'maoyanSpider'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']

    def start_requests(self):
        context = scrapy.Request(url='https://maoyan.com/films?showType=3', callback=self.parse, dont_filter=False)
        yield context

    def parse(self, response):
        dlElems = sl(response=response).xpath('//dl/dd')
        for i in range(1, 11):
            mainItem = {}
            movieTitle = dlElems.xpath('(//div[@class="channel-detail movie-item-title"]/@title)[%d]' %i)
            movieType = dlElems.xpath('(//div[@class="movie-hover-title"][2]/text())[%d]' %(i*2))
            movieDatetime = dlElems.xpath('(//div[@class="movie-hover-title movie-hover-brief"]/text())[%d]' %(i*2))
            mainItem['movieTitle'] = str(movieTitle.extract()).replace('\\n', '').replace('\n', '').replace(' ', '').replace('[', '').replace(']', '').replace('\'', '')
            mainItem['movieType'] = str(movieType.extract()).replace('\\n', '').replace('\n', '').replace(' ', '').replace('[', '').replace(']', '').replace('\'', '')
            mainItem['movieDatetime'] = str(movieDatetime.extract()).replace('\\n', '').replace('\n', '').replace(' ', '').replace('[', '').replace(']', '').replace('\'', '')
            yield mainItem


        
