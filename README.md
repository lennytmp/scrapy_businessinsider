# Scrapers to get bonds information
 
The data is parsed from markets.businessinsider.com/bonds/. To execute [Scrapy
framework](https://scrapy.org/) should be installed.

Short summary of spiders:

1. `scrapy_spider.py` was used to extract data from bonds search dialog, but for
unknown reason it scraped limited data, presumably after a certain page, the
data returned by businessinsider was always the same.
1. `suggestion_spider.py` was used to get the exact URLs for the bonds using
search suggestion system.
1. `lookup_spider.py` was used to get the information for each bond from the
corresponding page.

Initial list of bonds was acquired from degiro.ie with a hacky snippet in
JavaScript.

