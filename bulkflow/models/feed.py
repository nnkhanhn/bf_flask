from bulkflow.libs.utils import *
from bulkflow.models.setup import Setup
from bulkflow.models.constructs.feed_state import FeedState


class Feed():

	USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
	_state: FeedState

	def set_feed_id(self, feed_id):
		self._feed_id = feed_id

