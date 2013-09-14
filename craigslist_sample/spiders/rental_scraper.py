from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from craigslist_sample.items import CraigslistSampleItem
from scrapy.http.request import Request

from scrapy.item import Item, Field
import re

class MySpider(BaseSpider):
    name = "craig"
    allowed_domains = ["craigslist.org"]
    start_urls = ["http://boston.craigslist.org/search/nfa?query=somerville&zoomToPosting=&minAsk=1000&maxAsk=1700&bedrooms=1&housing_type="]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//p")
        items = []

        import pdb; pdb.set_trace()
        next_page = hxs.select('//span[@title="next page"]/a/@href').extract()
        if not not next_page:
            yield Request(next_page[0], self.parse)

        for titles in titles:
            item = CraigslistSampleItem()
            item['date'] = titles.select('span[@class="pl"]/span[@class="date"]/text()').extract()
            item ["title"] = titles.select('span[@class="pl"]/a/text()').extract()
            item ["link"] = titles.select('span[@class="pl"]/a/@href').extract()
            item ['price'] = titles.select('span[@class="l2"]/span[@class="price"]/text()').extract()
            item['location'] = titles.select('span[@class="l2"]/span[@class="pnr"]/small/text()').extract()
            item['bedrooms'] = titles.select('span[@class="l2"]/text()').extract()           
            if self.is_valid(item):
                items.append(item)
        for item in items:
		    yield item

    def is_valid(self, item):
        #first check if location actually has somerville in it
        regex = re.compile("\(.*Somerville.*\)",re.IGNORECASE)
        r = regex.search(str(item['location']))
        if not r:
            return False
        
        #check for bedrooms
        for bedroom_text in item['bedrooms']:
            decoded = bedroom_text.encode('utf8')
            index = str(decoded).find('1br')
            if index >= 0:
                return True
        return False
                
