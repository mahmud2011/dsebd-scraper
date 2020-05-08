from apscheduler.schedulers.twisted import TwistedScheduler
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from scrapperArchive.spiders.DayEndArchiveSpider import DayEndArchiveSpider
from scrapperArchive.spiders.DseMarketSummarySpider import DseMarketSummarySpider
from scrapperArchive.spiders.TickerSpider import TickerSpider


def schedule_method():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner(get_project_settings())
    runner.crawl(TickerSpider)
    runner.join()


sched = TwistedScheduler()
sched.add_job(schedule_method, trigger='cron', second="*/5", hour="10-16")


def schedule_archive_method():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner(get_project_settings())
    runner.crawl(DseMarketSummarySpider)
    runner.crawl(DayEndArchiveSpider)
    runner.join()


sched.add_job(schedule_archive_method, trigger='cron', hour="18")

sched.start()
reactor.run()
