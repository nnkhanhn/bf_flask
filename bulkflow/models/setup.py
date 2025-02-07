import configparser

from bulkflow.models.base.construct import ConstructBase
from bulkflow.libs.mysql import Mysql
from bulkflow.libs.utils import *


class Setup():
    
    _table_map = {
        'table': TABLE_MAP,
        'rows': {
            'id': 'BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY',
            'feed_id': "BIGINT NOT NULL",
            'type': "VARCHAR(255)",
            'id_src': "BIGINT",
            'id_desc': "BIGINT",
            'code_src': "VARCHAR(255)",
            'code_desc': "TEXT",
            'value': "LONGTEXT",
            'additional_data': "LONGTEXT",
            'store_id_src': "VARCHAR(255)",
            'store_id_desc': "VARCHAR(255)",
            'created_at': 'VARCHAR(25)',
            'src_entity_status': "TEXT",
            'target_entity_status': "TEXT",
        },
        'index': [
            ['feed_id'],
            ['id_src'],
            ['type'],
            ['code_src'],
        
        ],
    }
    
    _table_feed_history = {
        'table': TABLE_FEED_INF,
        'rows': {
            'id': 'BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY',
            'feed_id': "BIGINT NOT NULL",
            'type': "VARCHAR(255)",
            'created_at': "DATETIME",
            'state': "LONGTEXT"
        },
    }

    
    def __init__(self):
        super().__init__()
        self._db_local = None
        self._db_center = None
        self.tables = [self._table_feed_history,
                       self._table_map]


    def clear_feed(self, feed_id):
        db = Mysql(test = False, feed_id = feed_id)
        db.set_feed_id(feed_id)
        db.drop_database()

    def setup_db_for_feed(self, feed_id, test=False):
        if not feed_id:
            return False
        db = Mysql(test=test, feed_id=feed_id)
        db.set_feed_id(feed_id)
        db.create_database()
        db.set_config(None)
        for table in self.tables:
            query = db.dict_to_create_table_sql(table)
            if query['result'] != 'success':
                return False
            res = db.query_raw(query['query'])
            if res['result'] != 'success':
                return False
        db.close_connect()
        return True
    
