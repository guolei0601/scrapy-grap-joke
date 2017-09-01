# -*- coding:utf-8 -*-
import scrapy
import re
from joke.items import *;
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class StorySpider(scrapy.Spider):
    name = "joke"
    allowed_domains = ["jokeji.cn"]
    start_urls = [
        #'http://www.jokeji.cn/jokehtml/xxh/20091023112047.htm',
       # 'http://www.jokeji.cn/list29_96.htm'
        "http://www.jokeji.cn/Keyword.htm",
        #'http://www.jokeji.cn/list13_1.htm'
       # "http://www.jokeji.cn/list1_1.htm",
        #"http://www.dmoztools.net/Computers/Programming/Languages/Python/Resources/"
    ]

    # rules = (
    #     Rule(LinkExtractor(allow='/list'),callback='parse',follow=False),
    #     #Rule(LinkExtractor(allow='_list'),callback='parse_item')
    # )
    #
    # def parse(self,response):
    #     last_url = response.xpath('//div[@class="next_page"]/a/@href').extract()[-1]
    #     res = last_url.split('_')
    #     #print res
    #     type_list = res[0]
    #     num_list = res[1]
    #     #print num_list
    #     total  = int(num_list.split('.')[0])
    #     #print total
    #     for i in range(1,total + 1):
    #         print type_list + '_' + str(i) + '.htm'
    #     #last_url = response.urljoin(last_url)
    #     #print last_url
    #抓取具体分类链接
    def parse(self, response):

        for sel in response.xpath('//td[@width="119"]'):
            item = {}
            title = sel.xpath('a/text()').extract()[0]
            link  = sel.xpath('./a/@href').extract()[0]
            item['title'] = title
            item['link'] =  link
            url = response.urljoin(link)
            item['url'] =  url
            #print url
            #yield item
            yield scrapy.Request(url,self.parse_list_url)
        #return response.url
    #抓取每个分类的所有分页链接
    def parse_list_url (self,response):
        last_url = response.xpath('//div[@class="next_page"]/a/@href').extract()[-1]
        res = last_url.split('_')
        # print res
        type_list = res[0]
        num_list = res[1]
        # print num_list
        total = int(num_list.split('.')[0])
        # print total
        for i in range(1, total + 1):

            item = {}
            url = type_list + '_' + str(i) + '.htm'
            url = response.urljoin(url)
            yield scrapy.Request(url,self.parse_detail)
    #抓取每个分页中的所有链接
    def parse_detail(self,response):
        for sel in response.xpath('//div[@class="list_title"]/ul/li'):
            item = {}
            link = sel.xpath('./b/a/@href').extract()[0]
            print link
            url =  response.urljoin(link)
            item['url'] = url
            yield scrapy.Request(url,self.parse_content)
    #抓取每个详细链接的内容
    def parse_content(self,response):
        item ={}
        url =  response.url
        item['url'] = url
        item['origin'] = 'jokeji'
        url_list = url.split('/')
        #item['type'] = url_list[-2];
        item['ctime'] = url_list[-1].split('.')[0]
        #接下来获取type和title
        title = response.xpath('//div[@class="left_up"]/h1/text()').extract()[1];
        type  = response.xpath('//div[@class="left_up"]/h1/a[2]/text()').extract()[0];
        res =  response.xpath('//span[@id="text110"]').extract()[0]
        item['type'] =  type
        item['title'] = title[4:]
        #print res
        dr = re.compile(r'</?\w+[^>]*>')
        #去掉换行
        #br = re.compile()
        dd = dr.sub('', res)
        item['content'] =  dd
        yield item



