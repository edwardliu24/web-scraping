import scrapy
from scrapy.http import Request
import pandas as pd
from plotly import express as px

class ImdbSpider(scrapy.Spider):
    ## spider class with name "imdb_spider",the url starts with is "https://www.imdb.com/title/tt1533117/?ref_=fn_al_tt_1"
    name = 'imdb_spider'
    
    start_urls = ["https://www.imdb.com/title/tt1533117/?ref_=fn_al_tt_1"]

    def parse(self, response):
        ## Scrape on the initilia page and open the 'cast&crew' link
    
        ##Extract the link of "cast&crew"
        full_credits = response.css("li.ipc-inline-list__item a[href*=fullcredits]").attrib['href']
    
        ##Make the next url
        prefix = "https://www.imdb.com/title/tt1533117/"
        cast_url = prefix + full_credits

        ##Request the parse_full_credits method on the next url
        yield Request(cast_url, callback = self.parse_full_credits)

    def parse_full_credits(self, response):
        ##Find all the actor page of the actors in the movie
    
         ##Get all the links of each ators
        actor_page = [a.attrib["href"] for a in response.css("td.primary_photo a")]
    
        ##Make a list of all the links to actor page
        prefix = "https://www.imdb.com/"
        actor_url = [prefix + suffix for suffix in actor_page]

        ##For each link, open the actor page and call the parse_actor_page method
        for url in actor_url:
            yield Request(url, callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        ##Scrape on the actor page, scrape all the movies that this actor participated,output a dictionary with actor names and movies
    
        ##Scrpae the names of the actor
        name = response.css("h1.header span::text").get()
    
        ##Scrape all the movies that this actor was in
        for movie in response.css("div.filmo-row"):
            movies = movie.css("a::text").get()
        
            ##yield a dictionary
            yield {
                "actor" : name,
                "movies" : movies
            }


