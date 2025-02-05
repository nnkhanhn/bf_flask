from flask import Blueprint, request as flask_request, jsonify

from bulkflow.libs.utils import json_decode, start_subprocess, response_success, get_flask_request_data

feed_path = Blueprint('feed_path', __name__)
@feed_path.route("feeds/daily-sync", methods = ['post'])
def daily_sync():
	request_data = get_flask_request_data()
	request_data['process_type'] = 'refresh'
	buffer = dict()
	buffer['controller'] = 'feed'
	buffer['action'] = 'feed_daily_sync'
	buffer['data'] = request_data
	create = start_subprocess(buffer, wait = False)
	return jsonify(response_success())
@feed_path.route("feeds/move-cluster", methods = ['post'])
def feed_move_cluster():
	request_data = get_flask_request_data()
	buffer = dict()
	buffer['controller'] = 'cluster'
	buffer['action'] = 'feed_move_cluster'
	buffer['data'] = request_data
	create = start_subprocess(buffer, wait = False)
	return jsonify(response_success())

@feed_path.route("feed-source/<int:source_id>/import", methods = ['post'])
def feed_source_import(source_id):
	request_data = get_flask_request_data()
	request_data['source_id'] = source_id
	request_data['process_type'] = 'product'
	buffer = dict()
	buffer['controller'] = 'feed'
	buffer['action'] = 'feed_source_import'
	buffer['data'] = request_data
	create = start_subprocess(buffer, wait = False)
	return jsonify(response_success())

@feed_path.route("feeds/<int:feed_id>", methods = ['delete'])
def feed_deleted(feed_id):
	request_data = get_flask_request_data()
	request_data['feed_id'] = feed_id
	buffer = dict()
	buffer['controller'] = 'feed'
	buffer['action'] = 'feed_deleted'
	buffer['data'] = request_data
	create = start_subprocess(buffer, wait = False)
	return jsonify(response_success())

@feed_path.route("feeds/<int:feed_id>/category/count/<int:position>", methods = ['post'])
def feed_category_count(feed_id, position):
	request_data = get_flask_request_data()
	request_data['feed_id'] = feed_id
	request_data['position'] = position
	buffer = dict()
	buffer['controller'] = 'feed'
	buffer['action'] = 'apply_category_rule'
	buffer['data'] = request_data
	create = start_subprocess(buffer, wait = False)
	return jsonify(response_success())

@feed_path.route("feeds/<int:feed_id>/finalize", methods = ['post'])
def feed_finalize(feed_id):
	request_data = get_flask_request_data()
	request_data['feed_id'] = feed_id
	buffer = dict()
	buffer['controller'] = 'feed'
	buffer['action'] = 'restart_finalize'
	buffer['data'] = request_data
	create = start_subprocess(buffer, wait = False)
	return jsonify(response_success())

@feed_path.route("feeds/<int:feed_id>/finalize/quality", methods = ['post'])
def feed_quality(feed_id):
	request_data = get_flask_request_data()
	request_data['feed_id'] = feed_id
	buffer = dict()
	buffer['controller'] = 'feed'
	buffer['action'] = 'apply_mappings'
	buffer['data'] = request_data
	create = start_subprocess(buffer, wait = False)
	return jsonify(response_success())

@feed_path.route("feeds/create_feed", methods = ['post'])
def getting_started():
	request_data = get_flask_request_data()
	buffer = dict()
	buffer['controller'] = 'feed'
	buffer['action'] = 'create_feed'
	buffer['data'] = request_data
	create = start_subprocess(buffer, wait = False)
	return jsonify(response_success(create))

@feed_path.route("feeds/<int:feed_id>/rules/delete", methods = ['post'])
def delete_rule(feed_id):
	request_data = get_flask_request_data()
	request_data['feed_id'] = feed_id
	buffer = dict()
	buffer['controller'] = 'feed'
	buffer['action'] = 'delete_rule'
	buffer['data'] = request_data
	create = start_subprocess(buffer, wait = False)
	return jsonify(response_success())

@feed_path.route("feeds/<int:feed_id>/rule/<string:rule_id>/init", methods = ['post'])
def init_rule(feed_id, rule_id):
	request_data = get_flask_request_data()
	request_data['feed_id'] = feed_id
	request_data['rule_id'] = rule_id
	buffer = dict()
	buffer['controller'] = 'feed'
	buffer['action'] = 'init_rule'
	buffer['data'] = request_data
	create = start_subprocess(buffer, wait = False)
	return jsonify(response_success())

@feed_path.route("feeds/<int:feed_id>/rule/<string:rule_id>/apply-rule", methods = ['post'])
def apply_rule(feed_id, rule_id):
	request_data = get_flask_request_data()
	request_data['feed_id'] = feed_id
	request_data['rule_id'] = rule_id
	buffer = dict()
	buffer['controller'] = 'feed'
	buffer['action'] = 'apply_rule'
	buffer['data'] = request_data
	create = start_subprocess(buffer, wait = False)
	return jsonify(response_success())

@feed_path.route("feed-source/<int:source_id>/verify_connection", methods = ['post'])
def feed_source_verify_connection(source_id):
	request_data = get_flask_request_data()
	request_data['source_id'] = source_id
	request_data['process_type'] = 'product'
	buffer = dict()
	buffer['controller'] = 'feed'
	buffer['action'] = 'feed_source_verify_connection'
	buffer['data'] = request_data
	verify = start_subprocess(buffer, wait = True)
	return jsonify(verify.to_dict())

@feed_path.route("feeds/<string:master_rule_id>/rule/<string:rule_id>/apply-rule", methods = ['post'])
def apply_rule_master_rule(master_rule_id, rule_id):
	request_data = get_flask_request_data()
	request_data['master_rule_id'] = master_rule_id
	request_data['rule_id'] = rule_id
	buffer = dict()
	buffer['controller'] = 'feed'
	buffer['action'] = 'apply_rule_master_rule'
	buffer['data'] = request_data
	create = start_subprocess(buffer, wait = False)
	return jsonify(response_success())

@feed_path.route("feeds/<string:master_rule_id>/rule/<string:rule_id>/init", methods = ['post'])
def init_rule_master_rule(master_rule_id, rule_id):
	request_data = get_flask_request_data()
	request_data['master_rule_id'] = master_rule_id
	request_data['rule_id'] = rule_id
	buffer = dict()
	buffer['controller'] = 'feed'
	buffer['action'] = 'init_rule_master_rule'
	buffer['data'] = request_data
	create = start_subprocess(buffer, wait = False)
	return jsonify(response_success())