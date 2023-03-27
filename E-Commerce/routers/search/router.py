import sys
sys.path.insert(0, '../')

from flask import Flask, render_template, url_for, session, request

from config import Config
from layout.layout import Layout
from content import Content
from database.database import Database
from utils import Utils


class SearchRouter:
	def __init__(self, app: Flask):
		self.app= app
		self.utils: Utils= Utils()
		self.cfg: Config= Config()
		self.layout: Layout= Layout()
		self.content: Content= Content()
		self.database: Database= Database()


	def setup(self):
		self.assign_search_index()

	def assign_search_index(self):
		@self.app.route('/search/', methods=["GET"])
		@self.app.route('/find/', methods=["GET"])
		@self.app.route('/specialPick/', methods=["GET"])
		@self.app.route('/pick/', methods=["GET"])
		@self.app.route('/filter/', methods=["GET"])
		@self.app.route('/filterization/', methods=["GET"])
		def search_index():
			params= dict(request.values)
			products: list= self.database.products.get_products_by_filterization(params)
			self.database.categories.load()
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
					'search/index.html',
					user_data= user_data,
					utils= self.utils,
					lang= lang,
					cfg= self.cfg,
					content= self.content,
					primary_font_family= primary_font_family,
					second_font_family= second_font_family,
					len= len,
					database= self.database,
					layout= self.layout,
					products= products,
					search_params= params,
					cats_ids= [cat.id for cat in self.database.categories.all_categories]
				)
			return render_template(
				'search/index.html',
				lang= lang,
				utils= self.utils,
				cfg= self.cfg,
				content= self.content,
				primary_font_family= primary_font_family,
				second_font_family= second_font_family,
				len= len,
				database= self.database,
				layout= self.layout,
				products= products,
				search_params= params,
				cats_ids= [cat.id for cat in self.database.categories.all_categories]
			)