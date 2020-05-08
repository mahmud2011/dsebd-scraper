from datetime import datetime, date

from scrapy import Spider, FormRequest
from scrapy.selector import Selector

from scrapperArchive.items import DayEndArchiveItem


# Dev


class DayEndArchiveSpider(Spider):
    name = "dayendarchive"
    urls = [
        "http://www.dsebd.org/day_end_archive.php",
    ]

    def start_requests(self):
        currentDate = date.today()
        frmdata = {
            # Start Date
            "DayEndSumDate1": str(currentDate),
            'DayEndSumDate1_dp': '1',
            "DayEndSumDate1_year_start": '2016',
            "DayEndSumDate1_year_end": str(currentDate.year),
            "DayEndSumDate1_sna": '1',
            "DayEndSumDate1_inp": '1',
            "DayEndSumDate1_fmt": 'j F Y',
            "DayEndSumDate1_spt": '0',
            "DayEndSumDate1_str": '0',
            "DayEndSumDate1_int": '1',
            "DayEndSumDate1_hid": '1',
            "DayEndSumDate1_hdt": '1000',
            # Start Day
            "DayEndSumDate1_day": str(currentDate.day),
            # Start Month
            "DayEndSumDate1_month": str(currentDate.month),
            # Start Year
            "DayEndSumDate1_year": str(currentDate.year),
            # End Date
            "DayEndSumDate2": str(currentDate),
            "DayEndSumDate2_dp": '1',
            "DayEndSumDate2_year_start": '2016',
            "DayEndSumDate2_year_end": str(currentDate.year),
            "DayEndSumDate2_sna": '1',
            "DayEndSumDate2_inp": '1',
            "DayEndSumDate2_fmt": 'j F Y',
            "DayEndSumDate2_spt": '0',
            "DayEndSumDate2_str": '0',
            "DayEndSumDate2_int": '1',
            "DayEndSumDate2_hid": '1',
            "DayEndSumDate2_hdt": '1000',
            # End Day
            "DayEndSumDate2_day": str(currentDate.day),
            # End Month
            "DayEndSumDate2_month": str(currentDate.month),
            # End Year
            "DayEndSumDate2_year": str(currentDate.year),
            "Symbol": 'All Instrument',
            "ViewDayEndArchive": 'View Day End Archive'
        }
        yield FormRequest(self.urls[0], callback=self.parse, formdata=frmdata)

    def parse(self, response):
        # inspect_response(response, self)

        table = response.xpath('//table[@bgcolor="#808000"]')

        list_tr = table.xpath('tr').extract()

        for _ in list_tr[1:]:
            tr = Selector(text=_)
            list_td = tr.xpath('//td').extract()

            td = Selector(text=list_td[1])
            item = DayEndArchiveItem()
            item['date'] = td.xpath('//font/text()').extract_first()
            item['date'] = datetime.strptime(item['date'], '%Y-%m-%d')

            td = Selector(text=list_td[2])
            item['trading_code'] = td.xpath('//font/text()').extract_first()

            td = Selector(text=list_td[3])
            item['last_traded_price'] = float(td.xpath('//font/text()').extract_first().replace(",", ""))

            td = Selector(text=list_td[4])
            item['high'] = float(td.xpath('//font/text()').extract_first().replace(",", ""))

            td = Selector(text=list_td[5])
            item['low'] = float(td.xpath('//font/text()').extract_first().replace(",", ""))

            td = Selector(text=list_td[6])
            item['opening_price'] = float(td.xpath('//font/text()').extract_first().replace(",", ""))

            td = Selector(text=list_td[7])
            item['closing_price'] = float(td.xpath('//font/text()').extract_first().replace(",", ""))

            td = Selector(text=list_td[8])
            item['yesterdays_closing_price'] = float(td.xpath('//font/text()').extract_first().replace(",", ""))

            td = Selector(text=list_td[9])
            item['trade'] = int(td.xpath('//font/text()').extract_first().replace(",", ""))

            td = Selector(text=list_td[10])
            item['value_mn'] = float(td.xpath('//font/text()').extract_first().replace(",", ""))

            td = Selector(text=list_td[11])
            item['volume'] = int(td.xpath('//font/text()').extract_first().replace(",", ""))

            yield item
