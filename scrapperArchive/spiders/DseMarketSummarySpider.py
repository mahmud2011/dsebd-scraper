from datetime import datetime, date

from scrapy import Spider, FormRequest
from scrapy.selector import Selector

from scrapperArchive.items import DseMarketSummaryItem


# Dev


class DseMarketSummarySpider(Spider):
    name = "dsemarketsummary"
    allowed_domains = ["dsebd.org"]
    urls = [
        "http://www.dsebd.org/market_summary.php",
    ]

    def start_requests(self):
        currentDate = date.today()
        frmdata = {
            # Start Date
            "MktSumDate1": str(currentDate),
            "MktSumDate1_dp": '1',
            "MktSumDate1_year_start": '2016',
            "MktSumDate1_year_end": str(currentDate.year),
            "MktSumDate1_sna": '1',
            "MktSumDate1_inp": '1',
            "MktSumDate1_fmt": 'j+F+Y',
            "MktSumDate1_pth": 'calendar%2F',
            "MktSumDate1_spd": '%5B%5B%5D%2C%5B%5D%2C%5B%5D%5D',
            "MktSumDate1_spt": '0',
            "MktSumDate1_str": '0',
            "MktSumDate1_int": '1',
            "MktSumDate1_hid": '1',
            "MktSumDate1_hdt": '1000',
            # Start Day
            "MktSumDate1_day": str(currentDate.day),
            # Start Month
            "MktSumDate1_month": str(currentDate.month),
            # Start Year
            "MktSumDate1_year": str(currentDate.year),
            # End Date
            "MktSumDate2": str(currentDate),
            "MktSumDate2_dp": '1',
            "MktSumDate2_year_start": '2016',
            "MktSumDate2_year_end": str(currentDate.year),
            "MktSumDate2_sna": '1',
            "MktSumDate2_inp": '1',
            "MktSumDate2_fmt": 'j+F+Y',
            "MktSumDate2_pth": 'calendar%2F',
            "MktSumDate2_spd": '%5B%5B%5D%2C%5B%5D%2C%5B%5D%5D',
            "MktSumDate2_spt": '0',
            "MktSumDate2_str": '0',
            "MktSumDate2_int": '1',
            "MktSumDate2_hid": '1',
            "MktSumDate2_hdt": '1000',
            # End Day
            "MktSumDate2_day": str(currentDate.day),
            # End Month
            "MktSumDate2_month": str(currentDate.month),
            # End Year
            "MktSumDate2_year": str(currentDate.year),
            "ViewMktSum": 'View+Market+Summary'
        }
        yield FormRequest(self.urls[0], callback=self.parse, formdata=frmdata)

    def parse(self, response):
        tables = response.xpath('//table[@bgcolor="#808000"]')

        for table in tables:
            list_tr = table.xpath('tr').extract()
            tr = Selector(text=list_tr[0])

            item = DseMarketSummaryItem()

            item['date'] = tr.xpath('//font/text()').extract_first()[len("Market Summary of "):].replace(",", "")
            item['date'] = datetime.strptime(item['date'], '%b %d %Y')

            tr = Selector(text=list_tr[1])

            list_td = tr.xpath('//td').extract()
            td = Selector(text=list_td[1])
            item['dsex_index'] = float(td.xpath('//font/text()').extract_first().replace(",", ""))

            td = Selector(text=list_td[3])
            item['total_trade'] = int(td.xpath('//font/text()').extract_first().replace(",", ""))

            tr = Selector(text=list_tr[2])

            list_td = tr.xpath('//td').extract()
            td = Selector(text=list_td[1])
            item['dsex_index_change'] = float(td.xpath('//font/text()').extract_first().replace(",", ""))
            td = Selector(text=list_td[3])
            item['total_value_taka_mn'] = float(td.xpath('//font/text()').extract_first().replace(",", ""))

            tr = Selector(text=list_tr[3])

            list_td = tr.xpath('//td').extract()
            td = Selector(text=list_td[1])
            item['ds30_index'] = float(td.xpath('//font/text()').extract_first().replace(",", ""))
            td = Selector(text=list_td[3])
            item['total_volume'] = int(td.xpath('//font/text()').extract_first().replace(",", ""))

            tr = Selector(text=list_tr[4])

            list_td = tr.xpath('//td').extract()
            td = Selector(text=list_td[1])
            item['ds30_index_change'] = float(td.xpath('//font/text()').extract_first().replace(",", ""))
            td = Selector(text=list_td[3])
            item['total_market_cap_taka_mn'] = float(td.xpath('//text()').extract_first().replace(",", ""))

            yield item
