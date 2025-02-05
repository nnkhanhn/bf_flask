import base64
import configparser
import copy
import hashlib
import hmac
import html
import importlib
import json
import math
import os
import random
import re
import shutil
import socket
import struct
import subprocess
import sys
import traceback
import urllib.parse
import validators as python_validators
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from uuid import UUID

import six
import xmltodict
from bs4 import BeautifulSoup
from bson import ObjectId
from flask import request as flask_request
from packaging import version
from phpserialize import *

# from libs.base_thread import BaseThread
from prodict import Prodict

LIMIT_LINE_ERROR = 200
COLLETION_state = 'state'
MIGRATION_FULL = 2
MIGRATION_DEMO = 1
GROUP_USER = 1
GROUP_TEST = 2
STATUS_NEW = 1
STATUS_RUN = 2
STATUS_STOP = 3
STATUS_COMPLETED = 4
STATUS_KILL = 5
STATUS_CONFIGURING = 6
STATUS_PAYMENT = 7
DIR_UPLOAD = 'uploads'
BASE_DIR = 'bulkflow'

CONFIG_FILE = 'bulkflow/etc/docs.ini'
DIR_PROCESS = 'processes/'
FLAG_STOP = 1
FLAG_KILL_ALL = 2
APP_LOG_SINGLE = 'single'
APP_LOG_DAILY = 'daily'
APP_LOG_CUSTOM = 'custom'
LOG_SINGLE = ('process', 'attributes')
import time

import jwt


class Authorization:
	PREFIX = 'lit'


	def __init__(self, **kwargs):
		self._private_key = kwargs.get('private_key', get_config_ini('local', 'private_key'))
		self._user_id = kwargs.get('user_id')


	def encode(self, data = None, insert_prefix = True):
		if not data:
			data = dict()
		data['time'] = str(int(time.time()))
		data['user_id'] = self._user_id
		jwt_token = jwt.encode(data, self._private_key, algorithm = 'HS256')
		if isinstance(jwt_token, bytes):
			jwt_token = jwt_token.decode()
		if insert_prefix:
			jwt_token = f"{self.PREFIX} {jwt_token}"
		return jwt_token


	def decode(self, authorization):
		if not authorization or not isinstance(authorization, str):
			return False
		authorization = authorization.split(' ')
		if len(authorization) != 2 and authorization[0] != self.PREFIX:
			return False
		try:
			data = jwt.decode(authorization[1], self._private_key, algorithms = ['HS256'])
		except jwt.exceptions.InvalidSignatureError as e:
			return False
		except Exception as e:
			return False
		return data


	def get_user_id(self, authorization):
		data = self.decode(authorization)
		if not data:
			return self.get_user_id_default()
		return data.get('user_id', self.get_user_id_default())


	def get_user_id_from_flask_request(self):
		authorization = flask_request.environ.get('HTTP_AUTHORIZATION')
		if not authorization:
			return self.get_user_id_default()
		return self.get_user_id(authorization)


	def get_user_id_default(self):
		if to_bool(get_config_ini('local', 'is_local')):
			return get_config_ini('local', 'user_id_default')
		return 0


def get_value_by_key_in_dict(dictionary, key, default = None):
	if not dictionary or not isinstance(dictionary, dict):
		return default
	if key in dictionary:
		return dictionary[key] if dictionary[key] else default
	return default


def check_pid(pid):
	if not to_int(pid):
		return False
	pid = to_int(pid)
	""" Check For the existence of a unix pid. """
	try:
		os.kill(pid, 0)
	except OSError:
		return False
	else:
		return True


def get_controller(controller_name, data = None):
	# if controller_name == 'base':
	# 	if data:
	# 		my_instance = BaseThread(data)
	# 	else:
	# 		my_instance = BaseThread()
	# 	return my_instance
	try:
		module_class = importlib.import_module(BASE_DIR + '.controllers.' + controller_name)
	except Exception as e:
		log_traceback()
		return None
	class_name = "Controller{}".format(controller_name.capitalize())
	my_class = getattr(module_class, class_name)
	# if data:
	my_instance = my_class(data)
	# else:
	# 	my_instance = my_class()
	return my_instance


def get_model(name, data = None, class_name = None):
	if not name:
		return None
	# name_path = name.replace('_', '/')
	file_path = os.path.join(get_root_path(), BASE_DIR, 'models', *name.split('.')) + '.py'
	file_model = Path(file_path)
	if not file_model.is_file():
		return None
	name_path = name.split('_')
	model_name = BASE_DIR + ".models." + name.replace('/', '.')
	module_class = importlib.import_module(model_name)
	class_name = class_name if class_name else get_model_class_name(name)

	try:
		model_class = getattr(module_class, class_name)
		if data:
			model = model_class(data)
		else:
			model = model_class()
		return model
	except Exception as e:
		log_traceback(type_error = 'get_model')
		return None


