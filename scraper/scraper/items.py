from scrapy.item import Item, Field


class ApartmentItem(Item):
    title = Field()
    image_url = Field()
    