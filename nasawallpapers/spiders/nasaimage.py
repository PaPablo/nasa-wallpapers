import scrapy
from nasawallpapers.items import NasaImage


class NasaSpider(scrapy.Spider):
    name = "nasawallpaper"

    urls = [
        'https://www.nasa.gov/multimedia/imagegallery/index.html',
    ]

    base_url = 'https://www.nasa.gov'

    def start_requests(self):

        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        image_galleries = \
            '//div/h3[text()="Mission Galleries"]/parent::div/ul/li/a/@href'

        self.logger.info(response.xpath(image_galleries))

        galleries = response.xpath(image_galleries)

        for g in galleries:
            gallery_url = '{}{}'.format(self.base_url, g.get())
            yield response.follow(url=gallery_url, callback=self.parse_gallery)

    def parse_gallery(self, response):
        image_selector = '//div[@class="image"]/img/@src'

        images = response.xpath(image_selector)

        for i in images:
            url = '{}{}'.format(self.base_url, i.get())

            self.logger.info(url)
            yield NasaImage(image_urls=[url])
