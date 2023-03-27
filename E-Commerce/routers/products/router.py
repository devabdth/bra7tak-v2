from layout.layout import Layout
from database.database import Database
from content import Content
from config import Config
from utils import Utils
from flask import Flask, render_template, url_for, session, redirect
import sys
sys.path.insert(0, '../')


class ProductsRouter:
	def __init__(self, app: Flask):
		self.app: Flask = app
		self.content: Content = Content()
		self.database: Database = Database()
		self.layout: Layout = Layout()
		self.cfg: Config = Config()
		self.utils: Utils= Utils()

	def setup(self):
		self.assign_single_product_index()

	def assign_single_product_index(self):
		@self.app.route('/products/<prod_id>/', methods=["GET"])
		def single_product_index(prod_id):
			product = self.database.products.get_product_by_id(prod_id)
			if product == None:
				return redirect('{}/404/product/'.format(self.cfg.base_url))

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
					'products/single_product/index.html',
					user_data= user_data,
					product=product,
					category=self.database.categories.get_category_by_id(
						product.category),
					lang=lang,
					cfg=self.cfg,
					utils= self.utils,
					content=self.content,
					primary_font_family=primary_font_family,
					second_font_family=second_font_family,
					len=len,
					database=self.database,
					layout=self.layout

				)

			return render_template(
				'products/single_product/index.html',
				product=product,
				category=self.database.categories.get_category_by_id(
					product.category),
				lang=lang,
				cfg=self.cfg,
				utils= self.utils,
				content=self.content,
				primary_font_family=primary_font_family,
				second_font_family=second_font_family,
				len=len,
				database=self.database,
				layout=self.layout

			)
