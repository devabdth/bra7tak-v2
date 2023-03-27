import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../../')


from flask import Flask, render_template, url_for, request, redirect, session

from config import Config
from database.database import Database
from utils import Utils
from content import Content

import json
class AuthSubRouter:
	def __init__(self, app: Flask):
		self.app: Flask= app
		self.cfg: Config= Config()
		self.database: Database= Database()
		self.utils: Utils= Utils()
		self.content: Content= Content()


	def setup(self):
		self.assign_logout()
		self.assign_login()
		self.assign_login_operation()


	def assign_login_operation(self):
		@self.app.route('/webapp/adminstration/login/', methods=['PATCH'])
		def login_operation():
			try:
				body= dict(json.loads(request.data))
				admin= self.database.admins.get_admin_by_username(body['username'])

				if admin != None and admin['accessKey'] == body['accessKey']:
					session['CURRENT_ADMIN_ID']= admin['aid']
					return self.app.response_class(status= 200)
				elif admin != None and admin['accessKey'] != body['accessKey']:
					return self.app.response_class(status= 403)
				elif admin == None:
					return self.app.response_class(status= 404)
				
				return self.app.response_class(status= 500)
			except Exception as e:
				print(e)
				return self.app.response_class(status= 500)
		

	def assign_login(self):
		@self.app.route('/webapp/adminstration/login/')
		def admin_login():
			return render_template(
				'adminstration/login/index.html'
			)


	def assign_logout(self):
		@self.app.route('/webapp/adminstration/logout/')
		def admin_logout():
			try:
				if session.get('CURRENT_ADMIN_ID', None) is None:
					return self.app.response_class(status= 200)


				session.pop('CURRENT_ADMIN_ID')
				return self.app.response_class(status= 200)
			except Exception as e:
				print(e)
				return self.app.response_class(status= 500)

			

