from layout.layout import Layout
from database.database import Database
from content import Content
from config import Config

from flask import Flask, render_template, url_for, session, redirect 

import sys
sys.path.insert(0, '../')


class SignUpRouter:
	def __init__(self, app: Flask):
		self.app: Flask = app
		self.content: Content = Content()
		self.database: Database = Database()
		self.layout: Layout = Layout()
		self.cfg: Config = Config()

	def setup(self):
		self.assign_signup_index()

	def assign_signup_index(self):
		@self.app.route('/signup/', methods=["GET"])
		@self.app.route('/signUp/', methods=["GET"])
		@self.app.route('/joinUs/', methods=["GET"])
		@self.app.route('/join/', methods=["GET"])
		@self.app.route('/enroll/', methods=["GET"])
		@self.app.route('/newUser/', methods=["GET"])
		def signup_index():
			if session.get('CURRENT_USER_ID', None) != None:
				return redirect('/profile/')
			lang = session.get("LANG", "en")
			if lang == 'en':
				primary_font_family = 'Raleway'
				second_font_family = 'Poppins'
			elif lang == 'ar':
				primary_font_family = 'Cairo'
				second_font_family = 'Cairo'

			return render_template(
				'signup/index.html',
				lang=lang,
				cfg=self.cfg,
				content=self.content,
				primary_font_family=primary_font_family,
				second_font_family=second_font_family,
				database=self.database,
				layout=self.layout,
				len=len

			)
