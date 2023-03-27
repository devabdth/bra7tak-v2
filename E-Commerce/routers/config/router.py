from flask import Flask, render_template, request, session

import sys
sys.path.insert(0, '../')

from config import Config


class ConfigRouter:
	def __init__(self, app: Flask):
		self.app = app
		self.cfg: Config = Config()
		self.params = [
			"lang"
		]


	def setup(self):
		self.assign_config_router()

	def assign_config_router(self):
		@self.app.route('/config/', methods=["GET"])
		def website_config_index():
			params = dict(request.values)
			for param in params.keys():
				if param in self.params:
					session[param.upper()] = params[param]

			return self.app.response_class(status=200)
