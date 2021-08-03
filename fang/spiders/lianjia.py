import json
from datetime import datetime
from urlparse import urljoin

import scrapy
from scrapy import Spider

from fang.items import FangItem


class LianJiaSpider(Spider):
    name = "lianjia"
    allowed_domains = ["lianjia.com"]
    start_urls = [
        "https://sh.lianjia.com/ershoufang/pudong/mw1sf1l2l3a3a4bp450ep600/",
    ]

    def parse(self, response):
        base_url = "https://sh.lianjia.com"
        for sel in response.xpath('//ul/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]'):
            item = FangItem()
            item['id'] = sel.xpath('@data-lj_action_housedel_id').extract_first()
            item['link'] = sel.xpath('a/@href').extract_first()
            info = sel.xpath('div[@class="info clear"]')
            item['title'] = info.xpath('div[@class="title"]/a/text()').extract_first().strip()
            item['xiaoqu'] = info.xpath('div[@class="flood"]/div[@class="positionInfo"]/a[contains(@href, "xiaoqu")]/text()').extract_first().strip()
            item['region'] = info.xpath('div[@class="flood"]/div[@class="positionInfo"]/a[contains(@href, "ershoufang")]/text()').extract_first().strip()
            house_info = info.xpath('div[@class="address"]/div[@class="houseInfo"]/text()').extract_first()
            house_info = [i.strip() for i in house_info.split("|")]
            item['rooms'] = house_info[0].strip()
            item['area'] = house_info[1].strip()
            item['toward'] = house_info[2].strip()
            item['floor'] = house_info[4].strip()
            item['year'] = house_info[5].strip()
            item['price'] = float(info.xpath('div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()').extract_first().strip())
            item['unit'] = float(info.xpath('div[@class="priceInfo"]/div[@class="unitPrice"]/@data-price').extract_first().strip())
            item['tag'] = ",".join([i.strip() for i in info.xpath('div[@class="tag"]/span/text()').extract()])
            item['last_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
