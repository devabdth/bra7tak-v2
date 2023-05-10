import sys
sys.path.insert(0, '../')

from flask import Flask, request, session, redirect
import json

from config import Config
from database.database import Database

class UsersRouter:
	def __init__(self, app: Flask):
		self.app: Flask= app
		self.cfg: Config= Config()
		self.database: Database= Database()


	def setup(self):
		self.assign_login_index()
		self.assign_logout_index()
		self.assign_signup_index()

	def assign_login_index(self):
		@self.app.route('/users/login/', methods=["PATCH"])
		def login():
			params: dict= dict(json.loads(request.data))
			username= params['username']
			password= params['password']
			user_data= self.database.users.get_user_by_username(username) or None
			if user_data is None:
				return self.app.response_class(status= 404)

			if user_data.password != password:
				return self.app.response_class(status= 301)

			session['CURRENT_USER_ID'] = user_data.id
			session['CURRENT_USER_EMAIL'] = user_data.email
			return self.app.response_class(status= 200)


	def assign_logout_index(self):
		@self.app.route('/users/logout/', methods=["GET"])
		def logout():
			if session.get('CURRENT_USER_ID', None) is None:
				return redirect('{}/login/'.format(self.cfg.base_url))


			session.pop('CURRENT_USER_ID')
			session.pop('CURRENT_USER_EMAIL')
			return redirect('{}'.format(self.cfg.base_url))


	def assign_signup_index(self):
		@self.app.route('/users/signup/', methods=["POST"])
		def signup():
			params: dict= dict(json.loads(request.data))
			username= params['email']
			password= params['password']

			if not self.database.users.check_email_uniquness(username):
				return self.app.response_class(status= 203)

			try:
				session['CURRENT_USER_EMAIL'] = username
				session['CURRENT_USER_PASSWORD']= password
				return self.app.response_class(status= 201)
			except Exception as _:
				return self.app.response_class(status= 500)

