import sys
sys.path.insert(0, '../')


from flask import Flask, render_template, session, url_for, redirect, request

from config import Config
from database.database import Database
from layout.layout import Layout
from content import Content
from utils import Utils

import json

class FavouritesRouter:
	def __init__(self, app: Flask):
		self.app= app
		self.cfg: Config= Config()
		self.content: Content= Content()
		self.database: Database= Database()
		self.layout: Layout= Layout()
		self.utils: Utils= Utils()


	def setup(self):
		self.assign_favourites_router()
		self.assign_add()
		self.assign_remove()

	def assign_add(self):
		@self.app.route('/favourites/add/', methods=["PATCH"])
		def favourites_add():
			try:
				body= dict(json.loads(request.data))
				uid= session.get("CURRENT_USER_ID", None)
				if uid is None:
					return self.app.response_class(status=405)

				user_data= self.database.users.get_user_by_id(uid)
				if user_data is None:
					return self.app.response_class(status=405)

				for prod in body['products']:
					user_data.favourites.append(prod['id'])

				self.database.users.update_user_data(uid, user_data)
				print(self.database.users.get_user_by_id(uid).favourites)

				return self.app.response_class(status= 200)
			except Exception as e:
				print(e)
				return self.app.response_class(status= 500)
	
	def assign_remove(self):
		@self.app.route('/favourites/remove/', methods=["PATCH"])
		def favourites_remove():
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
							if prod['id'] in user_data.favourites:
								user_data.favourites.remove(prod['id'])
					else:
						for _ in range(1, 1000):
							if prod['id'] in user_data.favourites:
								user_data.favourites.remove(prod['id'])


				self.database.users.update_user_data(uid, user_data)
				print(self.database.users.get_user_by_id(uid).favourites)

				return self.app.response_class(status= 200)
			except Exception as e:
				print(e)
				return self.app.response_class(status= 500)


	def assign_favourites_router(self):
		@self.app.route('/favourites/')
		@self.app.route('/favourite/')
		@self.app.route('/likes/')
		@self.app.route('/liked/')
		@self.app.route('/wishlist/')
		@self.app.route('/savedForLater/')
		def favourites_index():
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
				prods: list= self.database.products.get_multiple_products_by_id(user_data.favourites)

				return render_template(
					'favourites/index.html',
					prods= prods,
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

			return redirect('{}/login/?customRecall=favourites'.format(self.cfg.base_url))



