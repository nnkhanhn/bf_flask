import io
import re

import math

import pandas as pandas
import requests

from bulkflow.libs.errors import Errors
from bulkflow.libs.response import Response
from bulkflow.libs.utils import *
from bs4 import BeautifulSoup

class CsvFile():
	_mapping: dict


	def __init__(self, **kwargs):
		self._csv_data = None
		self._format = kwargs.get('format')
		self._mapping = kwargs.get('mapping')
		self._delimiter = kwargs.get('delimiter', ',')
		self._error = None
		self._encoding = None
		self._user_id = kwargs.get('user_id')
		self._channel_id = kwargs.get('channel_id')
		self._process_id = kwargs.get('process_id')


	def log_traceback(self, type_error = 'exceptions', msg = ''):
		error = traceback.format_exc()
		if msg:
			error += "\n" + to_str(msg)
		self.log(error, type_error)


	def log(self, msg, log_type = 'exceptions'):
		prefix = "user/" + to_str(self._user_id)
		if self._channel_id:
			prefix = os.path.join('channel', to_str(self._channel_id))
		prefix = os.path.join(prefix, 'file')
		if self._process_id:
			prefix = os.path.join(prefix, to_str(self._process_id))
		log(msg, prefix, log_type)


	def is_litcommerce_template(self):
		return self._format == 'litc'


	def construct_products_csv_file(self):
		title = "sku,parent_sku,name,description,qty,brand,condition,condition_note,price,msrp,seo_url,manufacturer,mpn,upc,ean,isbn,gtin,gcid,asin,epid,height,length,width,dimension_units,weight,weight_units,variation_1,variation_2,variation_3,variation_4,variation_5,product_image_1,product_image_2,product_image_3,product_image_4,product_image_5,product_image_6,product_image_7,product_image_8,product_image_9,product_image_10,attributes,categories"
		return title.split(',')


	def get_file_title(self):
		file_content = self.get_csv_data()
		return list(file_content[0].keys())


	def validate_file(self, file_content = None, setup = False):
		if not file_content:
			file_content = self.get_csv_data(setup)
		if not file_content:
			if self._error:
				return self._error
			return Response().error(Errors.CSV_FILE_NOT_MATCH)
		if self.is_litcommerce_template():
			first_line = list(file_content[0].keys())
			csv_title_default = self.construct_products_csv_file()
			csv_diff = list(set(csv_title_default) - set(first_line))
			if csv_diff and (len(csv_diff) > 1 or csv_diff[0] != 'product_id'):
				return Response().error(Errors.CSV_FILE_NOT_MATCH)
			return Response().success()
		return self.validate_file_with_mapping(file_content)


	def validate_file_with_mapping(self, file_content = None):
		if not file_content:
			file_content = self.get_csv_data()
		if not file_content:
			return Response().error(Errors.CSV_FILE_NOT_MATCH)
		first_line = list(map(lambda x: to_str(x).lower().strip('"').strip("'"), list(file_content[0].keys())))
		field_missing = []
		for field in self._mapping.values():
			try:
				field_mapping = to_str(field).lower().encode().decode('utf-8-sig')
			except:
				field_mapping = to_str(field).lower()
			field_mapping = field_mapping.strip('"').strip("'")
			if field_mapping not in first_line:
				field_missing.append(field)
		if not field_missing:
			return Response().success()
		return Response().error(msg = Errors().get_msg_error(Errors.CSV_FILE_MISSING_FIELD).format(','.join(field_missing)))


	def to_list(self):
		if self._csv_data:
			return self._csv_data
		file_content = self.get_csv_data()
		validate = self.validate_file(file_content)
		if validate.result != Response.SUCCESS:
			return {}
		return file_content


	def get_csv_data(self, setup = False) -> dict or None:
		if self._csv_data:
			return self._csv_data
		encoding = csv_encodings()
		read_file_false = False
		try:
			read_file = self.get_file_content(setup)
		except:
			read_file_false = True
			read_file = False
		if not read_file:
			read_file_false = True
		if read_file_false:
			return Response().error(msg = "Currently, we are unable to read your file. Please check the file again and wait for the next synchronization, or please click the 'Start Progress' button to synchronize immediately.")
		if read_file.result != Response.SUCCESS:
			self._error = read_file
			return None
		file_data = read_file.data
		csv_file_data = read_file.data
		if isinstance(file_data, bytes):
			csv_file_data = file_data.decode('utf-8')
		for encode in encoding:
			try:
				data_csv = pandas.read_csv(io.StringIO(csv_file_data), sep = self._delimiter, encoding = encode, low_memory = False, na_values = None, error_bad_lines = False, dtype = {'sku': str, 'parent_sku': str})
				data_csv = data_csv.T.to_dict()
				self._csv_data = list(data_csv.values())
				return self._csv_data
			except:
				continue
		try:
			df = pandas.read_excel(io.BytesIO(csv_file_data.encode(self._encoding or 'utf-8')), engine = 'openpyxl')  # can also index sheet by name or fetch all sheets
			data_csv = df.to_dict('records')
			self._csv_data = data_csv

			return data_csv
		except Exception as e:
			self.log_traceback()
			pass
		return None


	def get_file_content(self, setup = False):
		return Response().success('')