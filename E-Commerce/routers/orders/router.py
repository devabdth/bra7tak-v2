import sys
sys.path.insert(0, '../')

from flask import Flask, session, request, redirect, send_file

from database.database import Database
from config import Config
from utils import Utils

class OrdersRouter:
	def __init__(self, app: Flask):
		self.app: Flask= app
		self.cfg: Config= Config()
		self.database: Database= Database()
		self.utils: Utils= Utils()


	def setup(self):
		self.assign_order_placement()
		self.assign_order_invoice()

	def assign_order_invoice(self):
		@self.app.route('/orders/invoices/')
		def order_invoice():
			params= dict(request.values)

			oid= params['oid']
			uid= session.get("CURRENT_USER_ID", None)

			if uid is None or oid is None:
				return self.app.response_class(status= 403)

			order= self.database.orders.get_order_by_id(params['oid'])
			if order is None:
				return self.app.response_class(status= 404)

			if str(uid) != str(order.uid):
				return self.app.response_class(status= 403)

			invoice= self.utils.inv_gen(order, self.utils).generate_invoice()
			return send_file(invoice, mimetype="application/pdf", as_attachment= True, attachment_filename="Order-{}.pdf".format(params['oid']))



	def assign_order_placement(self):
		@self.app.route('/orders/placement/')
		def order_placement():
			uid= session.get('CURRENT_URER_ID', None)