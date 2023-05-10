import json
from content import Content
from utils import Utils
from database.database import Database
from config import Config
from flask import Flask, render_template, url_for, request, redirect, session, send_file
from plugins.pos_calcs import POSCalculations
import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../../')


class ShippingSubRouter:
    def __init__(self, app: Flask):
        self.app: Flask = app
        self.cfg: Config = Config()
        self.database: Database = Database()
        self.utils: Utils = Utils()
        self.content: Content = Content()
        self.pos_calcs: POSCalculations= POSCalculations(self.database)

    def setup(self):
        self.assign_shipping_index()
        self.assign_delete_shipping_provider()
        self.assign_update_shipping_provider()
        self.assign_create_shipping_provider()

    def assign_update_shipping_provider(self):
        @self.app.route('/webapp/adminstration/shippingInformation/', methods=["PATCH"])
        def update_shipping_provider():
            try:
                body= dict(json.loads(request.data))
                url_params= dict(request.values)
                res= self.database.shipping_providers.update_shipping_provider(
                    sh_id= url_params['shprId'],
                    payload= body
                )

                if res:
                    return self.app.response_class(status= 200)
                return self.app.response_class(status= 500)
            except Exception as e:
                print(e)
                return self.app.response_class(status= 500)


    def assign_create_shipping_provider(self):
        @self.app.route('/webapp/adminstration/shippingInformation/', methods=["POST"])
        def create_shipping_provider():
            try:
                body= dict(json.loads(request.data))
                res= self.database.shipping_providers.create_shipping_provider(
                    name= body['name'],
                    fees= body['fees'],
                    del_days= body['del_days'],
                )

                if res:
                    return self.app.response_class(status= 201)
                return self.app.response_class(status= 500)
            except Exception as e:
                print(e)
                return self.app.response_class(status= 500)


    def assign_delete_shipping_provider(self):
        @self.app.route('/webapp/adminstration/shippingInformation/', methods=["DELETE"])
        def delete_shipping_provider():
            try:
                url_params= dict(request.values)
                shpr_id= url_params['shprid']

                res= self.database.shipping_providers.delete_shipping_provider(sh_id= shpr_id)
                if res: 
                    return self.app.response_class(status= 200)
                
                return self.app.response_class(status= 500)
            except Exception as e:
                print(e)
                return self.app.response_class(status= 500)


    def assign_shipping_index(self):
        @self.app.route('/webapp/adminstration/shippingInformation/', methods=['GET'])
        def shipping_index():
            self.database.pos.init_data()
            aid = session.get("CURRENT_ADMIN_ID", None)
            if aid is None:
                return redirect('{}/webapp/adminstration/login/'.format(self.cfg.base_url))

            admin_data = self.database.admins.get_admin_by_id(aid)
            self.database.products.load_shipping_options()
            self.database.products.refresh_all_products()
            return render_template(
                'adminstration/shipping/index.html',
                db=self.database,
                content=self.content,
                admin_data= admin_data,
                utils=self.utils,
                calcs= self.pos_calcs,
                shipping_options=self.database.products.shipping_options,
            )


