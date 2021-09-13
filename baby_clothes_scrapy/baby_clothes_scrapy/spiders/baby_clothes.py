import scrapy


class BabyClothesSpider(scrapy.Spider):
    name = 'baby_clothes'
    allowed_domains = ['www.matalan.co.uk']
    start_urls = ['https://www.matalan.co.uk/baby/shop-all']

    # def start_requests(self):
    #     yield scrapy.Request(
    #         url='https://www.matalan.co.uk/baby/shop-all',
    #         callback=self.parse,
    #         headers={
    #             'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    #         }
    #     )

    def parse(self, response, **kwargs):
        results = response.xpath('//div[@class="results__detail"]')

        for result in results:
            # garment_name = result.xpath('.//div[@class="results__detail__title u-font--small"]/text()').get()
            garment_name = result.xpath('.//div[contains(@class , "u-font--small")]/text()').get()
            # price = result.xpath('.//div[@class="results__detail__price u-font-wb u-mar-t-tiny@sm-down"]/span/text()').get().strip()
            price = result.xpath('.//div[contains(@class , "u-mar-t-tiny@sm-down")]/span/text()').get().strip()
            # url = result.xpath('.//div[@class="u-dis-flex u-mar-t-small u-space-between"]/a/@href').get()
            url = result.xpath('.//div[contains(@class , "u-space-between")]/a/@href').get()

            absolute_url = response.urljoin(url)
            # relative_url = response.follow(url=url)

            yield {
                'garment_name': garment_name,
                'price': price,
                'url': absolute_url,
            }

        pagination = response.xpath('.//div[contains(@class , "c-pagination-bar u-cf")]')
        next_page_url = pagination.xpath('.//a[contains(@rel , "next")]/@href').get()

        if next_page_url:
            yield response.follow(
                url=next_page_url,
                callback=self.parse,
                # headers={
                #     'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
                # }
            )
