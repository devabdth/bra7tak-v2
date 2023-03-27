import sys
sys.path.insert(0, '../')


from flask import Flask, render_template, url_for, session, redirect

from config import Config
from content import Content
from database.database import Database
from layout.layout import Layout
from utils import Utils

class ProfileRouter:
	def __init__(self, app: Flask):
		self.app= app
		self.cfg: Config= Config()
		self.content: Content= Content()
		self.database: Database= Database()
		self.layout: Layout= Layout()
		self.utils: Utils= Utils()


	def setup(self):
		self.assign_profile_router()


	def assign_profile_router(self):
		@self.app.route('/profile/', methods=["GET"])
		def profile_index():
			uid: str= session.get('CURRENT_USER_ID', None)
			user_data= self.database.users.get_user_by_id(uid)
			print(user_data.to_dict())
			user_orders= self.database.orders.get_orders_by_uid(uid)
			lang = session.get("LANG", "en")
			if lang == 'en':
				primary_font_family= 'Raleway'
				second_font_family= 'Poppins'
			elif lang == 'ar':
				primary_font_family= 'Cairo'
				second_font_family= 'Cairo'
			return render_template(
				'profile/index.html',
				user_data= user_data,
				orders= user_orders,
				lang= lang,
				cfg= self.cfg,
				utils= self.utils,
				content= self.content,
				primary_font_family= primary_font_family,
				second_font_family= second_font_family,
				len= len,
				database= self.database,
				layout= self.layout
			)

