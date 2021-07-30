import json
from urlparse import urljoin

import scrapy
from scrapy import Spider

from fang.items import FangItem


class LianJiaSpider(Spider):
    name = "lianjia"
    allowed_domains = ["lianjia.com"]
    start_urls = [
        "https://sh.lianjia.com/ershoufang/sanlin/a3a4/",
        "https://sh.lianjia.com/ershoufang/jinqiao/a3a4/"
    ]

    def parse(self, response):
        base_url = "https://sh.lianjia.com"
        for sel in response.xpath('//ul/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]'):
            item = FangItem()
            item['id'] = sel.xpath('a/@data-housecode').extract_first()
            item['link'] = sel.xpath('a/@href').extract_first()
            info = sel.xpath('div[@class="info clear"]')
            item['title'] = info.xpath('div[@class="title"]/a/text()').extract_first()
            item['xiaoqu'] = info.xpath('div[@class="flood"]/div[@class="positionInfo"]/a[contains(@href, "xiaoqu")]/text()').extract_first()
            item['region'] = info.xpath('div[@class="flood"]/div[@class="positionInfo"]/a[contains(@href, "ershoufang")]/text()').extract_first()
            house_info = info.xpath('div[@class="address"]/div[@class="houseInfo"]/text()').extract_first()
            house_info = [i.strip() for i in house_info.split("|")]
            item['rooms'] = house_info[0]
            item['area'] = house_info[1]
            item['toward'] = house_info[2]
            item['floor'] = house_info[4]
            item['year'] = house_info[5]
            item['price'] = int(info.xpath('div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()').extract_first())
            item['unit'] = int(info.xpath('div[@class="priceInfo"]/div[@class="unitPrice"]/@data-price').extract_first())
            item['tag'] = ",".join(info.xpath('div[@class="tag"]/span/text()').extract())
            yield item

        page_data = response.css('div::attr(page-data)').extract_first()
        page_url = response.css('div::attr(page-url)').extract_first()
        if page_data and page_url:
            page_data = json.loads(page_data)
            total_page = page_data.get("totalPage", 0)
            cur_page = page_data.get("curPage", 0)
            next_page = cur_page + 1
            if next_page <= total_page:
                page_url = page_url.format(page=next_page)
                next_page = urljoin(base_url, page_url)
                yield scrapy.Request(next_page, callback=self.parse)
