# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.cmdline import execute
from t66y.items import T66YItem


class A1024Spider(scrapy.Spider):
    name = '1024'
    allowed_domains = ['t66y.com']
    start_urls = ['http://t66y.com/thread0806.php?fid=22&search=&page=1']

    def parse(self, response):
        # name = response.xpath('//div[@class="t t2"][1]//h4/text()').extract_first()
        # video_url = response.xpath('//div[@class="tpc_content do_not_catch"]/a[2]/@onclick').extract_first()
        # video_url = video_url.split('=')[-1][1:-1]
        # item = T66YItem(name=name, video_url=video_url)
        # yield item
        tr_list = response.xpath('//tr[@class="tr3 t_one tac"]')

        for tr in tr_list:
            url = tr.xpath('.//td[1]/a/@href').extract_first()
            html_url = "http://t66y.com/" + str(url)
            yield scrapy.Request(url=html_url, callback=self.next_page)
        next_ = Selector(response).re('<a href="(\S*)">下一頁</a>')[0].replace('&amp;', '&')
        if next_:
            yield scrapy.Request(url="http://t66y.com/" + next_, callback=self.parse)

    def next_page(self, response):
        name = response.xpath('//div[@class="t t2"][1]//h4/text()').extract_first()
        video_url = response.xpath('//div[@class="tpc_content do_not_catch"]/a[2]/@onclick').extract_first()
        video_url = video_url.split('=')[-1][1:-1].replace(" ", "")
        item = T66YItem(name=name, video_url=video_url)
        yield item


if __name__ == '__main__':
    execute(["scrapy", "crawl", "1024"])
