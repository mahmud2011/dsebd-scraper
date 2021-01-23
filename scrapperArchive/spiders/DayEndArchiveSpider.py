from datetime import datetime, date
from scrapy import Spider, Request
from scrapy.selector import Selector
from scrapperArchive.items import DayEndArchiveItem


class DayEndArchiveSpider(Spider):
    start_date = date.today()
    end_date = date.today()

    name = "dayendarchive"
    urls = [
        'https://www.dsebd.org/day_end_archive.php?startDate=' + start_date + '&endDate=' + end_date + '&inst=All%20Instrument&archive=data',
    ]

    def start_requests(self):
        yield Request(url=self.urls[0], callback=self.parse)

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        table = response.xpath("//table[@class='table table-bordered background-white shares-table fixedHeader']")

        list_tr = table.xpath('.//tr')

        for tr in list_tr[1:]:
            list_td = tr.xpath('.//td')
            
            item = DayEndArchiveItem()
            item['date'] = datetime.strptime(list_td[1].xpath('text()').extract_first(), '%Y-%m-%d')
            item['trading_code'] = list_td[2].xpath('.//a/text()').extract_first().strip()
            item['last_traded_price'] = float(list_td[3].xpath('text()').extract_first().replace(",", ""))
            item['high'] = float(list_td[4].xpath('text()').extract_first().replace(",", ""))
            item['low'] = float(list_td[5].xpath('text()').extract_first().replace(",", ""))
            item['opening_price'] = float(list_td[6].xpath('text()').extract_first().replace(",", ""))
            item['closing_price'] = float(list_td[7].xpath('text()').extract_first().replace(",", ""))
            item['yesterdays_closing_price'] = float(list_td[8].xpath('text()').extract_first().replace(",", ""))
            item['trade'] = int(list_td[9].xpath('text()').extract_first().replace(",", ""))
            item['value_mn'] = float(list_td[10].xpath('text()').extract_first().replace(",", ""))
            item['volume'] = int(list_td[11].xpath('text()').extract_first().replace(",", ""))

            yield item
