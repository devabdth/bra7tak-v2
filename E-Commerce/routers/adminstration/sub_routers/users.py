import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../../')


from flask import Flask, render_template, url_for, request, redirect, session

from config import Config
from database.database import Database
from utils import Utils
from content import Content

import json
class UsersSubRouter:
	def __init__(self, app: Flask):
		self.app: Flask= app
		self.cfg: Config= Config()
		self.database: Database= Database()
		self.utils: Utils= Utils()
		self.content: Content= Content()


	def setup(self):
		self.assign_users_index()
		self.assign_user_delete()


	def assign_user_delete(self):
		@self.app.route('/webapp/adminstration/users/', methods=["delete"])
		def user_delete_index():
			params= dict(request.values)
			if 'uid' not in params.keys():
				return self.app.response_class(status= 500)

			res: bool= self.database.users.delete_user(uid= params['uid'])
			if res:
				return self.app.response_class(status= 200)

			return self.app.response_class(status= 500)


	def assign_users_index(self):
		@self.app.route('/webapp/adminstration/users/', methods=["GET"])
		def users_index():
			params= dict(request.values)

			aid= session.get("CURRENT_ADMIN_ID", None)
			if aid is None:
				return redirect('{}/webapp/adminstration/login/'.format(self.cfg.base_url))

			admin_data= self.database.admins.get_admin_by_id(aid)
			users= self.database.users.get_all_users(params)
			return render_template(
				'adminstration/users/index.html',
				cfg= self.cfg,
				users= users,
				database= self.database,
				content= self.content,
				admin_data= admin_data,
				utils= self.utils,
				len= len,
				lang= "en",
				search_params= params,
				cats_ids= [cat.id for cat in self.database.categories.all_categories],
			)

