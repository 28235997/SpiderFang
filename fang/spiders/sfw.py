# -*- coding: utf-8 -*-
import re

import scrapy
from fang.items import NewHouse
from fang.items import EsfHouse

class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")
        province = None
        for tr in trs:
            #省份的下一行是空，但他还是上一个省份的城市
            tds = tr.xpath(".//td[not(@class)]")
            province_td = tds[0]
            province_text = province_td.xpath(".//text()").get()
            province_text = re.sub(r"\s", "", province_text) #将省份中空格替换成空白字符
            #如果省份为空，则还使用的是上一个省份
            if province_text:
                province = province_text
            if province == "其他":
                continue
            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                url_module = city_url.split(".")
                # if "bj." in url_module[0]:  #字符串包含
                #     newhouse_url = 'http://bj.newhouse.fang.com'
                #     esf_url = 'http://bj.esf.fang.com'
                # else:
                    #构建新房的url链接
                newhouse_url = url_module[0] + ".newhouse." + url_module[1] + "." + url_module[2]

                #构建二手房的url连接
                esf_url = url_module[0] + ".esf." + url_module[1] + "." + url_module[2]

                #yield scrapy.Request(url=newhouse_url, callback=self.parse_newhouse,
                #                    meta={'info': (province, city, newhouse_url)})
                yield scrapy.Request(url=esf_url, callback=self.parse_esf,
                                     meta={'info': (province, city, esf_url)})
                break
            break


    def parse_newhouse(self, response):
        province, city, newhouse_url = response.meta.get('info')

        lis = response.xpath("//div[contains(@class,'nl_con')]/ul/li")
        for li in lis:
            try:

                name = li.xpath(".//div[@class='nlcd_name']/a/text()").get().strip()
                house_type = li.xpath(".//div[contains(@class,'house_type')]/a/text()").getall()
                house_type = list(map(lambda x: re.sub(r"\s", "", x), house_type)) #去掉空白字符
                address = li.xpath(".//div[@class='address']/a/@title").get()
                district_text = "".join(li.xpath(".//div[@class='address']/a//text()").getall())
                district = re.search(r"\[(.+)\].*", district_text).group(1)  #拿到中括号中的内容
                area = "".join(li.xpath(".//div[contains(@class,'house_type')]/text()").getall())
                area = re.sub(r"\s|/", "", area)
                price = "".join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
                price = re.sub(r"\s|广告", "", price)
                origin_url = li.xpath(".//div[@class='nlcd_name']/a/@href").get()
                item = NewHouse(name=name, province=province, city=city, rooms=house_type, address=address,
                                district=district, area=area, origin_url=origin_url, price=price)
                yield item


            except:
                continue
        next_url = response.xpath("//div[@class='page']//a[@class='next']/@href").get()
        next1 = next_url.strip()[1:]
        all_url = newhouse_url + next1
        print(all_url)
        yield scrapy.Request(url=all_url, callback=self.parse_newhouse,
                             meta={'info': (province, city, newhouse_url)})
        pass

    def parse_esf(self, response):
        province, city, esf_url = response.meta.get('info')
        item = EsfHouse(province=province, city=city)
        lis = response.xpath("//div[contains(@class,'shop_list')]/dl")
        for li in lis:
            try:
                #info = "".join(li.xpath(".//h4[@class='clearfix']//text()").getall())
                #info = re.sub(r"\s", "", info)
                detail_info = "".join(li.xpath(".//p[@class='tel_shop']//text()").getall())
                detail_info = re.sub(r"\s", "", detail_info).split("|")
                infos = detail_info[:-1]

                for info in infos:
                    if '厅' in info:
                        item['rooms'] = info
                    elif '层' in info:
                        item['floor'] = info
                    elif '向' in info:
                        item['toward'] = info
                    elif 'm' in info:
                        item['area'] = info
                    else:
                        item['year'] = info
                item['price'] = "".join(li.xpath(".//dd[@class='price_right']/span[@class='red']//text()").getall())
                item['oneprice'] = li.xpath(".//dd[@class='price_right']/span[not(@class)]/text()").get()
                item['name'] = li.xpath(".//p[@class='add_shop']/a/@title").get()
                item['address'] = li.xpath(".//p[@class='add_shop']//span/text()").get()
                advantage_text = "".join(li.xpath(".//p[@class='clearfix label']//text()").getall())
                item['advantage'] = re.sub(r"\s", "", advantage_text)
                url_info = li.xpath(".//h4[@class='clearfix']/a/@href").get()
                item['origin_url'] = response.urljoin(url_info)
                yield item
            except:
                continue
        next_url = response.xpath("//div[contains(@class,main945)]/div[@class='page_al']/p/a/@href").get()
        print(next_url)
        next1 = next_url.strip()[1:]
        all_url = esf_url + next1
        print(all_url)
        yield scrapy.Request(url=all_url, callback=self.parse_esf,
                             meta={'info': (province, city, esf_url)})