def get_model_class_name(name, char = '/'):
	name = name.replace(BASE_DIR, '')
	split = re.split(r'[^a-z0-9]', name)
	upper = list(map(lambda x: x.capitalize(), split))
	new_name = 'Model' + ''.join(upper)
	return new_name


def md5(s, raw_output = False):
	res = hashlib.md5(s.encode())
	if raw_output:
		return res.digest()
	return res.hexdigest()


def hash_hmac(algo, data, key):
	res = hmac.new(key.encode(), data.encode(), algo).hexdigest()
	return to_str(res)


def to_str(value):
	if isinstance(value, bool):
		return str(value)
	if (isinstance(value, int) or isinstance(value, float)) and value == 0:
		return '0'
	if not value:
		return ''
	if isinstance(value, dict) or isinstance(value, list):
		return json_encode(value)
	if hasattr(value, 'to_json'):
		return getattr(value, 'to_json')()
	try:
		value = str(value)
		return value
	except Exception:
		return ''


def change_permissions_recursive(path, mode = 0o755):
	os.chmod(path, mode)
	for root, dirs, files in os.walk(path):
		for sub_dir in dirs:
			os.chmod(os.path.join(root, sub_dir), mode)
		for sub_file in files:
			os.chmod(os.path.join(root, sub_file), mode)


def to_timestamp_or_false(value, str_format = '%Y-%m-%d %H:%M:%S', limit_len = True):
	if limit_len:
		value = value[0:19]
	try:
		timestamp = int(time.mktime(time.strptime(value, str_format)))
		if timestamp:
			return timestamp
		return False
	except:
		return False


def to_timestamp(value, str_format = '%Y-%m-%d %H:%M:%S', limit_len = True):
	if limit_len:
		value = value[0:19]
	try:
		timestamp = int(time.mktime(time.strptime(value, str_format)))
		if timestamp:
			return timestamp
		return int(time.time())
	except:
		return int(time.time())


def to_int(value):
	if not value:
		return 0
	try:
		value = int(float(value))
		return value
	except Exception:
		return 0


def to_bool(value):
	if isinstance(value, str):
		if value.lower().strip() == 'false':
			return False
	if value:
		return True
	return False


def to_object_id(value):
	if not value:
		return False
	try:
		value = ObjectId(value)
		return value
	except Exception:
		return False


def to_decimal(value, length = None):
	if not value:
		return 0.00
	try:
		value = round(float(value), length) if length else float(value)
		return value
	except Exception:
		return 0.00


def is_decimal(value):
	try:
		value = float(value)
		return True
	except Exception:
		return False


def is_float_nan(value):
	if not is_decimal(value):
		return False
	value = to_decimal(value)
	return math.isnan(value)


def to_len(value):
	if not value:
		return 0
	try:
		res = len(value)
	except Exception:
		res = 0
	return res


def isoformat_to_datetime(value):
	if len(value) == 29:
		value = value[0:19] + value[23:]
	if len(value) == 25:
		value = value[0:22] + value[23:]
	if len(value) == 20 and value[-1] == 'Z':
		value = value.replace('Z', '+0000')
	if value[-1] == 'Z':
		value = f'{value[0:19]}+0000'
	try:
		data = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
	except Exception:
		data = datetime.strptime(value[0:19], "%Y-%m-%dT%H:%M:%S")
	return data


def dict_key_to_str(dict_data: dict):
	if not dict_data:
		return dict_data
	new_data = dict()
	for k, v in dict_data.items():
		k = str(k)
		if isinstance(v, dict):
			v = dict_key_to_str(v)
		new_data[k] = v
	return new_data


def convert_format_time(time_data, old_format = '%Y-%m-%d %H:%M:%S', new_format = '%Y-%m-%d %H:%M:%S', limit_length = True):
	if old_format == '%Y-%m-%d %H:%M:%S':
		time_data = to_str(time_data).replace('T', ' ')
	if to_int(re.sub('[^0-9]', '', to_str(time_data))) == 0:
		return None
	try:
		if to_str(time_data).isnumeric():
			timestamp = datetime.fromtimestamp(to_int(time_data))
			res = timestamp.strftime(new_format)
			return res
		if not old_format:
			old_format = '%Y-%m-%d %H:%M:%S'
		time_data = time_data[0:19] if limit_length else time_data
		new_time = datetime.strptime(time_data, old_format)
		res = new_time.strftime(new_format)
		return res

	except Exception:
		# log_traceback()
		return get_current_time(new_format)


