import scrapy
from ivooscraper.items import IvooscraperItem
from ivooscraper.itemsloaders import IvooProductLoader

class IvoospiderSpider(scrapy.Spider):
    name = "ivoospider"
    allowed_domains = ["www.ivoo.com"]
    start_urls = ["https://www.ivoo.com/computacion.html"]

    def parse(self, response):
        products = response.css(".product-items")
        for product in products:
            ivoo = IvooProductLoader(item=IvooscraperItem(), selector=product)
            ivoo.add_css("name", ".product-item-link::text")
            ivoo.add_css("price", ".price::text")
            ivoo.add_css("url", ".product-item-link ::attr(href)")
            yield ivoo.load_item()

        next_page = response.css(".pages-item-next a.next::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
