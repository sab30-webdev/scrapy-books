import scrapy


class BooksSpider(scrapy.Spider):
    name = "book"
    start_urls = [
        "https://books.toscrape.com/catalogue/category/books_1/index.html"
    ]

    def parse(self, response):
        for s in response.xpath('//li[@class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]'):
            l = s.xpath('article/h3/a/@href').get()
            yield response.follow(url=l, callback=self.parse_book)

        yield response.follow(response.xpath('//li[@class="next"]/a/@href').get(), callback=self.parse)

    def parse_book(self, response):
        yield{
            "name": response.xpath('//div[@class="col-sm-6 product_main"]/h1/text()').get(),
            "price": response.xpath('//div[@class="col-sm-6 product_main"]/p[1]/text()').get()
        }
