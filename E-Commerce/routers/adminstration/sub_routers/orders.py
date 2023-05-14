from json import dumps as jsonParser
import json
from content import Content
from utils import Utils
from database.database import Database
from config import Config
from flask import Flask, render_template, url_for, request, redirect, session, send_file
import sys
import os
from io import BytesIO
from pypdf import PdfMerger
sys.path.insert(0, '../')
sys.path.insert(0, '../../')


class OrdersSubRouter:
    def __init__(self, app: Flask):
        self.app: Flask = app
        self.cfg: Config = Config()
        self.database: Database = Database()
        self.utils: Utils = Utils()
        self.content: Content = Content()

    def setup(self):
        self.assign_orders_index()
        self.assign_orders_post()
        self.assign_order_qr_code()
        self.assign_order_status_change()
        self.assign_order_data_update()
        self.assign_order_invoice()
        self.assign_order_multiple_invoice()
        self.assign_order_multiple_stocking()

    def assign_order_multiple_stocking(self,):
        @self.app.route('/webapp/adminstration/orders/multipeStock/', methods=["PATCH"])
        def order_multiple_stocking():
            try:
                body= dict(json.loads(request.data))
                orders= body['orders']
                for order in orders:
                    self.database.orders.update_order(
                            order, {'status': 0})
                    
                return self.app.response_class(status= 200)
            except Exception as e:
                return self.app.response_class(status= 500)




    def setup_products_tr_display(self, order_products, products):
        final_display = ''
        for order_prod in order_products:
            for prod in products:
                if str(prod.id) == str(order_prod['id']):
                    final_display += "<p>{} <span style=\"font-size: 0.75em\">({})</span> - <span style=\"font-size: 0.75em\">({})</span></p>".format(
                        prod.name['en'],
                        order_prod['size'] if 'size' in order_prod.keys(
                        ) and order_prod['size'] != "undefined" else 'No Size Mentioned',
                        order_prod['color'] if 'color' in order_prod.keys(
                        ) and order_prod['size'] != "undefined" else 'No color Mentioned',
                    )

        return final_display

    def assign_order_invoice(self):
        @self.app.route('/webapp/adminstration/orders/invoices/')
        def admin_order_invoice():
            params = dict(request.values)

            oid = params['oid']
            aid = session.get("CURRENT_ADMIN_ID", None)

            if aid is None or oid is None:
                return self.app.response_class(status=403)

            return send_file(os.path.abspath(os.path.join(os.path.join(os.path.dirname(
                __file__), '../../assets/invoices'), '{}.pdf'.format(oid))), mimetype="application/pdf")

    def assign_order_multiple_invoice(self):
        @self.app.route('/webapp/adminstration/orders/invoices/multiple/', methods=["PATCH"])
        def admin_order_multiple_invoices():
            try:
                orders = dict(json.loads(request.data))['orders']
                orders = [os.path.abspath(os.path.join(os.path.join(os.path.dirname(
                    __file__), '../../assets/invoices'), '{}.pdf'.format(order))) for order in orders]
                print(orders)
                merger = PdfMerger()
                for order in orders:
                    merger.append(order)

                buffer = BytesIO()
                merger.write(buffer)
                buffer.seek(0)
                return send_file(buffer, mimetype="application/pdf")
            except Exception as e:
                print(e)
                return self.app.response_class(status=500)

    def assign_orders_post(self):
        @self.app.route('/webapp/adminstration/orders/', methods=["POST"])
        def orders_post():
            aid = session.get("CURRENT_ADMIN_ID", None)
            if aid is None:
                return redirect('{}/webapp/adminstration/login/'.format(self.cfg.base_url))

            admin_data = self.database.admins.get_admin_by_id(aid)

            body = dict(json.loads(request.data))
            order: self.database.orders.order_form = self.database.orders.order_form(
                id=None,
                username=body['information']['customerName'],
                user_email=body['information']['customerEmail'],
                user_phone=body['information']['customerPhone'],
                uid='',
                gender=int(body['information']['gender']),
                address=body['information']['customerAddressLineOne'],
                address_two=body['information']['customerAddressLineTwo'],
                city_code=int(body['information']['customerCity']),
                products=body['products'],
                status=body['status'],
                price=body['fees']['price'],
                vat=body['fees']['vat'],
                shipping_fees=body['fees']['shippingFees'],
                placed_in=None,
                aid=admin_data['aid'],
                comment=body['information']['comments'],
                police_number=0,
                shpr= ''
            )

            try:
                oid = self.database.orders.create_order(order)
                self.utils.inv_gen(utils=self.utils, order=self.database.orders.get_order_by_id(
                    oid)).generate_invoice()

                print(oid)
                if oid is not None:
                    return self.app.response_class(status=201)

                return self.app.response_class(status=500)
            except Exception as e:
                print(e)
                return self.app.response_class(status=500)

    def assign_orders_index(self):
        @self.app.route('/webapp/adminstration/orders/', methods=["GET"])
        def orders_index():
            params = dict(request.values)

            aid = session.get("CURRENT_ADMIN_ID", None)
            if aid is None:
                return redirect('{}/webapp/adminstration/login/'.format(self.cfg.base_url))

            admin_data = self.database.admins.get_admin_by_id(aid)
            orders = self.database.orders.get_all_orders_combined(params)
            products = self.database.products.get_all_products()
            self.database.products.load_shipping_data()
            return render_template(
                'adminstration/orders/index.html',
                cfg=self.cfg,
                orders=orders,
                products=products,
                all_products=[prod.to_dict() for prod in products],
                database=self.database,
                content=self.content,
                admin_data=admin_data,
                utils=self.utils,
                len=len,
                lang="en",
                search_params=params,
                cats_ids=[
                    cat.id for cat in self.database.categories.all_categories],
                dumps=json.dumps,
                tr_display=self.setup_products_tr_display,
            )

    def assign_order_qr_code(self):
        @self.app.route('/webapp/adminstration/orders/qr/<oid>')
        def qr_generation(oid):
            if session.get('CURRENT_ADMIN_ID', 'sdsdcsdf') is not None:
                from qrcode import make
                from io import BytesIO
                file_ = make(oid)
                buf = BytesIO()
                file_.save(buf)
                buf.seek(0)
                return send_file(buf, mimetype="image/jpeg")

            return self.app.response_class(status=403)

    def assign_order_status_change(self):
        @self.app.route('/webapp/adminstration/orders/', methods=["PATCH"])
        def order_status_change():
            try:
                params = dict(request.values)
                if ('oid' in params.keys() and 'status' in params.keys()):
                    res = self.database.orders.update_order(
                        params['oid'], {'status': int(params['status'])})
                    if res:
                        return self.app.response_class(status=200)

                return self.app.response_class(status=500)
            except Exception as e:
                print(e)
                return self.app.response_class(status=500)

    def assign_order_data_update(self):
        @self.app.route('/webapp/adminstration/orders/data/', methods=["PATCH"])
        def order_order_data_update():
            try:
                order = dict(json.loads(request.data))
                id_ = order['_id']
                del order['_id']
                del order['id']
                if order is not None:
                    res = self.database.orders.update_order(
                        id_, order)
                    if res:
                        return self.app.response_class(status=200)

                return self.app.response_class(status=500)
            except Exception as e:
                print(e)
                return self.app.response_class(status=500)
