from typing import List

from bulkflow.models.base.base import ConstructBase

class ConstructProduct(ConstructBase):
    def __init__(self, **kwargs):
        self.id = 0
        self.name = ''
        self.sku = ''
        self.parent_sku = ''
        self.description = ''
        self.brand = ''
        self.tags = ''
        self.condition = ''
        self.condition_note = ''
        self.msrp = ''
        self.seo_url = ''
        self.manufacturer = ''
        self.mpn = ''
        self.upc = ''
        self.ean = ''
        self.isbn = ''
        self.price = 0
        self.qty = 0
        self.gtin = ''
        self.gcid = ''
        self.asin = ''
        self.epid = ''
        self.lenght = ''
        self.width = ''
        self.height = ''
        self.dimension_units = ''
        self.weight = ''
        self.weight_units = ''
        self.variant_1 = ''
        self.variant_2 = ''
        self.variant_3 = ''
        self.variant_4 = ''
        self.variant_5 = ''
        self.product_image_1 = ''
        self.product_image_2 = ''
        self.product_image_3 = ''
        self.product_image_4 = ''
        self.product_image_5 = ''
        self.attributes = ''
        self.categories = ''
        super().__init__(**kwargs)