import os
import sys
import traceback

from bulkflow.libs.errors import Errors
from bulkflow.libs.response import Response
from bulkflow.libs.utils import log, to_str, json_encode, get_current_time, to_int, get_model

class Controller:
	def __init__(self, data = None):
		self._response = Response()
		self._user_id = data.get('user_id') if data else None
		self._date_requested = get_current_time()
		self._order_channels = dict()
		self._product_channels = dict()
		self._data = data

	def response(self, res):
		if hasattr(res, 'to_json'):
			res = getattr(res, 'to_json')()
		if isinstance(res, (list, dict)):
			res = json_encode(res)
		print(res, end = '')
		sys.exit(1)


	def execute(self, action, data = None):
		try:
			if hasattr(self, action):
				res = getattr(self, action)(data)
			else:
				res = Response().error(Errors.ACTION_INVALID)
		except Exception:
			# prefix = ""
			# if data:
			# 	if data.get('user_id'):
			# 		prefix = "user/" + to_str(data['user_id'])
			# 	if data.get("sync_id"):
			# 		prefix = os.path.join('processes', to_str(data['sync_id']))
			error = traceback.format_exc()
			# log(error, prefix_path = prefix)
			self.log(error)
			res = Response().error(Errors.EXCEPTION)
		if hasattr(res, 'code') and res.code and not res.msg:
			res.msg = Errors().get_msg_error(res.code)
		self.response(res)


	def log(self, msg, type_log = 'exceptions'):
		prefix = os.path.join("user", to_str(self._user_id))
		log(msg, prefix, type_log)


	def log_traceback(self, type_error = 'exceptions', entity_id = None):
		error = traceback.format_exc()
		if entity_id:
			error = type_error + ' ' + to_str(entity_id) + ': ' + error
		self.log(error, type_error)



