from scrapy.item import Item, Field


class DseMarketSummaryItem(Item):
    date = Field()
    dsex_index = Field()
    dsex_index_change = Field()
    ds30_index = Field()
    ds30_index_change = Field()
    total_trade = Field()
    total_value_taka_mn = Field()
    total_volume = Field()
    total_market_cap_taka_mn = Field()


class DayEndArchiveItem(Item):
    date = Field()
    trading_code = Field()
    last_traded_price = Field()
    high = Field()
    low = Field()
    opening_price = Field()
    closing_price = Field()
    yesterdays_closing_price = Field()
    trade = Field()
    value_mn = Field()
    volume = Field()


class TickerItem(Item):
    timeStamp = Field()
    trading_code = Field()
    last_traded_price = Field()
    change_percentage = Field()
    change = Field()
    url = Field()
    status = Field()


class CategoryItem(Item):
    trading_code = Field()
    sector = Field()
    instrument_type = Field()
