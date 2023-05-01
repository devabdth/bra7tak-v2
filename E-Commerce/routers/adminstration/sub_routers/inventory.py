import json
from content import Content
from utils import Utils
from database.database import Database
from config import Config
from flask import Flask, render_template, url_for, request, redirect, session, send_file
import sys
from inventory_reports.app import InventoryReports
sys.path.insert(0, '../')
sys.path.insert(0, '../../')


class InventorySubRouter:
    def __init__(self, app: Flask):
        self.app: Flask = app
        self.cfg: Config = Config()
        self.database: Database = Database()
        self.utils: Utils = Utils()
        self.content: Content = Content()

    def setup(self):
        self.assign_inventory_index()
        self.assign_deposit_index()
        self.assign_debosit_requests_submission()
        self.assign_withdraw_requests_submission()
        self.assign_inventory_report()

    def assign_inventory_report(self):
        @self.app.route('/webapp/adminstration/inventory/report/<product>/')
        def inventory_report(product):
            import os
            if product == 'generalReport':
                report = InventoryReports.generate_multiple_products_report(
                    self.database.products.all_products
                )
            else:
                report = InventoryReports.generate_single_product_report(
                    self.database.products.get_product_by_id(product)
                )

            if report is None:
                return self.app.response_class(status=404)

            return send_file(
                report, as_attachment=True,
                mimetype="application/vnd.ms-excel", download_name="output.xlsx"

            )

    def assign_deposit_index(self):
        @self.app.route('/webapp/adminstration/inventory/deposit/', methods=['PATCH'])
        def deposit_index():
            try:
                aid = session.get("CURRENT_ADMIN_ID", None)
                body = dict(json.loads(request.data))
                res = self.database.inventory.deposit_product(
                    admin_id=aid,
                    product_id=body['productId'],
                    color=body['color'].replace(' ', '').lower(),
                    size=body['size'].replace(' ', '').lower(),
                    quantity=int(body['quantity'])
                )
                if res:
                    return self.app.response_class(status=200)
                return self.app.response_class(status=500)
            except Exception as e:
                print(e)
                return self.app.response_class(status=500)

    def assign_debosit_requests_submission(self):
        @self.app.route('/webapp/adminstration/inventory/requests/submission/deposit/<rid>/', methods=["PATCH"])
        def debosit_requests_submission(rid):
            try:
                res = self.database.inventory.handle_request_interactions(
                    mode='archive', rid=rid, rmode='deposit')
                return self.app.response_class(status=200)
            except Exception as e:
                print(e)
                return self.app.response_class(status=500)

    def assign_withdraw_requests_submission(self):
        @self.app.route('/webapp/adminstration/inventory/requests/submission/withdraw/<rid>/', methods=["PATCH"])
        def withdraw_requests_submission(rid):
            try:
                res = self.database.inventory.handle_request_interactions(
                    mode='archive', rid=rid, rmode='withdraw')
                return self.app.response_class(status=200)
            except Exception as e:
                print(e)
                return self.app.response_class(status=500)

    def assign_inventory_index(self):
        @self.app.route('/webapp/adminstration/inventory/', methods=['GET'])
        def inventory_index():
            aid = session.get("CURRENT_ADMIN_ID", None)
            if aid is None:
                return redirect('{}/webapp/adminstration/login/'.format(self.cfg.base_url))

            admin_data = self.database.admins.get_admin_by_id(aid)

            self.database.products.refresh_all_products()
            return render_template(
                'adminstration/inventory/index.html',
                db=self.database,
                content=self.content,
                sum=sum,
                requests=self.database.inventory.read_requests_file(),
                calculate_stock=self.database.inventory.calc.calculate_total_pieces,
                utils=self.utils,
                inventory_scopes=self.database.inventory.scopes_report(),
            )
