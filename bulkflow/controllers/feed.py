import copy
import os
import time

from bulkflow.models.base.controller import Controller
from bulkflow.libs.errors import Errors
from prodict import Prodict
from bulkflow.libs.response import Response
from bulkflow.libs.utils import to_int, get_model, to_str, get_server_id, FLAG_KILL_ALL, FLAG_STOP, log, to_len
from bulkflow.models.constructs.state import State
from bulkflow.models.setup import Setup
from bulkflow.models.feed import Feed
from bulkflow.models.setup import Setup


class ControllerFeed(Controller):

	def create_feed(self, request_data):
		feed_model = Feed()
		channel_type = request_data.get('channel_type')
		user_id = request_data.get('user_id')
		file_type = request_data.get('file_type')
		feed_id = feed_model.get_feed_max_id()
		feed_model.set_feed_id(feed_id)
		self.setup_before_create(feed_id)
		pass

	def setup_before_create(self, feed_id):
		setup = Setup()
		setup.setup_db_for_feed(feed_id)
		pass

	def init_channel(self):
		pass