# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd

class MaoyanmoviePipeline:
    def process_item(self, item, spider):
        # movieCsvContent = [item['movieTitle'], item['movieType'], item['movieDatetime']]
        movieCsvContent = [item['movieTitle'] + ',' + item['movieType'] + ',' + item['movieDatetime']]
        #movieCsvContent = '{a},{b},{c}'.format(a=item['movieTitle'], b=item['movieType'], c=item['movieDatetime']) # %(item['movieTitle'], item['movieType'], item['movieDatetime'])
        print(movieCsvContent)
        pd.DataFrame(data = movieCsvContent).to_csv('movieInfo2.csv', 
            encoding='utf8', index=False, header=False, mode='a')
        return item