def print_time(thread_name):
	time.sleep(10)
	print("%s: %s" % (thread_name, time.ctime(time.time())))


def gmdate(str_format, int_time_stamp = None):
	if not int_time_stamp:
		return time.strftime(str_format, time.gmtime())
	else:
		return time.strftime(str_format, time.gmtime(int_time_stamp))


def log_no_date(msg, prefix_path = None, type_error = 'exceptions'):
	prefix_path = to_str(prefix_path)
	type_error = to_str(type_error.replace('.log', ''))
	file_log = '{}.log'.format(type_error)

	file_log = os.path.join(get_pub_path(), 'log', prefix_path, file_log)
	folder_log = os.path.dirname(file_log)
	if not os.path.isdir(folder_log):
		os.makedirs(folder_log)
		change_permissions_recursive(folder_log, 0o777)
	# if os.path.exists(file_log) and os.path.getsize(file_log) >= 10485760:
	# 	os.remove(file_log)

	msg = f"{to_str(msg)}\n"
	check_exist = False
	if os.path.isfile(file_log):
		check_exist = True
	with open(file_log, 'a') as log_file:
		log_file.write(msg)
	if not check_exist and os.path.isfile(file_log):
		os.chmod(file_log, 0o777)


def log(msg, prefix_path = None, type_error = 'exceptions'):
	prefix_path = to_str(prefix_path)
	type_error = to_str(type_error.replace('.log', ''))
	app_log = get_config_ini('local', 'app_log')
	if not app_log:
		app_log = APP_LOG_DAILY
	if app_log == APP_LOG_SINGLE or type_error in LOG_SINGLE:
		file_log = '{}.log'.format(type_error)
	elif app_log == APP_LOG_DAILY:
		file_log = '{}_{}.log'.format(type_error, get_current_time("%Y-%m-%d"))
	else:
		file_log = get_config_ini('local', 'log_file', 'exceptions.log')
	file_log = os.path.join(get_pub_path(), 'log', prefix_path, file_log)
	folder_log = os.path.dirname(file_log)
	if not os.path.isdir(folder_log):
		os.makedirs(folder_log)
		change_permissions_recursive(folder_log, 0o777)
	if os.path.exists(file_log) and os.path.getsize(file_log) >= 10485760:
		os.remove(file_log)
	msg_log = '{}: \n{}'

	msg = to_str(msg)
	ts = time.strftime('%Y/%m/%d %H:%M:%S')
	msg_log = msg_log.format(ts, msg).rstrip('\n')
	msg_log += "\n{}\n".format("-" * 100)
	check_exist = False
	if os.path.isfile(file_log):
		check_exist = True
	with open(file_log, 'a') as log_file:
		log_file.write(msg_log)
	if not check_exist and os.path.isfile(file_log):
		os.chmod(file_log, 0o777)


def clear_log(migration_id):
	if not migration_id:
		return response_success()
	path = get_pub_path() + '/log/' + str(migration_id)
	if os.path.isdir(path):
		shutil.rmtree(path)
	return response_success()


def log_traceback(prefix = None, type_error = 'exceptions'):
	error = traceback.format_exc()
	log(error, prefix, type_error)


def get_default_format_date():
	return "%Y-%m-%d %H:%M:%S"


def diff_month(d1, d2):
	return (d1.year - d2.year) * 12 + d1.month - d2.month


def get_current_time(str_format = '%Y-%m-%d %H:%M:%S'):
	try:
		current_time = time.strftime(str_format)
	except Exception:
		current_time = time.strftime(get_default_format_date())
	return current_time


def ip2long(ip):
	"""
	Convert an IP string to long
	"""
	try:
		packedIP = socket.inet_aton(ip)
		res = struct.unpack("!L", packedIP)[0]
	except Exception:
		res = ''
	return res


# response
def create_response(result = '', msg = '', data = None):
	return Prodict(**{'result': result, 'msg': msg, 'data': data})


def response_error(msg = ''):
	return create_response('error', msg)


def response_api(msg = ''):
	return create_response('api', msg)


def response_success(data = None, msg = ''):
	return create_response('success', msg, data)


def response_warning(msg = None):
	return create_response('warning', msg)


# base64
def string_to_base64(s):
	if not isinstance(s, str):
		s = str(s)
	return base64.b64encode(s.encode('utf-8')).decode('utf-8')


def base64_to_string(b):
	try:
		s = base64.b64decode(b).decode('utf-8')
		return s
	except Exception as e:
		try:
			s = base64.b64decode(b.encode('utf-8')).decode('utf-8')
			return s
		except Exception as e:
			# log_traceback()
			return None


def php_serialize(obj):
	try:
		res = serialize(obj).decode('utf-8')
	except Exception as e:
		res = False
	return res


