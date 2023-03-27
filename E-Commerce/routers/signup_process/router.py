from layout.layout import Layout
from database.database import Database
from content import Content
from config import Config
from plugins.email_plugin import EmailPlugin

from flask import Flask, render_template, url_for, session, request, redirect

import sys
sys.path.insert(0, '../')

import random
import json

class SignUpProcessRouter:
	def __init__(self, app: Flask):
		self.app: Flask = app
		self.content: Content = Content()
		self.database: Database = Database()
		self.layout: Layout = Layout()
		self.cfg: Config = Config()


	def setup(self):
		self.assign_signup_process_router()
		self.assign_confirm_code_router()
		self.assign_change_email()
		self.assign_send_code_again()
		self.assign_save_user_data()

	def assign_save_user_data(self):
		@self.app.route('/confirmSignUp/', methods=["POST"])
		def confirm_sign_up():
			try:
				email = session.get('CURRENT_USER_EMAIL', None)
				password = session.get('CURRENT_USER_PASSWORD', None)
				
				body = dict(json.loads(request.data))
				body['email'] = email
				body['password'] = password
				print(session)

				print(body)

				res = self.database.users.create_user(body)
				if not res is None:
					session.pop('CURRENT_USER_PASSWORD')
					session['CURRENT_USER_ID'] = str(res)
					return self.app.response_class(status=201)
				else:
					return self.app.response_class(status=500)
			except Exception as e:
				print(e)
				return self.app.response_class(status=500)


	def assign_change_email(self):
		@self.app.route('/changeEmail/', methods=["GET"])
		def website_change_email():
			if "CURRENT_USER_EMAIL" in session:
				session.pop('CURRENT_USER_EMAIL')
			return redirect('{}/signup/'.format(self.cfg.base_url))

	def assign_send_code_again(self):
		@self.app.route('/sendCodeAgain/', methods=["GET"])
		def website_send_code_again():
			try:
				code = str(random.randint(0, 9999))
				recipent= session.get('CURRENT_USER_EMAIL', None) 
				if recipent == None:
					return self.app.response_class(status=500)

				EmailPlugin().send_raw_email(
					msg= 'Welcome to Bra7tak! Your verfication code is: {}'.format(code),
					recipent= recipent,
					subject="Verify your Email"
				)
				session["CurrentEmailConfirmationCode"] = code
				return self.app.response_class(status=200)

			except Exception as e:
				print(e)
				return self.app.response_class(status=500)

	def assign_confirm_code_router(self):
		@self.app.route('/completeSignUp/confrimCode/', methods=["GET"])
		def website_confirm_code():
			code = session.get('CurrentEmailConfirmationCode', None)
			code_ = dict(request.values)['code']
			if str(code) == str(code_):
				return self.app.response_class(status=200)
			else:
				return self.app.response_class(status=401)

			

			return self.app.response_class(status=500)


	def assign_signup_process_router(self):
		@self.app.route('/completeSignUp/', methods=["GET"])
		@self.app.route('/signUpProcess/', methods=["GET"])
		def website_signupprocess_index():
			if session.get('CURRENT_USER_ID', None) != None:
				return redirect('/profile/')

			params = dict(request.values)
			lang = session.get("LANG", "en")
			current_user_email = session.get('CURRENT_USER_EMAIL', None)
			current_user_password = session.get('CURRENT_USER_PASSWORD', None)

			if lang == 'en':
				primary_font_family= 'Raleway'
				second_font_family= 'Poppins'
			elif lang == 'ar':
				primary_font_family= 'Cairo'
				second_font_family= 'Cairo'

			# if current_user_email is None or current_user_password is None:
			# 	return redirect('{}/signup/'.format(self.cfg.base_url))

			return render_template(
				'signupProcess/index.html',
				lang=lang,
				cfg=self.cfg,
				content=self.content,
				primary_font_family=primary_font_family,
				second_font_family=second_font_family,
				database=self.database,
				layout=self.layout,
				email= current_user_email,
			)
			