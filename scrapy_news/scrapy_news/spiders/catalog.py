import scrapy


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    allowed_domains = ['russia24.pro']
    start_urls = ['https://russia24.pro/news/']

    def start_requests(self):
        for page in range(288820000,288930000):
            url = f'https://russia24.pro/news/_ajax/showmore/?from={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        time = response.xpath('//time/@datetime').extract_first()
        time = time.split('-')
        if time[0] == '2021' and time[1] in ['06']:
            for href in response.css('.r24_body a::attr("href")').extract():
                url = response.urljoin(href)
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        item = {
            'title': response.css('h1::text').extract_first('').strip(),
            # 'desc': response.css('.r24_text::text').extract_first('').strip(),
            'time': response.xpath('//time/@datetime').extract_first(),}
        yield item