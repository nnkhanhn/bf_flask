import copy
import os
import time

from bulkflow.models.controllers.controller import Controller
from bulkflow.libs.errors import Errors
from prodict import Prodict
from bulkflow.libs.response import Response
from bulkflow.libs.utils import to_int, get_model, to_str, get_server_id, FLAG_KILL_ALL, FLAG_STOP, log, to_len
from bulkflow.models.constructs.feed_state import FeedState

class ControllerFeed(Controller):
	PULL_START_ACTION = 'display_pull'
	_channel: ModelChannel or None