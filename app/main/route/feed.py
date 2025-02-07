from flask import Blueprint, request as flask_request, jsonify

from bulkflow.libs.utils import json_decode, start_subprocess, response_success, get_flask_request_data

feed_path = Blueprint('feed_path', __name__)

@feed_path.route("feeds/create_feed", methods = ['post'])
def create_feed():
	'''
	file: ../../../app/documents/docs/feed/create.yml
	'''
	request_data = get_flask_request_data()
	buffer = dict()
	buffer['controller'] = 'feed'
	buffer['action'] = 'create_feed'
	buffer['data'] = request_data
	create = start_subprocess(buffer, wait = True)
	return jsonify(response_success(create))
