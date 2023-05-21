from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class IvooProductLoader(ItemLoader):
    default_input_processor = TakeFirst()
    price_in = MapCompose(lambda x: x.split("$")[-1])