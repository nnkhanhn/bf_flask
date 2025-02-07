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

	def get_channel(self):
		source_cart_type = self._state['src']['cart_type']
		target_cart_type = self._state['target']['cart_type']
		special_type = source_cart_type == target_cart_type
		cart_version = self._state['target']['config']['version']
		cart_name = getattr(self.get_router(), 'get_cart')(target_cart_type, cart_version, special_type)
		self.target_cart = get_model(cart_name)
		if not self.target_cart:
			return None
		getattr(self.target_cart, 'set_type')('target')
		getattr(self.target_cart, 'set_migration_id')(self._migration_id)
		getattr(self.target_cart, 'set_state')(self._state)
		getattr(self.target_cart, 'set_db')(getattr(self.router, 'get_db')())
		getattr(self.target_cart, 'set_is_test')(self.test)
		if self._state['config'].get('datasync_migration_id'):
			self.target_cart.set_datasync_migration_id(self._state['config'].get('datasync_migration_id'))
		if self._state['config'].get('parent_migration_id'):
			self.target_cart.set_parent_migration_id(self._state['config'].get('parent_migration_id'))
		return self.target_cart
	
	def get_file(self):

		# cart_custom_name = getattr(basecart, 'get_target_custom_cart')(self._migration_id)
		# target_cart = get_model(cart_custom_name)
		if self.target_cart:
			return self.target_cart
		source_cart_type = self._state['src']['cart_type']
		target_cart_type = self._state['target']['cart_type']
		special_type = source_cart_type == target_cart_type
		cart_version = self._state['target']['config']['version']
		cart_name = getattr(self.get_router(), 'get_cart')(target_cart_type, cart_version, special_type)
		self.target_cart = get_model(cart_name)
		if not self.target_cart:
			return None
		getattr(self.target_cart, 'set_type')('target')
		getattr(self.target_cart, 'set_migration_id')(self._migration_id)
		getattr(self.target_cart, 'set_state')(self._state)
		getattr(self.target_cart, 'set_db')(getattr(self.router, 'get_db')())
		getattr(self.target_cart, 'set_is_test')(self.test)
		if self._state['config'].get('datasync_migration_id'):
			self.target_cart.set_datasync_migration_id(self._state['config'].get('datasync_migration_id'))
		if self._state['config'].get('parent_migration_id'):
			self.target_cart.set_parent_migration_id(self._state['config'].get('parent_migration_id'))
		return self.target_cart

	def delete_notice(self):
		# router = get_model('migration')
		delete = getattr(self.get_router(), 'delete_migration_notice')(self._migration_id)
		if delete:
			self._notice = None
		return delete

	def update_notice(self, _migration_id, notice = None, pid = None, mode = None, status = None, finish = False):
		# router = get_model('migration')
		return getattr(self.get_router(), 'update_notice')(_migration_id, notice, pid , mode, status, finish)


