import scrapy
import re

class LookupSpider(scrapy.Spider):
  name = 'lookup'
  # Those URLs return 301 redirect. Scrapy can process it, but we need 2 calls for each page.
  #TODO(lenny): Fix the URLs.
  start_urls = [
    'https://markets.businessinsider.com/bonds/6_250-Oesterreich-Republik-Bond-2027-AT0000383864',
    'https://markets.businessinsider.com/bonds/3_900-Oesterreich-Republik-Bond-2020-AT0000386115',
    'https://markets.businessinsider.com/bonds/3_500-Oesterreich-Republik-Bond-2021-AT0000A001X2'
  ]
  
  def parse(self, response):
    instrument = get_text(response.css('.snapshot-headline-instrumentname .aktien-time'))
    coupon = get_property_from_2td_table(response, 'Coupon')
    maturity_date = get_property_from_2td_table(response, 'Maturity Date')
    issuer = get_issuer(response)
    country = get_property_from_2td_table(response, 'Country')
    n_payments = get_property_from_2td_table(response, 'No. of Payments per Year')
    yield_p = get_yield(response)
    yield {
      'symbol': instrument,
      'coupon': coupon,
      'maturity_date': maturity_date,
      'issuer': issuer,
      'country': country,
      'n_payments': n_payments,
      'yield': yield_p
    }

def get_property_from_2td_table(data, key):
  for tr in data.css('table.table.table-small.no-margin-bottom tr'):
    tds = tr.css('td')
    if len(tds) != 2:
      continue
    if get_text(tds[0]) == key:
      return get_text(tds[1])

def get_issuer(data):
  for tr in data.css('table.table.table-small.no-margin-bottom tr'):
    tds = tr.css('td')
    if len(tds) != 2:
      continue
    if get_text(tds[0]) == 'Issuer':
      return get_text(tds[1].css('a'))

def get_yield(data):
  for tr in data.css('table.table.table-small.no-margin-bottom tr'):
    tds = tr.css('td')
    if len(tds) != 4:
      continue
    if get_text(tds[2]) == 'Yield in %':
      return get_text(tds[3])
  

def get_text(el):
  return el.xpath('text()').extract_first().strip()

