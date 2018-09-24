import scrapy
import re

class SuggestionSpider(scrapy.Spider):
  name = 'suggestion'
  symbols = ['AT0000383864', 'AT0000386115', 'AT0000A001X2']
  start_urls = ['https://markets.businessinsider.com/ajax/SearchController_Suggest?max_results=25&Keywords_mode=APPROX&Keywords=%s&bias=100&target_id=0&query=%s' % (s, s) for s in symbols]
  
  def parse(self, response):
    resp = response.body.decode("utf-8")
    url_part = re.search('.*"", "([^|]*)|.*"', resp).group(1)
    if url_part != None:
      yield {
        'symbol': re.search('.*=(.*)$', response.request.url).group(1),
        'url': 'https://markets.businessinsider.com/bonds/' + url_part
      }

