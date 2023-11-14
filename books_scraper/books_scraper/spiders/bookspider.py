import scrapy
import pandas as pd


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        urls_books = response.css('article.product_pod h3 a::attr(href)').getall()
        
        for urls in urls_books:
            yield response.follow(urls, callback = self.parse_book_page)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback = self.parse)

    def parse_book_page(self,response):
        # xpath for title: response.xpath('//div[@class="col-sm-6 product_main"]/h1/text()').get()
        # xpath for price: response.xpath('//div[@class="col-sm-6 product_main"]/p/text()').get() 
        # xpath for description : response.xpath('//article/p[not(@class)]/text()').get()
        # xpath for stars : response.xpath('//p[contains(@class, "star-rating")]/@class').get()
        tabla = response.xpath('//table//td/text()').getall()
        
        yield {
            'url' : response.url,
            'title' : response.xpath('//div[@class="col-sm-6 product_main"]/h1/text()').get(),
            'price' : response.xpath('//div[@class="col-sm-6 product_main"]/p/text()').get(),
            'stars' : response.xpath('//p[contains(@class, "star-rating")]/@class').get(),
            'description' : response.xpath('//article/p[not(@class)]/text()').get(),
            'upc' : tabla[0],
            'product_type' : tabla[1],
            'price_excl_tax' : tabla[2],
            'price_incl_tax' : tabla [3],
            'tax' : tabla [4],
            'availability' : tabla [5],
            'number_of_reviews' : tabla [6]
        }