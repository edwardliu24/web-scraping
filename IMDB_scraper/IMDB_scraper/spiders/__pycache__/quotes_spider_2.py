import scrapy

'''
1. from terminal, run:
scrapy shell "https://quotes.toscrape.com/page/1/"
to understand the different Python objects that scrapy gives you.

2. from terminal, run:
scrapy startproject tutorial
to create the framework.

3. inside tutorial > tutorial > spiders folder,
make this quotes_spider.py file 
'''





class QuotesSpider1(scrapy.Spider):
    name = "quotes1" # each spider class needs unique name

    # needs urls to start scraping/crawling from
    start_urls=["https://quotes.toscrape.com/page/1/",
    "https://quotes.toscrape.com/page/2/"]

    # needs a parse method to know what to do with the response object
    # this response object is the same one that we saw on 
    # terminal
    def parse(self, response):
        page_num = response.url.split("/")[-2]
        filename = f'quotes-{page_num}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

'''
4. from terminal, run:
scrapy crawl quotes1
and check that you now have html files
'''

class QuotesSpider2(scrapy.Spider):
    name = "quotes2" # each spider class needs unique name

    # needs urls to start scraping/crawling from
    start_urls=["https://quotes.toscrape.com/page/1/",
    "https://quotes.toscrape.com/page/2/"]

    # needs a parse method to know what to do with the response object
    # this response object is the same one that we saw on 
    # terminal
    def parse(self, response):

        # response.css('div.quote') 
        # returns a iterator through all the div elements with class quote
        for quote in response.css('div.quote'):
            text = quote.css("span.text::text").get()

            author = quote.css("small.author::text").get()
            tags = quote.css("div.tags a.tag::text").getall()
            tags = ",".join(tags)
            
            yield {
                "text": text,
                "author": author,
                "tags" : tags
            }

'''
5. from terminal, run:
scrapy crawl quotes2 -o quotes.csv
and check that quotes.csv file is made
'''        

class QuotesSpider3(scrapy.Spider):
    name = "quotes3"

    start_urls = ["https://quotes.toscrape.com/page/1/"]

    def parse(self, response):
        for quote in response.css('div.quote'):
            text = quote.css("span.text::text").get()

            author = quote.css("small.author::text").get()
            tags = quote.css("div.tags a.tag::text").getall()
            tags = ",".join(tags)
            
            yield {
                "text": text,
                "author": author,
                "tags" : tags
            }

        next_page = response.css("li.next a").attrib["href"]

        if next_page: # identical to if next_page is not None
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

'''
6. from terminal, run:
scrapy crawl quotes3 -o quotes-all.csv
and check that quotes-all.csv file is made

Turns out there are 10 pages and each pages have 10 quotes
'''      