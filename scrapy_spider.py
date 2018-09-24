import scrapy
import re

class ScrapySpider(scrapy.Spider):
  name = 'scrapy'
  start_urls = ['https://markets.businessinsider.com/bonds/finder?currency=814&p=%s' % page for page in range(1,1380)]
  
  def parse(self, response):
    for title in response.css('#bond-searchresults-container .table tr'):
      tds = title.css('td')
      try:
        if len(tds) > 2:
          href = tds[0].css('a::attr(href)').extract_first().upper()
          symbol = re.search('-([A-Z0-9]*?)$', href).group(1)
          yield {
            'issuer': tds[0].css('a::text').extract_first().strip(),
            'symbol': symbol,
            'currency': tds[1].xpath('text()').extract_first().strip(),
            'coupon': tds[2].xpath('text()').extract_first().strip(),
            'yield': tds[3].xpath('text()').extract_first().strip(),
            'rating': tds[4].xpath('text()').extract_first().strip(),
            'maturity_date': tds[5].xpath('text()').extract_first().strip(),
            'bid': tds[6].xpath('text()').extract_first().strip(),
            'ask': tds[7].xpath('text()').extract_first().strip(),
          }
      except AttributeError:
        continue

