import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../../')


from flask import Flask, render_template, url_for, request, redirect, session

from config import Config
from database.database import Database
from utils import Utils
from content import Content
from layout.layout import Layout

import json
class BannersSubRouter:
	def __init__(self, app: Flask):
		self.app: Flask= app
		self.cfg: Config= Config()
		self.database: Database= Database()
		self.utils: Utils= Utils()
		self.content: Content= Content()
		self.layout: Layout= Layout()


	def setup(self):
		self.assign_banners_index()
		self.assing_banners_update()


	def assing_banners_update(self):
		@self.app.route('/webapp/adminstration/banners/', methods=["PATCH"])
		def update_banner():
			try:
				params= dict(request.values)
				if not 'bid' in params.keys():
					return self.app.response_class(status= 500)
				body= dict(request.form)

				banner_dict= json.loads(body['banner'])
				banner_dict['id']= params['bid']
				banner_dict['asset']= "{}.png".format(banner_dict['id'])
				if 'asset' in request.files.keys():
					import os
					
					banner_asset= request.files['asset']
					banner_asset.filename= '{}.png'.format(banner_dict['id'])
					if not os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__),'../../assets/banners/'))):
						os.mkdir(os.path.abspath(os.path.join(os.path.dirname(__file__),'../../assets/banners/')))
					banner_asset.save(os.path.abspath(os.path.join(os.path.dirname(__file__),'../../assets/banners/'+banner_asset.filename)))

				res: bool= self.layout.update_banner(banner_dict)
				if res:
					self.layout.load()
					return self.app.response_class(status= 200)

				return self.app.response_class(status= 500)
			except Exception as e:
				print(e)
				return self.app.response_class(status= 500)


	def assign_banner_delete(self):
		@self.app.route('/webapp/adminstration/banners/', methods=["delete"])
		def banner_delete_index():
			params= dict(request.values)
			if 'uid' not in params.keys():
				return self.app.response_class(status= 500)

			res: bool= self.database.banners.delete_banner(uid= params['uid'])
			if res:
				return self.app.response_class(status= 200)

			return self.app.response_class(status= 500)


	def assign_banners_index(self):
		@self.app.route('/webapp/adminstration/banners/', methods=["GET"])
		def banners_index():
			params= dict(request.values)

			aid= session.get("CURRENT_ADMIN_ID", None)
			if aid is None:
				return redirect('{}/webapp/adminstration/login/'.format(self.cfg.base_url))

			admin_data= self.database.admins.get_admin_by_id(aid)
			self.layout.load()
			banners= self.layout.all_banners
			return render_template(
				'adminstration/banners/index.html',
				cfg= self.cfg,
				banners= banners,
				layout= self.layout,
				database= self.database,
				content= self.content,
				admin_data= admin_data,
				utils= self.utils,
				len= len,
				lang= "en",
				search_params= params,
				cats_ids= [cat.id for cat in self.database.categories.all_categories],
			)

