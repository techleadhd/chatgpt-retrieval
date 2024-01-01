import scrapy

class MakersSpider(scrapy.Spider):
    name = 'makers'
    allowed_domains = ['makers.tech']
    start_urls = ['https://makers.tech/']

    def parse(self, response):
    # Example: Extracting article titles and URLs
        for article in response.css('div.article'):
            yield {
                'title': article.css('h2::text').get(),
                'url': article.css('a::attr(href)').get()
            }
        
        # Follow links to next pages (if any)
        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
