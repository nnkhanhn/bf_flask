import pymongo

from bulkflow.libs.db.mongo import Mongo
from bulkflow.libs.utils import get_config_ini


class FeedMongo(Mongo):
	def __init__client__(self):
		driver = get_config_ini('feed_mongo', 'db_driver')
		password = self.encode_password(get_config_ini('feed_mongo', 'db_password'))
		driver = driver.replace('<password>', password)
		try:
			self._client = pymongo.MongoClient(driver)
		except:
			pass
			c = 3
			d = 4
	def _create_connect(self, user_id):
		database_name = f"{get_config_ini('feed_mongo', 'db_name')}_{user_id}"

		connect = getattr(self._get_client(), database_name)

		return connect