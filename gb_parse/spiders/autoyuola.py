import scrapy


class AutoyuolaSpider(scrapy.Spider):
    name = "autoyuola"
    allowed_domains = ["auto.youla.ru"]
    start_urls = ["https://auto.youla.ru/"]
    css_query = {
        "brands": "div.TransportMainFilters_brandsList__2tIkv div.ColumnItemList_container__5gTrc a.blackLink",
        "pagination": "div.Paginator_block__2XAPy a.Paginator_button__u1e7D",
        "ads": "div.SerpSnippet_titleWrapper__38bZM a.blackLink",
    }

    data_query = {
        "title": "div.AdvertCard_advertTitle__1S1Ak::text",
        "price": "div.AdvertCard_price__3dDCr::text",
        "description": "div.AdvertCard_descriptionInner__KnuRi::text",
    }

    @staticmethod
    def gen_tasks(response, link_list, callback):
        for link in link_list:
            yield response.follow(link.attrib.get("href"), callback=callback)

    def parse(self, response):
        yield from self.gen_tasks(
            response, response.css(self.css_query["brands"]), self.brand_parse
        )

    def brand_parse(self, response):
        yield from self.gen_tasks(
            response, response.css(self.css_query["pagination"]), self.brand_parse
        )
        yield from self.gen_tasks(response, response.css(self.css_query["ads"]), self.ads_parse)

    def ads_parse(self, response):
        data = {}
        for key, query in self.data_query.items():
            data[key] = response.css(query).get()

