import copy
import os
import time

from bulkflow.models.base.controller import Controller
from bulkflow.libs.errors import Errors
from prodict import Prodict
from bulkflow.libs.response import Response
from bulkflow.libs.utils import to_int, get_model, to_str, get_server_id, FLAG_KILL_ALL, FLAG_STOP, log, to_len
from bulkflow.models.constructs.feed_state import FeedState

class FeedController(Controller):
	def create_feed(self):
		pass

	def setup_before_create(self):
		pass