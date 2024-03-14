import json
from datetime import datetime
from scrapy.http import Response, Request
from twisted.python.failure import Failure
from scrapy.core.downloader.handlers.http11 import TunnelError

from rmq.utils import Task, get_import_full_name, TaskStatusCodes
from rmq.pipelines import ItemProducerPipeline
from rmq.spiders import TaskToSingleResultSpider
from rmq.utils.decorators import rmq_errback, rmq_callback
from rmq.extensions import RPCTaskConsumer

from items import CompanyItem
from middlewares.retry_request_middleware import RetryRequestMiddleware



class CompanySpider(TaskToSingleResultSpider):
    name = "company"

    custom_settings = {"ITEM_PIPELINES": {get_import_full_name(ItemProducerPipeline): 310,},
                    #    "DOWNLOADER_MIDDLEWARES": {get_import_full_name(RetryRequestMiddleware): 543,}
                       }
    
    def __init__(self, *args, **kwargs):
        super(CompanySpider, self).__init__(*args, **kwargs)
        self.task_consumer = RPCTaskConsumer(self)
        self.task_consumer.completion_strategy = RPCTaskConsumer.CompletionStrategies.REQUESTS_BASED
        self.task_queue_name = f"task"
        self.result_queue_name = f"result"

    def next_request(self, delivery_tag, message):
        url = json.loads(message)['url']
        return Request(url, callback=self.parse, meta={'delivery_tag': delivery_tag, 'reply_to': 'replies_queue'}, errback=self.handle_error)

    @rmq_callback
    def parse(self, response: Response):
        item = CompanyItem()

        
        self.logger.warning(self.processing_tasks.current_processing_count())
        
        item['url'] = response.url
        item['business_id'] = item['url'].split('/')[-1]
        item['name'] = response.xpath('//span[@class="bds-h2 font-normal text-black"]/text()').get()
        item['category'] = response.xpath('//div[contains(@class, "text-size-4 text-gray-70")]/text()').get()
        item['website'] = response.xpath('//a[contains(@class, "dtm-url")]/@href').get()
        
        item['phone'] = response.xpath('//a[contains(@class, "dtm-phone")]/text()').get()
        item['phone'] = int(''.join(filter(str.isdigit, item['phone']))) if item['phone'] else None

        address_partiotions = response.xpath('//div[contains(@class, "dtm-address")]/div/address/p/text()').getall()
        if address_partiotions:
            item['city'], _, item['state'], _, item['postal_code'] = address_partiotions[-5:]
            item['address'] = f'{item['city']}, {item['state']} {item['postal_code']}'

            if len(address_partiotions) > 5:
                item['street'] = ' '.join(address_partiotions[:-5]) if ' '.join(address_partiotions[:-5]) != ' ' else None
                item['address'] = f"{item['street']} {item['address']}"  

        if '.org/us/' in item['url']:
            item['country'] = 'USA'
        elif '.org/ca/' in item['url']:
            item['country'] = 'Canada'
        else:
            self.logger.error(f"Can't parse country {item['url']}")

        item['years_old'] = response.xpath('//p[@class="bds-body"]/strong[text()="Years in Business:"]/following-sibling::text()[1]').get()
        item['years_old'] = int(item['years_old'].strip()) if item['years_old'] else None

        item['reviews_quantity'] = response.xpath('//p[contains(., "Average of")]/text()').re_first(r'\d+') 
        item['reviews_quantity'] = int(item['reviews_quantity']) if item['reviews_quantity'] else None
        item['user_score'] = response.xpath('//div[contains(@class, "dtm-stars")]/following-sibling::span[1]/text()').get() 
        item['user_score'] = item['user_score'].split('/')[0] if item['user_score'] else None
        item['accredited_score'] = ''.join(response.xpath("//span[contains(@class, 'dtm-rating')]//span/text()").getall()).replace('BBB rating', '')

        yield Request(url=f'{item['url']}/details', callback=self.parse_detail, meta={'item': item})

    @rmq_callback
    def parse_detail(self, response: Response):
        foundation_date = response.xpath('//dt[text()="Business Started:"]/following-sibling::dd[1]/text()').get()
        item = response.meta['item']
        item['image_url'] = response.xpath('//div[@class="repel css-7ta29z eynu2dr1"]//img/@src').get()
        if item['image_url'] == 'https://m.bbb.org/terminuscontent/dist/img/non-ab-icon__300w.png?tx=w_120':
            item['image_url'] = None

        
        item['foundation_date'] = foundation_date.strip() if foundation_date else None
        accredited_date = response.xpath("//div/p/strong[text()='Accredited Since:']/following-sibling::text()[1]").get()
        item['accredited_date'] = accredited_date.strip() if accredited_date else None


        item['fax'] = response.xpath('//li[contains(., "Primary Fax")]/span/text()').get()
        
        raw_hours = response.xpath('//div[@class="stack"]//*[self::dt or self::dd]/text()').getall()
        work_hours = {}
        work_hours.update({raw_hours[i]: raw_hours[i + 2] for i in range(0, len(raw_hours), 3)})
        item['work_hours'] = json.dumps(work_hours)

        media_path = response.xpath('//ul[@class="css-zyn7di e62xhj40"]/li/a[@class="with-icon"]') 
        media_dict = {link.xpath('text()').get().strip().lower(): link.xpath('@href').get() for link in media_path}

        for social_network in ['instagram', 'facebook', 'twitter']:
            item[social_network] = media_dict.get(social_network, None)

        management = response.xpath('//dt[text()="Business Management"]/following-sibling::dd/ul/li/span/text()').getall()
        item['management'] = json.dumps({mng.split(',')[0]: mng.split(',')[1].strip() if len(mng.split(',')) >= 2 else None for mng in management})

        contact = response.xpath('//dt[text()="Contact Information"]/following-sibling::dd/ul/li/span/text()').getall()
        item['contact'] = json.dumps({cnt.split(',')[0]: cnt.split(',')[1].strip() if len(cnt.split(',')) >= 2 else None for cnt in contact})

        for date_str in ['accredited_date', 'foundation_date']:
            date_item = item.get(date_str)
            if date_item:
                try:
                    item[date_str] = datetime.strptime(date_item, '%d/%m/%Y').isoformat()
                except:
                    item[date_str] = datetime.strptime(date_item, '%m/%d/%Y').isoformat()

        yield item
        self.logger.warning(item)

    @rmq_errback
    def handle_error(self, failure: Failure):
        self.logger.warning(f'{failure.value.response.status}')
        if failure.check(TunnelError):
            self.logger.info("TunnelError. Copy request")
            yield failure.request.copy()
        delivery_tag = failure.request.meta['delivery_tag']
        self.processing_tasks.set_status(delivery_tag=delivery_tag, status=TaskStatusCodes.ERROR.value)
        
        task: Task = self.processing_tasks.get_task(delivery_tag=delivery_tag)

        if failure.value.response.status in (404, ):
            self.logger.warning(f'{task.payload}')
            task.ack()
        # elif failure.value.response.status in (403, 429):
        #     self.logger.warning('403 or 429, retry')
        #     yield failure.request.copy()
        # else:
        #     task.ack()
        #     self.processing_tasks.remove_task(delivery_tag=delivery_tag)
        #     self.logger.warning(f"IN ERRBACK: {repr(failure)}")
