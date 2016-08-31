# coding: utf-8
import scrapy
from urllib.parse import urlparse
from urllib.parse import parse_qs
from scrapy_scimago.items import JournalItem
from pymongo import MongoClient
from xylose.scielodocument import Journal


def journals_issns():
    coll = MongoClient(
        'node1-mongodb.scielo.org', 27000)['articlemeta']['journals']

    issns = []

    for journal in coll.find():
        xjournal = Journal(journal)
        jissns = [xjournal.scielo_issn, xjournal.print_issn, xjournal.electronic_issn]
        issns += [i for i in jissns if i]

    return set(issns)


class ScimagoSpider(scrapy.Spider):

    name = "scimago"
    allowed_domains = ["scimagojr.org"]
    start_urls = ["http://www.scimagojr.com/journalsearch.php?q=%s" % issn for issn in journals_issns()]

    def parse(self, response):
        request_url = urlparse(response.request.url)
        issn = parse_qs(request_url.query).get('q', [])[0]
        data = response.selector.xpath('//div[@class="search_results"]//a/@href')
        if not len(data) == 1:
            return None
        url = data[0].extract()
        purl = urlparse(url)
        scimago_id = parse_qs(purl.query).get('q', [])[0]
        item = JournalItem()
        item['issn'] = issn
        item['scimago_id'] = scimago_id

        return item