def php_unserialize(str_serialize):
	try:
		res = unserialize(str_serialize.encode('utf-8'))
	except Exception:
		try:
			res = unserialize(str_serialize)
		except Exception:
			res = False
	res = decode_after_unserialize(res)
	if isinstance(res, dict):
		keys = list(res.keys())
		keys = list(map(lambda x: to_str(x), keys))
		keys.sort()
		for index, key in enumerate(keys):
			if to_str(index) != to_str(key):
				return res
		res = list(res.values())
	return res


def decode_after_unserialize(data):
	res = None
	if isinstance(data, dict):
		res = dict()
		for k, v in data.items():
			try:
				key = k.decode('utf-8')
			except Exception:
				key = k
			if isinstance(v, dict):
				value = decode_after_unserialize(v)
			else:
				try:
					value = v.decode('utf-8')
				except Exception:
					value = v
			res[key] = value
	elif isinstance(data, list):
		res = list()
		for row in data:
			value = decode_after_unserialize(row)
			res.append(value)
	else:
		try:
			res = data.decode('utf-8')
		except Exception:
			res = data
	return res


# Get one array from list array by field value
def get_row_from_list_by_field(data, field, value):
	result = dict()
	if not data or not field:
		return result
	for row in data:
		if (field in row) and str(row[field]) == str(value):
			result = row
			break
	return result


# Get array value from list array by field value and key of field need
def get_row_value_from_list_by_field(data, field, value, need):
	if not data:
		return False
	row = get_row_from_list_by_field(data, field, value)
	if not row:
		return False
	row = dict(row)
	return row.get(need, False)


# Get and unique array value by key
def duplicate_field_value_from_list(data, field):
	result = list()
	if not data:
		return result
	data = list(data)
	for item in data:
		if to_str(field) in item:
			result.append(item[field])
	result = list(set(result))
	return result


# Get list array from list by list field value
def get_list_from_list_by_list_field(data, field, values):
	if not data or not field:
		return list()
	if not isinstance(data, list):
		values = [values]
	values = list(map(lambda x: to_str(x), values))
	result = list()
	try:
		for row in data:
			if to_str(row[field]) in values:
				result.append(row)
	except Exception:
		return list()
	return result


# Get list array from list by field  value
def get_list_from_list_by_field(data, field, value):
	if not data:
		return list()
	result = list()
	try:
		for row in data:
			if isinstance(value, list):
				for item in value:
					if to_str(row[field]) == to_str(item):
						result.append(row)
			else:
				if to_str(row[field]) == to_str(value):
					result.append(row)
	except Exception:
		return list()
	return result


# url
def strip_domain_from_url(url):
	parse = urllib.parse.urlparse(url)
	path_url = parse.path
	query = parse.query
	fragment = parse.fragment
	if query:
		path_url += '?' + query
	if fragment:
		path_url += '#' + fragment
	return path_url


def join_url_path(url, path_url):
	full_url = url.rstrip('/')
	if path_url:
		full_url += '/' + path_url.lstrip('/')
	return full_url


def send_data_socket(data, conn):
	if isinstance(data, list) or isinstance(data, dict):
		data = json_encode(data)
	data = str(data).encode('utf-8')
	conn.send(data)
	conn.close()


def get_root_path():
	path = os.path.dirname(os.path.abspath(__file__))
	path = path.replace('/bulkflow/libs', '')
	return path


def get_pub_path():
	path = get_root_path()
	if 'pub' in path:
		index = path.find('pub')
		path = path[0:index]
	path = path.rstrip('/') + '/pub'
	return path


def console_success(msg):
	result = '<p class="success"> - ' + msg + '</p>'
	return result


def console_error(msg):
	result = '<p class="error"> - ' + msg + '</p>'
	return result


def console_warning(msg):
	result = '<p class="warning"> - ' + msg + '</p>'
	return result


# json
def json_decode(data):
	try:
		data = json.loads(data)
	except Exception:
		try:
			data = json.loads(data.decode('utf-8'))
		except Exception:
			data = False
	return data if isinstance(data, (list, dict)) else False


def json_encode(data):
	try:
		data = json.dumps(data)
	except Exception:
		data = False
	return data


def clone_code_for_migration_id(migration_id):
	if check_folder_clone(migration_id):
		return True
	base_dir = get_pub_path() + '/' + DIR_PROCESS + to_str(migration_id)
	if not os.path.isdir(base_dir):
		os.makedirs(base_dir)
	folder_copy = ['controllers', 'libs', 'models']
	file_copy = ['bootstrap.py']
	for folder in folder_copy:
		if os.path.isdir(base_dir + '/' + BASE_DIR + '/' + folder):
			continue
		shutil.copytree(BASE_DIR + '/' + folder, base_dir + '/' + BASE_DIR + '/' + folder)
	for file in file_copy:
		if os.path.isfile(base_dir + '/' + file):
			continue
		shutil.copy(file, base_dir + '/' + file)

	git_ignore_file = base_dir + '/' + '.gitignore'
	f = open(git_ignore_file, "w+")
	f.write('*')
	change_permissions_recursive(base_dir, 0o777)


