import scrapy
from scraper.items import ApartmentItem
from scrapy_playwright.page import PageMethod


class SrealitySpider(scrapy.Spider):
    name = 'sreality'
    url = 'https://www.sreality.cz/en/search/for-sale/apartments?page='
    n_pages = 25

    def start_requests(self):
        yield scrapy.Request(self.url+'1', meta=dict(
            playwright=True,
            playwrite_include_page=True,
            playwright_page_methods=[
                PageMethod('wait_for_selector', 'div.dir-property-list')
            ]
        ))

    def scrape_title(self, apartment):
        name = apartment.xpath('.//span[@class="name ng-binding"]/text()').get()
        locality = apartment.xpath('.//span[@class="locality ng-binding"]/text()').get()
        price = apartment.xpath('.//span[@class="norm-price ng-binding"]/text()').get()
        return name+'   |   '+locality+'   |   '+price

    async def parse(self, response):
        apartment_item = ApartmentItem()
        for apartment in response.xpath('//div[@class="property ng-scope"]'):
            apartment_item['title'] = self.scrape_title(apartment)
            apartment_item['image_url'] = apartment.xpath('.//preact/div/div/a/img/@src').get()
            yield apartment_item

        for page in range(2, self.n_pages+1):
            yield response.follow(self.url+str(page), meta=response.meta, callback=self.parse)

