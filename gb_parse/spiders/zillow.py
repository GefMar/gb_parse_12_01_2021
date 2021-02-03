import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class ZillowSpider(scrapy.Spider):
    name = 'zillow'
    allowed_domains = ['www.zillow.com']
    start_urls = ["https://www.zillow.com/san-francisco-ca/"]
    browser = webdriver.Firefox()

    def parse(self, response):
        for pag_url in response.xpath("//div[@class='search-pagination']/nav/ul/li/a/@href"):
            yield response.follow(pag_url, callback=self.parse)
        for ads_url in response.xpath("//ul[contains(@class, 'photo-cards')]/li/article/div/a[contains(@class, 'list-card-link')]"):
            yield response.follow(ads_url, callback=self.ads_parse)
    
    def ads_parse(self, response):
        self.browser.get(response.url)
        media_col = self.browser.find_element_by_xpath('//div[contains(@class, "ds-media-col")]')
        len_photos = len(media_col.find_elements_by_xpath("//picture[contains(@class, 'media-stream-photo')]/source"))
        while True:
            for _ in range(5):
                media_col.send_keys(Keys.PAGE_DOWN)
            photos = media_col.find_elements_by_xpath("//picture[contains(@class, 'media-stream-photo')]/source")
            if len_photos == len(photos):
                break
            len_photos = len(photos)
        
        print(1)
