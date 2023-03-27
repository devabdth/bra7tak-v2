import sys
sys.path.insert(0, '../')

from flask import Flask, render_template, url_for, session

from config import Config
from content import Content
from database.database import Database
from layout.layout import Layout
from utils import Utils

class HomeRouter:
	def __init__(self, app: Flask):
		self.cfg: Config = Config()
		self.app = app
		self.content: Content= Content()
		self.database: Database= Database()
		self.layout: Layout= Layout()
		self.utils: Utils= Utils()


	def setup(self):
		self.assign_index()

	def assign_index(self):
		@self.app.route('/', methods=['GET'])
		@self.app.route('/home/', methods=['GET'])
		@self.app.route('/index/', methods=['GET'])
		@self.app.route('/main/', methods=['GET'])
		@self.app.route('/landingPage/', methods=['GET'])
		@self.app.route('/landingpage/', methods=['GET'])
		@self.app.route('/landing%20page/', methods=['GET'])

		def home_index():
			self.database.categories.load()
			
			lang = session.get("LANG", "en")
			uid= session.get("CURRENT_USER_ID", None)
			if lang == 'en':
				primary_font_family= 'Raleway'
				second_font_family= 'Poppins'
			elif lang == 'ar':
				primary_font_family= 'Cairo'
				second_font_family= 'Cairo'
			self.layout.load()
			if not uid is None:
				user_data= self.database.users.get_user_by_id(uid)
				return render_template(
					'home/index.html',
					uid= uid,
					user_data= user_data,
					lang= lang,
					cfg= self.cfg,
					content= self.content,
					primary_font_family= primary_font_family,
					second_font_family= second_font_family,
					len= len,
					database= self.database,
					layout= self.layout,
					utils= self.utils
				)
			return render_template(
				'home/index.html',
				lang= lang,
				cfg= self.cfg,
				content= self.content,
				primary_font_family= primary_font_family,
				second_font_family= second_font_family,
				len= len,
				database= self.database,
				layout= self.layout,
				utils= self.utils
			)