def clone_code(prefix):
	if check_folder_clone(prefix):
		return True
	destination_dir = os.path.join(get_pub_path(), 'clone', prefix, BASE_DIR)
	base_dir = os.path.join(get_root_path(), BASE_DIR)
	if not os.path.isdir(destination_dir):
		os.makedirs(destination_dir)
	folder_copy = ['controllers', 'libs', 'models']
	file_copy = ['bootstrap.py']
	for folder in folder_copy:
		if os.path.isdir(os.path.join(destination_dir, folder)):
			continue
		shutil.copytree(os.path.join(base_dir, folder), os.path.join(destination_dir, folder))
	for file in file_copy:
		if os.path.isfile(os.path.join(destination_dir, '..', file)):
			continue
		shutil.copy(os.path.join(get_root_path(), file), os.path.join(destination_dir, '..', file))

	git_ignore_file = destination_dir + '/' + '.gitignore'
	f = open(git_ignore_file, "w+")
	f.write('*')
	change_permissions_recursive(destination_dir, 0o777)


def clone_code_for_user(user_id):
	prefix = os.path.join('users', to_str(user_id))
	clone_code(prefix)


def clone_code_for_process(process_id):
	prefix = os.path.join(DIR_PROCESS, to_str(process_id))
	clone_code(prefix)


# destination_dir = os.path.join(get_pub_path(), DIR_PROCESS, to_str(process_id), BASE_DIR)
# base_dir = os.path.join(get_root_path(), BASE_DIR)
# if not os.path.isdir(destination_dir):
# 	os.makedirs(destination_dir)
# folder_copy = ['controllers', 'libs', 'models']
# file_copy = ['bootstrap.py']
# for folder in folder_copy:
# 	if os.path.isdir(os.path.join(destination_dir, folder)):
# 		continue
# 	shutil.copytree(os.path.join(base_dir, folder), os.path.join(destination_dir, folder))
# for file in file_copy:
# 	if os.path.isfile(os.path.join(destination_dir, '..', file)):
# 		continue
# 	shutil.copy(os.path.join(get_root_path(), file), os.path.join(destination_dir, '..', file))
#
# git_ignore_file = destination_dir + '/' + '.gitignore'
# f = open(git_ignore_file, "w+")
# f.write('*')
# change_permissions_recursive(destination_dir, 0o777)
def get_python_path():
	if is_local():
		return "python"
	root_path = get_root_path()
	return os.path.join(root_path, 'venv', 'bin', 'python')

def start_subprocess(buffer = None, wait = False):
	data = buffer.get('data') or dict()
	if not data.get('user_id'):
		user_id = Authorization().get_user_id_from_flask_request()
		data['user_id'] = user_id
		buffer['data'] = data
	sync_id = to_str(data.get('sync_id'))
	user_id = to_str(data.get('user_id'))
	list_special = ['reset_migration', 'clone_migration', 'stop_auto_test', 'restart_migration', 'kill_end_loop_migration', 'kill_migration', 'delete_migration']
	action = buffer.get('action')
	path = None
	if action not in list_special:
		if user_id and check_folder_clone(os.path.join('users', user_id)):
			path = os.path.join(get_pub_path(), 'clone', 'users', user_id)
		if sync_id and check_folder_clone(os.path.join(DIR_PROCESS, sync_id)):
			path = os.path.join(get_pub_path(), 'clone', DIR_PROCESS, sync_id)

		if path and to_decimal(os.path.getctime(path)) < to_decimal(get_config_ini('local', 'time_clone', 1589795205)):
			old_path = path + '_v30'
			os.rename(path, old_path)
			clone_code_for_migration_id(sync_id)
			folder_clear = '/sync/models/cart'
			shutil.rmtree(path + folder_clear)
			shutil.copytree(old_path + folder_clear, path + folder_clear)

	if not path:
		path = get_root_path()
	if wait:
		proc = subprocess.Popen([get_python_path(), path + '/bootstrap.py', json_encode(buffer)], stdout = subprocess.PIPE, bufsize = 1)
		data = ''
		while True:
			line = proc.stdout.readline().decode('utf8')
			if line != '':
				data += line
			else:
				break
		data = data.splitlines()
		if data:
			data = data[-1]
		decode_data = json_decode(data)
		if isinstance(decode_data, dict):
			return Prodict(**decode_data)
		return decode_data
	else:
		subprocess.Popen([get_python_path(), path + '/bootstrap.py', json_encode(buffer)])


