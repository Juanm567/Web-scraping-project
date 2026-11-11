import scrapy
from Books.items import BooksItem

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    # For each book, it creates a BooksItem instance and extracts the URL, title, and price using CSS selectors.

    def parse(self, response):
        #Loop through each book on the page and extract the required information
        for book in response.css("article.product_pod"):
            # BooksItem instance to store the extracted data
            item = BooksItem()
            #Data specified in the item fields using CSS selectors in items.py
            item["url"] = book .css("h3 > a::attr(href)").get()
            item["title"] = book .css("h3 > a::attr(title)").get()
            item["price"] = book .css("p.price_color::text").get()
            #yield each item and pause function
            yield item
            #Deal with next pages, get the next page link
        next_page = response.css("li.next > a::attr(href)").get()
        # If there is a next page, it constructs the full URL and makes a request to that page, calling the parse method again to continue scraping.
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)