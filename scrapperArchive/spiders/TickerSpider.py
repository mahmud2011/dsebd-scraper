from datetime import datetime

from scrapy import Spider, Request

from scrapperArchive.items import TickerItem


# Dev


class TickerSpider(Spider):
    name = "ticker"
    urls = [
        'http://www.dsebd.org/',
    ]

    def start_requests(self):
        for url in self.urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        list_td = response.xpath('//marquee[@id="mq2"]/table/tr/td')
        for td in list_td:
            item = TickerItem()

            item['timeStamp'] = datetime.now()

            anchor = td.xpath('table/tr/td/a')

            sub_url = anchor.xpath('@href').extract_first()
            main_url = response.urljoin(sub_url)
            item['url'] = main_url

            data = " ".join(anchor.xpath('text()').extract())
            # item['data'] = " ".join(data.split())
            new_data = data.split()

            item['trading_code'] = new_data[0]
            item['last_traded_price'] = float(new_data[1])
            item['change'] = float(new_data[2])
            item['change_percentage'] = float(new_data[3].replace('%', ''))

            status = anchor.xpath('img/@src').extract_first()
            if "tkupdown" in status:
                item['status'] = "Neutral"
            elif "up" in status:
                item['status'] = "Up"
            else:
                item['status'] = "Down"

            yield item