def start_autotest(auto_test_id):
	dir_test = 'test/' + str(auto_test_id)
	if auto_test_id and check_folder_clone(dir_test):
		path = get_pub_path() + '/' + DIR_PROCESS + dir_test
	else:
		path = get_root_path()
	buffer = {
		'auto_test_id': auto_test_id
	}
	subprocess.Popen(['python3', path + '/autotest.py', json_encode(buffer)])


def check_folder_clone(prefix):
	path = get_pub_path()
	if not isinstance(prefix, str):
		prefix = str(prefix)
	base_dir = os.path.join(path, 'clone', prefix)
	if not os.path.isdir(base_dir):
		return False
	folder_check = ['controllers', 'libs', 'models']
	file_check = ['bootstrap.py']
	for folder in folder_check:
		if not os.path.isdir(base_dir + '/' + BASE_DIR + '/' + folder):
			return False
	for file in file_check:
		if not os.path.isfile(base_dir + '/' + file):
			return False
	return True


def clear_folder_clone(migration_id):
	path = get_pub_path()
	if not isinstance(migration_id, str):
		migration_id = str(migration_id)
	base_dir = path + '/' + DIR_PROCESS + str(migration_id)
	if not os.path.isdir(base_dir):
		return True
	shutil.rmtree(base_dir)
	return True


def response_from_subprocess(data, conn = True):
	if conn:
		if isinstance(data, list) or isinstance(data, dict):
			data = json_encode(data)
		print(data, end = '')
		sys.exit(1)
	return data


def get_ini_file_content(file):
	config_file = os.path.join(get_pub_path(), '..', 'etc', file)
	if os.path.isfile(config_file):
		config = configparser.ConfigParser()
		config.read(config_file)
		return config
	return False


def get_config_ini(section, key = None, default = None, migration_id = None, file = 'config.ini'):
	if file == 'config.ini':
		if not globals().get('config_ini'):
			global config_ini
			config_ini = get_ini_file_content(file)
		else:
			config_ini = globals().get('config_ini')

	else:
		if not globals().get('local_ini'):
			global local_ini
			config_ini = get_ini_file_content(file)
		else:
			config_ini = globals().get('local_ini')
	try:
		if not key:
			return config_ini[section]
		value = config_ini[section][key]
		return value
	except Exception as e:
		return default

	return default


def parse_version(str_version):
	return version.parse(str_version)


def get_content_log_file(migration_id, path_file = 'exceptions_top', is_limit = True, limit_line = None):
	if migration_id:
		log_file = get_pub_path() + '/log/' + to_str(migration_id) + '/' + path_file + '.log'
	else:
		log_file = get_pub_path() + '/log/' + path_file + '.log'
	lines = list()
	_limit = to_int(limit_line if limit_line else LIMIT_LINE_ERROR)
	if os.path.isfile(log_file):
		file_handle = open(log_file, "r")
		line_lists = file_handle.readlines()
		file_handle.close()
		if (not is_limit) or (to_len(line_lists) <= _limit):
			lines = line_lists
		else:
			index = 0 - _limit
			while index <= -1:
				lines.append(line_lists[index])
				index += 1
	return lines


def update_nested_dict(d, u):
	import collections.abc
	for k, v in u.items():
		if isinstance(v, collections.abc.Mapping):
			d[k] = update_nested_dict(d.get(k, {}), v)
		else:
			d[k] = v
	return d


def url_to_link(url, link = None, target = '_blank'):
	if not url:
		return ''
	if not link:
		link = url
	return "<a href='{}' target='{}'>{}</a>".format(url, target, link)


def get_random_useragent():
	user_agent = '''
		Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36
		Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36
		'''
	user_agent = user_agent.splitlines()
	user_agent = list(map(lambda x: to_str(x).strip('\t'), user_agent))
	user_agent = list(filter(lambda x: len(x) > 0, user_agent))
	return random.choice(user_agent)


def random_string(length = 16, lower = False, have_number = True):
	chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
	if have_number:
		chars += "0123456789"
	string = "".join(random.choice(chars) for _ in six.moves.xrange(length))
	return string if not lower else string.lower()


class StripHtml(HTMLParser):
	def __init__(self):
		super().__init__()
		self.reset()
		self.strict = False
		self.convert_charrefs = True
		self.fed = []


	def handle_data(self, d):
		self.fed.append(d)


	def get_data(self):
		return ''.join(self.fed)


def strip_html_tag(html, none_check = False):
	if not html:
		return ''
	s = StripHtml()
	s.feed(to_str(html))
	return s.get_data()


