import scrapy
from books_scraper.items import BookItem

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
        # xpath for category : response.xpath('//ul[@class="breadcrumb"]/li[3]/a/text()').get()
        tabla = response.xpath('//table//td/text()').getall()
        book_item = BookItem()
                
        book_item['url'] = response.url
        book_item['title'] = response.xpath('//div[@class="col-sm-6 product_main"]/h1/text()').get()
        book_item['price'] = response.xpath('//div[@class="col-sm-6 product_main"]/p/text()').get()
        book_item['stars'] = response.xpath('//p[contains(@class, "star-rating")]/@class').get()
        book_item['description'] = response.xpath('//article/p[not(@class)]/text()').get()
        book_item['upc'] = tabla[0]
        book_item['product_type'] = tabla[1]
        book_item['price_excl_tax'] = tabla[2]
        book_item['price_incl_tax'] = tabla [3]
        book_item['tax'] = tabla [4]
        book_item['availability'] = tabla [5]
        book_item['number_of_reviews'] = tabla [6]
        book_item['category'] = response.xpath('//ul[@class="breadcrumb"]/li[3]/a/text()').get()
        

        yield book_item