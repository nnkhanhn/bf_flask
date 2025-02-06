from bulkflow.libs.messages import Messages
from bulkflow.libs.response import Response


class ModelChannel:
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self._storage_image_service = None
		self._storage_service = None
		self._request_data = dict()
		self._user_id = kwargs.get('user_id')
		self._channel_type = kwargs.get('channel_type')
		self._state = None
		self._server_name = None
		self._model_state = None
		self._model_catalog = None
		self._model_category = None
		self._model_attribute = None
		self._model_template = None
		self._model_activity = None
		self._model_order = None
		self._model_process = None
		self._model_deleted_product = None
		self._sync_id = None
		self._channel_id = None
		self._product_id = None
		self._is_test = False
		self._channel_url = ''
		self._response = Response()
		self._model_sync_mode = None
		self._identifier = ''
		self._name = ''
		self._type = ''
		self._id = ''
		self._last_header = None
		self._last_status = None
		self._db = None
		self._state_id = None
		self._action_stop = False
		self._warehouse_location_default = None
		self._warehouse_location_fba = None
		self._date_requested = None
		self._is_update = False
		self._process_type = ''
		self._user_plan = None
		self._user_info = None
		self._is_inventory_process = False
		self._publish_action = None
		self._src_channel_id = None
		self._channel_action = None
		self._channel_default_id = None
		self._product_available_import = None
		self._order_available_import = None
		self._user_info = None
		self._limit_process = None
		self._all_channel = dict()
		self._all_channel_by_id = dict()
		self._product_max_last_modified = ''
		self._order_max_last_modified = ''
		self._template_update = False
		self._custom_data = None
		self._extend_product_map = {}
		self._total_product = 0
		self._total_product_batch_import = 0
		self._product_need_refresh = []
		self._order_product_need_refresh = []
		self._live_process_id = False
		self._categories_path_by_id = {}
		self._new_sync_product_id = False
		self.is_sync_product_process = False
		self._is_feed_source = False
		self._currency_converter = False
		self._variants_update = {}
		self._all_templates = None

	def channel_setup(self):
		pass