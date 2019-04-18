from scrapy import Spider
import scrapy
from cronjob.items import CronjobItem
from scrapy.selector import Selector

class CronjobSpider(Spider):
    # //*[@id="question-summary-55413756"]/div[2]

    name = "cronjob"
    # allowed_domains = ["http://4510m.in/"]
    start_urls = [
        "https://4510m.in/",
    ]


    def parse(self, response):
        posts = response.xpath('//*[contains(@class, "post small-12")]/h4[@class="title"]/a/@href').extract_first()
        for post in posts:
            post = response.urljoin(post)
            yield scrapy.Request(url = post, callback = self.parse_details)

        for href in response.xpath('//div[@class="navigation"]/span[@class="pagenavi-box-a"]/a/@href'):
            next_page = href.extract()
            yield scrapy.Request(url = next_page, callback = self.parse)
    
    
    def parse_details(self, response):
        post = CronjobItem()
        temp_job_id = response.xpath('//*[contains(@class, "post small-12")]/h4[@class="title"]/span[1]/text()').extract_first()
        temp_job_id_slipt = temp_job_id.split('.')
        post['job_id'] = temp_job_id_slipt[1]
        post['job_title'] = response.xpath('//*[contains(@class, "post small-12")]/h4[@class="title"]/a/span[last()]/text()').extract_first()
        temp_basic_info = response.xpath('//*[contains(@class, "post small-12")]/p[@class="basic_info"]/span[@class="post_category"]/*/text()').extract()
        
        if len(temp_basic_info) > 0:
            post['area1'] = temp_basic_info[0]
            post['employment_type'] = temp_basic_info[1]
            post['job_category'] = temp_basic_info[2]
            post['salary_range'] = temp_basic_info[3]
        else:
            post['area1'] = None
            post['employment_type'] = None
            post['job_category'] = None
            post['salary_range'] = None

        # temp_post_date = response.xpath('//*[contains(@class, "post small-12")]/p[@class="basic_info"]/span[@class="date_from"][1]/text()').extract_first()
        temp_posted_date = response.xpath('//*[contains(@class, "post small-12")]/p[@class="basic_info"]/span[@class="date_from"]/text()').re(r'\d+/\d+/\d+\s+\d+:\d+')
        if len(temp_posted_date) > 0:
            post['posted_date']  = temp_posted_date[0]
        else:
            post['posted_date']  = None

        post['age'] = response.xpath('//table//tr[1]/td/text()').extract_first()
        post['requirements'] = response.xpath('//table//tr[2]/td/text()').extract_first()
        post['salary']  = response.xpath('//table//tr[3]/td/text()').extract_first()
        post['period']  = response.xpath('//table//tr[4]/td/text()').extract_first()
        post['working_hour']  = response.xpath('//table//tr[5]/td/text()').extract_first()
        post['location']  = response.xpath('//table//tr[6]/td/text()').extract_first()
        tem_decs = response.xpath('//div[@class="more"]/p/text()').extract()
        post['desc'] = ', '.join(tem_decs) if tem_decs is not None else None
        post['company_name'] = response.xpath('//*[contains(@class, "com_info small-12 medium-3 right")]/*[li]/a/text()').extract_first()
        post['company_website'] = response.xpath('//*[contains(@class, "com_info small-12 medium-3 right")]/*[1]/a/@href').extract_first()
        post['representative'] = response.xpath('//*[contains(@class, "com_info small-12 medium-3 right")]/*[2]/a/text()').extract_first()
        post['email'] = response.xpath('//*[contains(@class, "com_info small-12 medium-3 right")]/*[2]/a/@href').extract_first()

        tel_temp = response.xpath('//*[contains(@class, "com_info small-12 medium-3 right")]/*[3]/text()').extract_first()
        post['tel'] = tel_temp if tel_temp is not None else None

        if tel_temp is not None:
            if 'Tel' not in tel_temp:
                post['tel'] = None
            else:
                tel_temp_split = tel_temp.split('Tel：')
                post['tel'] = tel_temp_split[1]

        fax_temp = response.xpath('//*[contains(@class, "com_info small-12 medium-3 right")]/*[4]/text()').extract_first()
        post['fax'] = fax_temp if fax_temp is not None else None

        if fax_temp is not None:
            if 'Fax' not in fax_temp:
                post['fax'] = None
            else:
                fax_temp_split = fax_temp.split('Fax：')
                post['fax'] = fax_temp_split[1]

        pr_temp = response.xpath('//*[contains(@class, "com_info small-12 medium-3 right")]/*[last()]/text()').extract_first()
        post['pr'] = pr_temp if pr_temp is not None else None
        if pr_temp is not None:
            if 'PR' not in fax_temp:
                post['pr'] = None
            else:
                pr_temp_split = pr_temp.split('PR：')
                post['pr'] = pr_temp_split[1]

        yield post