from flasgger import Swagger
from flask import Flask, request, jsonify
from flask_cors import CORS
from bulkflow.libs.utils import *
from app.main.middleware.auth import Auth
from marshmallow import Schema, fields

ROOT_DIR = get_root_path()

mode = get_config_ini('local', 'mode')
if mode == 'live':
	api_url = get_config_ini('server', 'api_url')
	if not api_url:
		print("Please add api_url in file dataprocessing/etc/config.ini.sample under section server")
		sys.exit()
app = Flask(__name__, template_folder = os.path.join(ROOT_DIR, 'app', 'documents', 'templates'))

swagger_config = {
	"headers": [
	],
	"specs": [
		{
			"endpoint": 'apispec_1',
			"route": '/apispec_1.json',
			"rule_filter": lambda rule: True,  # all in
			"model_filter": lambda tag: True,  # all in
		}
	],
	"static_url_path": "/flasgger_static",
	# "static_folder": "static",  # must be set by user
	"swagger_ui": True,
	"specs_route": "/sync_docs/",
}

swagger = Swagger(app, template_file = os.path.join(ROOT_DIR, 'app', 'documents', 'swagger.yml'), config = swagger_config)

app.wsgi_app = Auth(app.wsgi_app)
app.debug = to_bool(get_config_ini('local', 'debug', False))
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()
@app.route('/api1/hello', methods = ['GET'])
def hello():
	"""
    Greet the user.
    ---
    parameters:
      - name: name
        in: query
        type: string
        required: true
        description: The name of the user to greet.
    responses:
        200:
            description: A greeting message with the user's name.
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: "Hello, John!"
    """
	name = request.args.get('name')
	return jsonify({"message": f"Hello, {name}!"})



if __name__ == '__main__':
	port = to_int(get_config_ini('local', 'port'))
	app.run(host = '0.0.0.0', port = port)