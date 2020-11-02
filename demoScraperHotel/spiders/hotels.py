import scrapy
from scrapy_splash import SplashRequest


class HotelsSpider(scrapy.Spider):
    name = 'hotels'
    start_urls = [
        'https://myreservations.omnibees.com/default.aspx?q=3073&lang=es-ES#/&diff=false&CheckIn=02112020&CheckOut=16112020&Code=&group_code=&loyality_card=&NRooms=1&ad=1&ch=0&ag=-'
    ]

    custom_settings = {
       'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                                endpoint='render.html',
                                args={'wait': 0.5},
                                )

    def parse(self, response):
        names = response.xpath(
            '//td[@class="colExcerpt"]//div[@class="roomExcerpt"]/div[@class="excerpt"]/h5/a/text()').getall()
        #prices = response.xpath(
            #'//td[@class="colExcerpt"]//div[@class="roomExcerpt"]/div[contains(@class, "sincePrice")]/div[@class="sincePriceContent"]/h6/text()').getall()

        for i in range(len(names)):

            conditions_prices = []
            conditions = response.xpath('//tr[contains(@class,"item jsRoom_'+ str(i) +' jsRoom")]/td[@class="col_2 rates_col2"]/div[@class="wrapRateInfo"]//div[@class="rateName"]/a/text()').getall()
            conditions_extras = response.xpath('//tr[contains(@class,"item jsRoom_'+ str(i) +' jsRoom")]/td[@class="col_2 rates_col2"]/div[@class="wrapRateInfo"]//span[@class="extras extrasAndPoliciesResultsColor"]/a/text()').getall()

            prices_promotions = response.xpath('//tr[contains(@class,"item jsRoom_'+ str(i) +' jsRoom")]/td[@class="col_3 rates_col3"]/table[@class="ratePriceTable"]//a[@class="price_tooltip pricesResultsTextColor"]/text()').getall()            

            for j in range(len(conditions)):
                conditions_prices.append({
                    'name_rate': conditions[j],
                    'features_rate': conditions_extras,
                    'price_rate': prices_promotions[j]
                })

            yield{
                'fecha_arrival_withoutFormat': '02112020',
                'fecha_departure_withoutFormat': '16112020',
                'names': names[i],
                #'prices': prices[i],
                'conditions_prices': conditions_prices
            }
           

  