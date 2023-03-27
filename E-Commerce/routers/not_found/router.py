import sys 
sys.path.insert(0, '../')

from flask import Flask, render_template, url_for, session

from database.database import Database
from content import Content
from config import Config


class NotFoundRouter:
	def __init__(self, app: Flask):
		self.app= app
		self.database: Database= Database()
		self.cfg: Config= Config()
		self.content: Content= Content()


	def setup(self):
		self.assign_not_found_product()
		self.assign_not_found_category()
		self.assign_not_found_collection()


	def assign_not_found_product(self):
		@self.app.route('/notFoundProduct/', methods=["GET"])
		@self.app.route('/404/product/', methods=["GET"])
		def not_found_product():
			lang = session.get("LANG", "en")
			uid= session.get("CURRENT_USER_ID", None)
			if lang == 'en':
				primary_font_family= 'Raleway'
				second_font_family= 'Poppins'
			elif lang == 'ar':
				primary_font_family= 'Cairo'
				second_font_family= 'Cairo'
			
			self.database.categories.load()

			if not uid is None:
				user_data= self.database.users.get_user_by_id(uid)
				return render_template(
					'not_found/product/index.html',
					uid= uid,
					user_data= user_data,
					lang= lang,
					cfg= self.cfg,
					content= self.content,
					primary_font_family= primary_font_family,
					second_font_family= second_font_family,
					database= self.database,
				)
			return render_template(
				'not_found/product/index.html',
				lang= lang,
				cfg= self.cfg,
				content= self.content,
				primary_font_family= primary_font_family,
				second_font_family= second_font_family,
				database= self.database,
			)




	def assign_not_found_category(self):
		@self.app.route('/notFoundCategory/', methods=["GET"])
		@self.app.route('/404/category/', methods=["GET"])
		def not_found_category():
			lang = session.get("LANG", "en")
			uid= session.get("CURRENT_USER_ID", None)
			if lang == 'en':
				primary_font_family= 'Raleway'
				second_font_family= 'Poppins'
			elif lang == 'ar':
				primary_font_family= 'Cairo'
				second_font_family= 'Cairo'
			if not uid is None:
				user_data= self.database.users.get_user_by_id(uid)
				return render_template(
					'not_found/category/index.html',
					uid= uid,
					user_data= user_data,
					lang= lang,
					cfg= self.cfg,
					content= self.content,
					primary_font_family= primary_font_family,
					second_font_family= second_font_family,
					database= self.database,
				)
			return render_template(
				'not_found/category/index.html',
				lang= lang,
				cfg= self.cfg,
				content= self.content,
				primary_font_family= primary_font_family,
				second_font_family= second_font_family,
				database= self.database,
			)




	def assign_not_found_collection(self):
		@self.app.route('/notFoundCollection/', methods=["GET"])
		@self.app.route('/404/collection/', methods=["GET"])
		def not_found_collection():
			lang = session.get("LANG", "en")
			uid= session.get("CURRENT_USER_ID", None)
			if lang == 'en':
				primary_font_family= 'Raleway'
				second_font_family= 'Poppins'
			elif lang == 'ar':
				primary_font_family= 'Cairo'
				second_font_family= 'Cairo'
			if not uid is None:
				user_data= self.database.users.get_user_by_id(uid)
				return render_template(
					'not_found/collection/index.html',
					uid= uid,
					user_data= user_data,
					lang= lang,
					cfg= self.cfg,
					content= self.content,
					primary_font_family= primary_font_family,
					second_font_family= second_font_family,
					database= self.database,
				)
			return render_template(
				'not_found/collection/index.html',
				lang= lang,
				cfg= self.cfg,
				content= self.content,
				primary_font_family= primary_font_family,
				second_font_family= second_font_family,
				database= self.database,
			)






