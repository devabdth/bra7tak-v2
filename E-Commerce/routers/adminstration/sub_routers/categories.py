import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../../')


from flask import Flask, render_template, url_for, request, redirect, session

from config import Config
from database.database import Database
from utils import Utils
from content import Content

import json
class CategoriesSubRouter:
	def __init__(self, app: Flask):
		self.app: Flask= app
		self.cfg: Config= Config()
		self.database: Database= Database()
		self.utils: Utils= Utils()
		self.content: Content= Content()


	def setup(self):
		self.assign_categories_index()
		self.assign_categories_update()
		self.assign_categories_create()
		self.assign_categories_delete()

	def assign_categories_delete(self):
		@self.app.route('/webapp/adminstration/categories/', methods=["DELETE"])
		def categories_delete():
			params= dict(request.values)
			if not 'cid' in params.keys():
				return self.app.response_class(status= 500)

			res= self.database.categories.delete_category(params['cid'])
			if res:
				return self.app.response_class(status= 200)

			return self.app.response_class(status= 500)

	def assign_categories_update(self):
		@self.app.route('/webapp/adminstration/categories/', methods=["PATCH"])
		def categories_update():
			try:
				params= dict(request.values)
				body= dict(request.form)
				category= dict(json.loads(body['category']))
				icon= request.files['icon'] if 'icon' in request.files.keys() else None
				cover= request.files['cover'] if 'cover' in request.files.keys() else None
				res= self.database.categories.update_category(category, icon= icon, cover= cover)
				if res:
					return self.app.response_class(status= 200)

				return self.app.response_class(status= 500)
			except Exception as e:
				print(e)
				return self.app.response_class(status= 500)


	def assign_categories_create(self):
		@self.app.route('/webapp/adminstration/categories/', methods=["POST"])
		def categories_create():
			try:
				params= dict(request.values)
				body= dict(request.form)
				category= dict(json.loads(body['category']))
				icon= request.files['icon'] if 'icon' in request.files.keys() else None
				cover= request.files['cover'] if 'cover' in request.files.keys() else None
				res= self.database.categories.create_category(category, icon= icon, cover= cover)
				if res:
					return self.app.response_class(status= 201)

				return self.app.response_class(status= 500)
			except Exception as e:
				print(e)
				return self.app.response_class(status= 500)



	def assign_categories_index(self):
		@self.app.route('/webapp/adminstration/categories/', methods=["GET"])
		def categories_index():
			params= dict(request.values)

			aid= session.get("CURRENT_ADMIN_ID", None)
			if aid is None:
				return redirect('{}/webapp/adminstration/login/'.format(self.cfg.base_url))

			admin_data= self.database.admins.get_admin_by_id(aid)
			self.database.categories.load()
			categories= self.database.categories.all_categories
			return render_template(
				'adminstration/categories/index.html',
				cfg= self.cfg,
				categories= categories,
				database= self.database,
				content= self.content,
				admin_data= admin_data,
				utils= self.utils,
				len= len,
				lang= "en",
				search_params= params,
				cats_ids= [cat.id for cat in self.database.categories.all_categories],
			)

