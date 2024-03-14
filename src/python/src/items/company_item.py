from scrapy import Field
from rmq.items import RMQItem


class CompanyItem(RMQItem):
    business_id = Field()
    url = Field()
    name = Field()
    category = Field()
    address = Field()
    country = Field()
    state = Field()
    city = Field()
    street = Field()
    postal_code = Field()
    website = Field()
    image_url = Field()
    phone = Field()
    phone_clean = Field()
    fax = Field()
    work_hours = Field()
    user_score = Field()
    reviews_quantity = Field()
    accredited_score = Field()
    accredited_date = Field()
    foundation_date = Field()
    years_old = Field()
    social_networks = Field()
    instagram = Field()
    facebook = Field()
    twitter = Field()
    management = Field()
    contact = Field()
    