def get_jwt_token(data, private_key = None):
	if not private_key:
		private_key = get_config_ini('server', 'private_key')
	if not data.get('time'):
		data['time'] = to_str(to_int(time.time()))
	jwt_token = jwt.encode(data, private_key, algorithm = 'HS256')
	if isinstance(jwt_token, bytes):
		jwt_token = jwt_token.decode()
	return jwt_token


def get_api_server_url(path = None):
	api_url = get_config_ini('server', 'ngrok_url', get_config_ini('server', 'api_url'))
	if to_str(path):
		api_url += '/' + to_str(path).strip('/')
	return api_url


def get_server_callback(path = None, prefix = 'api/v1'):
	api_url = get_config_ini('callback', 'ngrok_url', get_config_ini('callback', 'api_url'))
	api_url = f"{api_url.strip('/')}/{prefix.strip()}"
	if to_str(path):
		api_url += '/' + to_str(path).strip('/')
	return api_url


def get_app_url(path = ""):
	server_url = get_config_ini('server', 'app_url').strip('/')
	if path:
		server_url += "/" + path.strip('/')
	return server_url


def html_unescape(string):
	string = to_str(string)
	if not string:
		return ''
	return html.unescape(string)


def html_escape(string, quote = False):
	string = to_str(string)
	if not string:
		return ''
	res = html.escape(string)
	if quote:
		res = res.replace('&#x27;', "&#39;")
	return res


def html_unquote(string):
	if not string:
		return ''
	return urllib.parse.unquote(string)


def is_local():
	return to_str(get_config_ini('local', 'mode', 'test')) == 'test' or to_bool(get_config_ini('local', 'is_local')) == True


def xml_to_dict(xml_data):
	try:
		data = xmltodict.parse(xml_data)
	except Exception:
		log_traceback()
		data = False
	return Prodict.from_dict(data)


def obj_to_list(obj):
	if not obj:
		return obj
	if not isinstance(obj, list):
		obj = [obj]
	return obj


def strip_none(data):
	if isinstance(data, dict):
		return {k: strip_none(v) for k, v in data.items() if k is not None and v is not None and not (isinstance(v, dict) and not v)}
	elif isinstance(data, list):
		return [strip_none(item) for item in data if item is not None]
	elif isinstance(data, tuple):
		return tuple(strip_none(item) for item in data if item is not None)
	elif isinstance(data, set):
		return {strip_none(item) for item in data if item is not None}
	else:
		return data


def get_flask_request_data():
	request_data = flask_request.data
	if isinstance(request_data, bytes):
		request_data = request_data.decode()
	request_data = json_decode(request_data)
	if not request_data:
		request_data = dict()
	return request_data


def is_uuid(string, uuid_version = 4):
	try:
		uuid_obj = UUID(string, version = uuid_version)
	except ValueError:
		return False
	return str(uuid_obj) == string


def nl2br(string, is_xhtml = True, forced = False):
	string = to_str(string)
	if not string:
		return ''
	if bool(BeautifulSoup(string, "html.parser").find()) and not forced:
		return string
	if is_xhtml:
		return string.replace('\n', '<br />\n')
	else:
		return string.replace('\n', '<br>\n')


