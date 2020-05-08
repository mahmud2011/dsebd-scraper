from scrapy import Spider

from scrapperArchive.items import CategoryItem


class CategorySpider(Spider):
    name = "category"
    start_urls = ['http://dsebd.org/displayCompany.php?name=' + line.rstrip('\n') for line in
                  open('trading_codes.txt', 'r')]

    def parse(self, response):
        table = response.xpath('//table[@id="company"]')

        item = CategoryItem()
        item['trading_code'] = table[1].xpath('tr')[0].xpath('td/text()')[0].extract()
        item['sector'] = table[7].xpath('tr')[3].xpath('td/text()')[1].extract()
        item['instrument_type'] = table[7].xpath('tr')[1].xpath('td/text()')[1].extract().strip()

        yield item
