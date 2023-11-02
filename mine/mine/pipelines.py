# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MinePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # template usage
        # keys = ["data_key_01", "data_key_02", "data_key_03"]
        # for key in keys:
        #     value = adapter.get(key)
        #     adapter[key] = value

        return item
