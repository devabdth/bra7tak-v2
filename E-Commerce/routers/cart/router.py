import sys
sys.path.insert(0, '../')

from flask import Flask, render_template, session, url_for, redirect, request
import json

from config import Config
from layout.layout import Layout
from database.database import Database
from content import Content
from utils import Utils


class CartRouter:
	def __init__(self, app: Flask):
		self.app= app
		self.layout: Layout= Layout()
		self.cfg: Config= Config()
		self.database: Database= Database()
		self.content: Content= Content()
		self.utils: Utils= Utils()


	def setup(self):
		self.assign_cart_router()
		self.assign_add()
		self.assign_remove()
		self.assign_clear_cart()

	def assign_add(self):
		@self.app.route('/cart/add/', methods=["PATCH"])
		def cart_add():
			try:
				body= dict(json.loads(request.data))
				uid= session.get("CURRENT_USER_ID", None)
				if uid is None:
					return self.app.response_class(status=405)

				user_data= self.database.users.get_user_by_id(uid)
				if user_data is None:
					return self.app.response_class(status=405)

				for prod in body['products']:
					for _ in range(prod['count']):
						user_data.cart.append({"id": prod['id'], "color": prod['color'] if 'color' in prod.keys() else "", "size": prod['size'] if 'size' in prod.keys() else ""})

				self.database.users.update_user_data(uid, user_data)
				print(self.database.users.get_user_by_id(uid).cart)

				return self.app.response_class(status= 200)
			except Exception as e:
				print(e)
				return self.app.response_class(status= 500)
	
	def assign_remove(self):
		@self.app.route('/cart/remove/', methods=["PATCH"])
		def cart_remove():
			try:
				body= dict(json.loads(request.data))
				uid= session.get("CURRENT_USER_ID", None)
				if uid is None:
					return self.app.response_class(status=405)


				user_data= self.database.users.get_user_by_id(uid)
				if user_data is None:
					print('User Data is None')
					return self.app.response_class(status= 500)

				for prod in body['products']:
					if prod['count'] != -1:
						for _ in range(1, prod['count']):
							if prod['id'] in user_data.cart:
								user_data.cart.remove(prod['id'])
					else:
						for _ in range(1, 1000):
							if prod['id'] in user_data.cart:
								user_data.cart.remove(prod['id'])


				self.database.users.update_user_data(uid, user_data)
				print(self.database.users.get_user_by_id(uid).cart)

				return self.app.response_class(status= 200)
			except Exception as e:
				print(e)
				return self.app.response_class(status= 500)

	def assign_clear_cart(self):
		@self.app.route('/cart/clear/', methods=["PATCH"])
		def clear_cart():
			try:
				uid= session.get("CURRENT_USER_ID", None)
				if uid is None:
					print('UID is None')
					return self.app.response_class(status= 500)

				user_data= self.database.users.get_user_by_id(uid)
				if user_data is None:
					print('User Data is None')
					return self.app.response_class(status= 500)

				user_data.cart= []
				self.database.users.update_user_data(uid, user_data)

				return self.app.response_class(status= 200)
			except Exception as e:
				print(e)
				return self.app.response_class(status= 500)

	def assign_cart_router(self):
		@self.app.route('/cart/', methods= ["GET"])
		def cart_index():
			self.database.categories.load()
			
			params= dict(request.values)
			fresh_prod= self.database.products.get_product_by_id(params['freshProduct']) if 'freshProduct' in params.keys() else None
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
					'cart/index.html',
					cart= self.utils.cart_calculations(user_data.cart, city_code= user_data.city_code),
					fresh_prod= fresh_prod,
					utils= self.utils,
					uid= uid,
					user_data= user_data,
					lang= lang,
					cfg= self.cfg,
					content= self.content,
					primary_font_family= primary_font_family,
					second_font_family= second_font_family,
					len= len,
					database= self.database,
					layout= self.layout
				)

			return redirect('{}/login/?customRecall=cart'.format(self.cfg.base_url))

