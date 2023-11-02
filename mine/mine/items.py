# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose

from w3lib.html import remove_tags
import html

from mine.utilities import replace_tags_with_space, decode_html_entities


class MineItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
