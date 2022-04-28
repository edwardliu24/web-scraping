import scrapy
from scrapy.http import Request
import pands as pd
from plotly import express as px

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ["https://www.imdb.com/title/tt1533117/?ref_=fn_al_tt_1"]

    def parse(self, response):
        full_credits = response.css("li.ipc-inline-list__item a[href*=fullcredits]").attrib['href']
        prefix = "https://www.imdb.com/title/tt1533117/"
        cast_url = prefix + full_credits

        yield Request(cast_url, callback = self.parse_full_credits)

    def parse_full_credits(self, response):

        actor_page = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        prefix = "https://www.imdb.com/"
        actor_url = [prefix + suffix for suffix in actor_page]

        for url in actor_url:
            yield Request(url, callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        name = response.css("h1.header span::text").get()
        for movie in response.css("div.filmo-row"):
            movies = movie.css("a::text").get()

            yield {
                "actor" : name,
                "movies" : movies
            }

result = pd.read_csv("results.csv")
df = result.value_counts(['movies'])
df =pd.DataFrame(df)
df =df.reset_index()
df.columns = ['movies','number of shared actors']
fig = px.scatter(data_frame = df, 
                 x = 'movies',
                 y = 'number of shared actors', 
                 width = 1500,
                 height = 300)
