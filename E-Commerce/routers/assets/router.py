import sys
sys.path.insert(0, '../')


from flask import Flask, render_template, url_for, session, send_file
import os

from config import Config
from content import Content
from database.database import Database

class AssetsRouter:
	def __init__(self, app: Flask):
		self.cfg: Config= Config()
		self.app= app

		self.supported_exts= [
			'png', 'jpeg', 'jpg', 'gif', 'jfjf'
		]


	def setup(self):
		self.assign_categories_icons()
		self.assign_categories_covers()
		self.assign_collections_covers()
		self.assign_product_name()
		self.assign_order_bar_code()
		self.assign_banners_assets()

	def assign_categories_icons(self):
		@self.app.route('/assets/categories/icons/<cat_id>', methods=["GET"])
		def categories_icons_index(cat_id):
			for ext in self.supported_exts:
				path_= os.path.abspath(os.path.join(os.path.dirname(__file__), './categories/icons/{}.{}'.format(cat_id, ext)))
				if os.path.exists(path_):
					return send_file(path_)

	def assign_banners_assets(self):
		@self.app.route('/assets/banners/assets/<bid>', methods=["GET"])
		def banners_assets_index(bid):
			for ext in self.supported_exts:
				path_= os.path.abspath(os.path.join(os.path.dirname(__file__), './banners/{}.{}'.format(bid, ext)))
				if os.path.exists(path_):
					return send_file(path_)

	def assign_categories_covers(self):
		@self.app.route('/assets/categories/covers/<cat_id>', methods=["GET"])
		def categories_covers_index(cat_id):
			for ext in self.supported_exts:
				path_= os.path.abspath(os.path.join(os.path.dirname(__file__), './categories/covers/{}.{}'.format(cat_id, ext)))
				if os.path.exists(path_):
					return send_file(path_)


	def assign_collections_covers(self):
		@self.app.route('/assets/collections/covers/<cat_id>', methods=["GET"])
		def collections_covers_index(cat_id):
			for ext in self.supported_exts:
				path_= os.path.abspath(os.path.join(os.path.dirname(__file__), './collections/covers/{}.{}'.format(cat_id, ext)))
				if os.path.exists(path_):
					return send_file(path_)


	def assign_product_name(self):
		@self.app.route('/assets/products/name/<prod_name>/', methods=["GET"])
		def product_by_name_index(prod_name):
			path_= os.path.abspath(os.path.join(os.path.dirname(__file__), './products/{}'.format(prod_name)))
			return send_file(path_)

	def assign_order_bar_code(self):
		@self.app.route('/assets/orders/barcode/<order_id>/', methods=["GET"])
		def order_bar_code_index(order_id):
			if not Database().orders.get_order_by_id(order_id) is None:
				import qrcode
				from io import BytesIO
				qr = qrcode.make(order_id)
				buf= BytesIO()
				qr.save(buf)
				buf.seek(0)
				return send_file(buf, mimetype='image/jpeg')


			return self.app.response_class(status=404)

