import configparser

from bulkflow.models.base.base import ConstructBase
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
    
    def run(self):
        config_file = get_root_path() + '/bulkflow/etc/config.ini'
        if os.path.isfile(config_file):
            config_local = None
        else:
            host = input('Enter local database host: \n')
            username = input('Enter local database username: \n')
            password = input('Enter local database password: \n')
            name = input('Enter local database name: \n')
            prefix = input('Enter local database prefix: \n')
            config_local = dict()
            config_local['db_host'] = host
            config_local['db_username'] = username
            config_local['db_password'] = password
            config_local['db_name'] = name
            config_local['db_prefix'] = prefix
        db = self.get_db(config_local)
        con = db.get_connect()
        if not con:
            print("Database local setup fail")
            print("----------------------------------")
            return False
        for table in self.tables:
            query = self.dict_to_create_table_sql(table)
            if query['result'] != 'success':
                return False
            res = self.query_raw(query['query'])
            if res['result'] != 'success':
                return False
        self.delete_obj('directory_country_region')
        file_state = get_pub_path() + '/uploads/directory_country_region.sql'
        import_cmd = ' -u ' + db.get_db_username() + ' -p' + db.get_db_password() + ' ' + db.get_db_name() + ' < ' + file_state
        subprocess.call(['mysql', import_cmd], shell=False)
        with open(file_state, 'r') as f:
            command = ['mysql', '-u%s' % db.get_db_username(), '-p%s' % db.get_db_password(), db.get_db_name()]
            proc = subprocess.Popen(command, stdin=f, stdout=subprocess.PIPE)
            stdout, stderr = proc.communicate()
        print("Database local setup successfully")
        print("----------------------------------")
        if os.path.isfile(config_file):
            config_center = None
        else:
            
            host = input('Enter center database host: \n')
            username = input('Enter center database username: \n')
            password = input('Enter center database password: \n')
            name = input('Enter center database name: \n')
            prefix = input('Enter center database prefix: \n')
            config_center = dict()
            config_center['db_host'] = host
            config_center['db_username'] = username
            config_center['db_password'] = password
            config_center['db_name'] = name
            config_center['db_prefix'] = prefix
        db = self.get_db(False, config_center)
        con = db.get_connect()
        if not con:
            print("Can't connect to center database")
            print("----------------------------------")
            return False
        print("Connected Database center!")
        print("----------------------------------")
        if os.path.isfile(config_file):
            config = configparser.ConfigParser()
            config.read(config_file)
            try:
                port = config['server']['port']
                port_upload = config['server']['port_upload']
            except Exception:
                port = input('Enter port socket: \n')
                port_upload = input('Enter port upload file: \n')
            if not config.has_section('server'):
                config.add_section('server')
                config['server']['port'] = port
                config['server']['port_upload'] = port_upload
                with open(config_file, 'w') as configfile:  # save
                    config.write(configfile)
        
        if not os.path.isfile(config_file):
            port = input('Enter port socket: \n')
            port_upload = input('Enter port upload file: \n')
            config = configparser.ConfigParser()
            config.add_section('server')
            config['server']['port'] = port
            config['server']['port_upload'] = port_upload
            config.add_section(Mysql.TYPE_LOCAL)
            for key, value in config_local.items():
                config[Mysql.TYPE_LOCAL][key] = value
            config.add_section(Mysql.TYPE_CENTER)
            for key, value in config_center.items():
                config[Mysql.TYPE_CENTER][key] = value
            config_file = get_root_path() + '/bulkflow/etc/config.ini'
            with open(config_file, 'w') as configfile:  # save
                config.write(configfile)
        return True
