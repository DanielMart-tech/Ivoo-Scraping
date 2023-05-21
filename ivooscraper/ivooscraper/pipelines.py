# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class NamePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("name"):
            name = adapter["name"][0].strip()
            adapter["name"] = name
            return item


class PricePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("price"):
            floatPrice = adapter["price"][0].replace(",", ".")
            adapter["price"] = float(floatPrice)
            return item


class URLPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["url"]:
            url = adapter["url"][0]
            adapter["url"] = url
            return item


class SavingToPostgresPipeline(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = psycopg2.connect(
            host="localhost", database="ivoo_scraping", user="postgres", password="1234"
        )

        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_in_db(item)
        return item

    def store_in_db(self, item):
        self.cur.execute(
            """insert into computers values (%s,%s,%s)""",
            (item["name"], item["price"], item["url"]),
        )
        self.conn.commit()
