import scrapy
from scrapy.linkextractors import LinkExtractor


class TnSpider(scrapy.Spider):
    name = "tn"
    allowed_domains = ["tn.gov"]
    start_urls = ["https://www.tn.gov/careers.html"]

    def parse(self, response):
        page_text = ' '.join(response.css('p::text').getall())
        page_name = response.url.split("/")[-2]        
        with open(f'./crawled_data/{page_name}.txt', 'w', encoding='utf-8') as f:        
            f.write(page_text)

        # Follow only internal links and deny unwanted patterns (like /admin or /login)
        internal_links = LinkExtractor(
            allow_domains=self.allowed_domains, 
            deny=['/admin', '/login']
        ).extract_links(response)
        
        for link in internal_links:
            yield response.follow(link.url, self.parse)