def rounding_price(rounding, price):
	price = to_decimal(price, 2)
	if rounding == 'nearest_010':
		return to_decimal(price, 1)
	if rounding == 'nearest_099':
		price = to_int(price * 100)
		price = (price // 100) * 100 + 100 - 1
		return to_decimal(price / 100)
	if rounding == 'nearest_095':
		price = to_int(price * 100)
		residuals = price % 100
		if residuals > 95:
			price += 100
		price = (price // 100) * 100 + 100 - 5
		return to_decimal(price / 100)
	if rounding == 'nearest_09':
		price = to_int(price * 100)
		residuals = price % 100
		if residuals > 90:
			price += 100
		price = (price // 100) * 100 + 100 - 10
		return to_decimal(price / 100)
	if rounding == 'nearest_1':
		return math.ceil(price)
	if rounding == 'nearest_10':
		price = math.ceil(price)
		residuals = price % 10
		if not residuals:
			return price
		return (price // 10) * 10 + 10
	if rounding == 'nearest_5':
		return nearest_base(price)
	if rounding == 'nearest_9':
		price = math.ceil(price)
		return price// 10 * 10 + 9
	if rounding == 'nearest_990':
		price = math.floor(price)
		residuals = price % 10
		if residuals:
			price = (price // 10) * 10
			price -= 10 if residuals < 5 else 0
		return price + 9.9
	if rounding == 'nearest_1099':
		price = math.floor(price)
		residuals = price % 10
		if residuals:
			price = (price // 10) * 10 + 10
		return price + 0.99
	return price


def nearest_base(x, base = 5):
	return base * round(x / base)


def get_server_id():
	return get_config_ini('server', 'id')


def remove_emojis(text, is_remove = False):
	if not is_remove:
		return text
	text = to_str(text)
	if not text:
		return ''
	emoj = re.compile("["
	                  u"\U0001F600-\U0001F64F"  # emoticons
	                  u"\U0001F300-\U0001F5FF"  # symbols & pictographs
	                  u"\U0001F680-\U0001F6FF"  # transport & map symbols
	                  u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
	                  u"\U00002500-\U00002BEF"  # chinese char
	                  u"\U00002702-\U000027B0"
	                  u"\U00002702-\U000027B0"
	                  u"\U000024C2-\U0001F251"
	                  u"\U0001f926-\U0001f937"
	                  u"\U00010000-\U0010ffff"
	                  u"\u2640-\u2642"
	                  u"\u2600-\u2B55"
	                  u"\u200d"
	                  u"\u23cf"
	                  u"\u23e9"
	                  u"\u231a"
	                  u"\ufe0f"  # dingbats
	                  u"\u3030"
	                  "]+", re.UNICODE)
	return re.sub(emoj, '', text)


def split_list(list_data, length):
	number_array = math.ceil(to_len(list_data) / length)
	return split_list_by_numberarray(list_data, number_array)

def split_list_by_numberarray(list_data, number_array):
	if not isinstance(list_data, list) or not list_data:
		return []
	list_convert_data = []
	for row in list_data:
		if isinstance(row, Prodict):
			row = row.to_dict()
		list_convert_data.append(row)
	import numpy as np
	try:
		array = np.array(list_convert_data)
	except:
		c = 3
		return [list_data]
	new_list = list(map(lambda x: list(x), np.array_split(array, number_array)))
	new_list_return = []
	for row in new_list:
		new_row_return = []
		for a in row:
			if isinstance(a, dict):
				a = Prodict.from_dict(a)
			new_row_return.append(a)
		new_list_return.append(new_row_return)
	return new_list_return

def is_starts_with_digit(s):
    return bool(re.match(r'^\d', s))

def replace_leading_digits_with_underscore(s):
    if is_starts_with_digit(s):
       return re.sub(r'^\d+', '_', s)
    return s


def attribute_name_to_code(name, strip_underscore = False):
	str_convert = html.unescape(name)
	if isinstance(str_convert, bool):
		if str_convert:
			str_convert = 'yes'
		else:
			str_convert = 'no'
	result = str_convert.replace(' ', '-').replace('-', '_')
	result = result.replace('/', '')
	if result.startswith('c.'):
		result = 'c.' + to_str(result[2:].replace('.', ''))
	elif result.startswith('{{c.'):
		result = '{{' + 'c.' + to_str(result[4:].replace('.', ''))
	else:
		result = result.replace('.', '')
	result = ''.join(e for e in result if e.isalnum() or e in ['_', '.'])
	result = result.strip(' .')
	while result.find('__') != -1:
		result = result.replace('__', '_')
	result = result.strip(' .').lower()
	if strip_underscore:
		result = result.strip('_')
	if is_starts_with_digit(result):
		result = '_' + result
	return result


def csv_encodings():
	return ['utf-8', 'cp1252', 'latin1', 'latin1-1', 'iso-8859-1', 'unicode_escape','utf-16']


def replace_duplicate_character(elm, chars):
	if not chars:
		return elm
	elm = to_str(elm)
	if not isinstance(chars, list):
		chars = [chars]
	for char in chars:
		while elm.find(char*2) != -1:
			elm = elm.replace(char*2, char)
	return elm


def split_by_title_word(s):
	return [chunk for chunk in re.split(r"([A-Z][a-z]+)", s) if chunk]


def round_off(value, length = 0):
	try:
		value = float(value)
	except:
		return 0
	integer_part, decimal_part = str(value).split('.')
	if not int(decimal_part):
		if not length:
			return int(value)
		return float(value)
	if str(decimal_part).endswith('5'):
		decimal_part = f'{decimal_part}1'
	value = float(f'{integer_part}.{decimal_part}')
	if not length:
		return round(value)
	return round(value, length)


def set_nested_value(data, keys, value):
	for key in keys[:-1]:
		data = data.setdefault(key, {})
	data[keys[-1]] = value

def is_valid_url(url):
	if not url:
		return False
	return python_validators.url(url)

def split_by_upper_case(string):
	return re.findall('[A-Z][^A-Z]*', string)

def string_to_function_name(string):
	string = split_by_upper_case(string)
	return '_'.join(string).lower()
