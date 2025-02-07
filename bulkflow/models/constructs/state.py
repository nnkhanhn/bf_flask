from typing import List

from bulkflow.models.base.construct import ConstructBase

class State(ConstructBase):
    def __init__(self, **kwargs):
        self.channel_config = ChannelConfig()
        self.file_config = ChannelConfig()
        self.total = 0
        self.feed_id = 0
        self.imported = 0
        self.imported_previous = 0
        self.last_product_id = 0
        self.last_page = 0
        self.number_break = 0
        self.status = ''
        self.feed_type = ''
        self.feed_format = ''
        super().__init__(**kwargs)

class ChannelConfig(ConstructBase):
    def __init__(self, **kwargs):
        self.type = ''
        self.url = ''
        self.api = ''
        self.token = ''
        super().__init__(**kwargs)

class FileConfig(ConstructBase):
    def __init__(self, **kwargs):
        self.type = ''
        self.link = ''
        self.ssh = ''
        self.config = ''
        super().__init__(**kwargs)