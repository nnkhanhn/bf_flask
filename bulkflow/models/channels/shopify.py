import copy
import csv
import io
import mimetypes
import urllib.parse
import math
from collections import defaultdict
from typing import Any, Dict, Union, List, Tuple
from datetime import datetime, timedelta
from requests.utils import requote_uri
from bs4 import BeautifulSoup
from bulkflow.models.base.channel import ModelChannel

class ShopifyChannel(ModelChannel):
	FORMAT_DATETIME = 'y-m-d h:i:s'
	TABLE_SHOPIFY_REVIEW = 'shopify_review'
	SP_MANU = 'manufacturers_table_construct'
	API_VERSION = '2023-01'
	TYPE_SMART_COLLECTION = 'smart'
	TYPE_CUSTOM_COLLECTION = 'custom'
	MAX_QTY = 1000000000
	ORDER_CANCEL_STATUSES = ["cancel", "canceled"]
	MAX_IMAGE_RESOLUTION = 20_971_520
	GRAPHQL_PATH = 'graphql.json'
	DIMENSION_METAFIELDS = ['length', 'width', 'height']
	PRODUCT_CODE_METAFIELDS = ['upc', 'ean', 'jan', 'isbn', 'mpn']
	MAX_IMG_NUMBER = 10
	MAX_ALLOW_VARIANTS = 100
	MAX_ALLOW_OPTIONS = 3
	MAX_CHARACTER_LENGTH = 255
	MAX_METAFIELD_NUMBER = 25
	DEFAULT_METAFIELD_NAMESPACE = 'custom'
	DEFAULT_METAFIELD_TYPE = 'single_line_text_field'
	EXTERNAL_VIDEO = 'EXTERNAL_VIDEO'
	MAX_PRODUCT_COLLECTION = 250
	SEO_METAFIELD_TYPE = 'string'
	SHOPIFY_MAX_COUNT = 10000
	GRAPHQL_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

	def __init__(self):
		super().__init__()
		self._api_url = None
		self._location_id = None
		self._theme_data = dict()
		self._shopify_countries = dict()
		self.last_header = ''
		self._allow_clear_warning = True
		self._version_api = None
		self._sales_channels = []

		def api_graphql(self, query: str, variables: Optional[Union[Dict[str, Any], None]] = None, add_version=True) -> Dict[str, Any]:
			"""
			Shopify GraphQL API

			Require API version >= 2023-01

			:param query:  string, GraphQL query
			:param variables: dict or None, GraphQL variables
			:param add_version: bool

			:return: dict, GraphQL response
			"""
			api_type = self.TYPE_POST
			path = self.GRAPHQL_PATH

			path = self.get_api_path(path, add_version)
			self._clear_entity_warning = self._allow_clear_warning
			self._total_time_sleep = 0
			header = {"Content-Type": "application/json"}
			# time.sleep(1)
			url = self.get_api_url() + '/' + to_str(path).strip('/')
			method = 'request_by_' + to_str(api_type).lower()

			data = {
				"query": query,
				**{"variables": variables if variables else None}
			}
			if not data:
				self.log('Expected queries or variables input', 'graphql_error')
			data = json_encode(data)

			api_password = self._notice[self._type]['config']['api']['password'] if self._notice[self._type]['config'][
				'api'].get('password') else self._notice[self._type]['config']['api'].get('token')
			header['X-Shopify-Access-Token'] = api_password
			res = getattr(self, method)(url, data, header)
			retry = 0
			while (json_decode(res) is False) or self.last_status >= 500:
				retry += 1
				self.sleep_time(20)
				res = getattr(self, method)(url, data, header)
				if retry > 5:
					break
			return res
