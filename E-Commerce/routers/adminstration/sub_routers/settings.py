import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../../')


from flask import Flask, render_template, url_for, request, redirect, session, send_file

from config import Config
from database.database import Database
from utils import Utils
from content import Content

import json
class SettingsSubRouter:
	def __init__(self, app: Flask):
		self.app: Flask= app
		self.cfg: Config= Config()
		self.database: Database= Database()
		self.utils: Utils= Utils()
		self.content: Content= Content()


	def setup(self):
		self.assign_settings_index()
		self.assign_setting_delete_admin()
		self.assign_settings_create_admin()

	def assign_settings_create_admin(self):
		@self.app.route('/webapp/adminstration/settings/', methods=["POST"])
		def post_admin():

			aid= session.get("CURRENT_ADMIN_ID", None)
			if aid is None:
				return redirect('{}/webapp/adminstration/login/'.format(self.cfg.base_url))

			body= dict(json.loads(request.data))
			res= self.database.admins.create_admin(body)
			if res:
				return self.app.response_class(status= 201)
			return self.app.response_class(status= 500)

	def assign_setting_delete_admin(self):
		@self.app.route('/webapp/adminstration/settings/', methods=["DELETE"])
		def delete_admin():
			params= dict(request.values)

			aid= session.get("CURRENT_ADMIN_ID", None)
			if aid is None:
				return redirect('{}/webapp/adminstration/login/'.format(self.cfg.base_url))

			if 'key' in params.keys() and 'aid' in params.keys():
				if params['aid']== aid:
					if 'CURRENT_ADMIN_ID' in session:
						session.pop('CURRENT_ADMIN_ID')

				if params['key'] != self.cfg.meta_key:
					return self.app.response_class(status= 405)

				res= self.database.admins.delete_admin(params['aid'])

				if res:
					return self.app.response_class(status= 200)
			return self.app.response_class(status= 500)


	def assign_settings_index(self):
		@self.app.route('/webapp/adminstration/settings/', methods=["GET"])
		@self.app.route('/webapp/adminstration/', methods=["GET"])
		def settings_index():
			params= dict(request.values)

			aid= session.get("CURRENT_ADMIN_ID", None)
			if aid is None:
				return redirect('{}/webapp/adminstration/login/'.format(self.cfg.base_url))

			admin_data= self.database.admins.get_admin_by_id(aid)
			return render_template(
				'adminstration/settings/index.html',
				cfg= self.cfg,
				database= self.database,
				content= self.content,
				admin_data= admin_data,
				utils= self.utils,
				len= len,
				lang= "en",
				search_params= params,
				cats_ids= [cat.id for cat in self.database.categories.all_categories],
				accesses= self.utils.accesses
			)
