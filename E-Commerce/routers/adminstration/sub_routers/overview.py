import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../../')


from flask import Flask, render_template, url_for, request, redirect, session, send_file

from config import Config
from database.database import Database
from utils import Utils
from content import Content
from plugins.pos_calcs import POSCalculations
from plugins.inventory_calcs import InventoryCalculations


import json
class OverviewSubRouter:
	def __init__(self, app: Flask):
		self.app: Flask= app
		self.cfg: Config= Config()
		self.database: Database= Database()
		self.utils: Utils= Utils()
		self.content: Content= Content()
		self.pos_calcs: POSCalculations= POSCalculations(self.database)


	def setup(self):
		self.assign_overview_index()

	def assign_overview_index(self):
		@self.app.route('/webapp/adminstration/overview/', methods=["GET"])
		def overview_index():
			params= dict(request.values)

			aid= session.get("CURRENT_ADMIN_ID", None)
			if aid is None:
				return redirect('{}/webapp/adminstration/login/'.format(self.cfg.base_url))

			admin_data= self.database.admins.get_admin_by_id(aid)
			return render_template(
				'adminstration/overview/index.html',
				cfg= self.cfg,
				database= self.database,
				content= self.content,
				admin_data= admin_data,
				utils= self.utils,
				len= len,
				lang= "en",
				search_params= params,
				pos_report= self.pos_calcs.report(),
				inventory_calcs= InventoryCalculations
			)
