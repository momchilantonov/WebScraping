import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class EmagTvSpider(CrawlSpider):
    name = 'emag_tv'
    allowed_domains = ['www.emag.bg']
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.emag.bg/televizori/c?ref=hp_menu_quick-nav_320_1&type=link/', headers={
            'user-agent': self.user_agent
        })

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths='//div[contains(@id , "card_grid")]/'
                                'div[contains(@class, "card-item")]/'
                                'div[contains(@class, "card")]/'
                                'div[contains(@class, "card-section-wrapper")]/'
                                'div[contains(@class, "card-section-mid")]/'
                                'h2/'
                                'a'
            ),
            callback='parse_item',
            follow=True,
            process_request='set_user_agent',
        ),
        Rule(
            LinkExtractor(restrict_xpaths='//a[contains(@aria-label, "Next")]'),
            process_request='set_user_agent',
        )
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        header = response.xpath('//div[contains(@class, "page-header")]')
        body = response.xpath('//div[contains(@class, "product-page-pricing")]')

        yield {
            'title': header.xpath('./h1/text()').get().strip(),
            'code': header.xpath('./div/div/span/text()').get(),
            'price': body.xpath('./div/div/div/p/text()').get().strip(),
            'status': body.xpath('./span/text()').get(),
            'url': response.url,
        }
