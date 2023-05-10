from database.database import Database
from utils import Utils
from config import Config
from content import Content
from flask import Flask, render_template, url_for, session, request
import sys
sys.path.insert(0, '../')


class CheckoutRouter:
    def __init__(self, app: Flask):
        self.app = app
        self.cfg: Config = Config()
        self.content: Content = Content()
        self.utils: Utils = Utils()
        self.database: Database = Database()

    def setup(self):
        self.assign_checkout_form_router()
        self.assign_place_order()

    def assign_place_order(self):
        @self.app.route('/checkout/', methods=["POST"])
        def place_order():
            self.database.products.load_shipping_options()
            import json

            params = dict(request.values)
            uid = session.get('CURRENT_USER_ID', None)
            if uid is not None:
                user_data = self.database.users.get_user_by_id(uid)
            else:
                params = dict(request.values)
                cart = []
                for prod in params['prods'].split('|'):
                    if prod != '':
                        cart.append({'id': list(prod.split(','))[0], 'size': list(prod.split(','))[1] if len(prod.split(
                            ',')) > 2 else None, 'color': list(prod.split(','))[2] if len(prod.split(',')) > 2 else None})

            body = dict(json.loads(request.data))
            if not 'order' in body.keys():
                return self.app.response_class(status=500)

            order = body['order']
            cart_calc = self.utils.cart_calculations(
                user_data.cart if uid != None else cart)
            order_: self.database.orders.order_form = self.database.orders.order_form(
                id="",
                aid=None,
                username=order['username'],
                user_email=order['email'],
                user_phone=order['phone'],
                address=order['addressLineOne'],
                address_two=order['addressLineTwo'],
                city_code=order['city'],
                products=user_data.cart if uid != None else cart,
                vat=cart_calc['TOTAL_VAT'],
                price=cart_calc['TOTAL_PRICE'],
                shipping_fees=self.database.products.shipping_options[(str(user_data.city_code))]['fees'],
                status=0,
                gender=order['gender'],
                comment=order['comments'],
                uid=uid if uid is not None else "",
                placed_in="",
                police_number=0,
            )
            if uid is not None:
                self.database.users.update_user_data(
                    uid=uid, user_data={'cart': []})

            try:
                order_id = self.database.orders.create_order(order_)
                self.utils.inv_gen(utils=self.utils, order=self.database.orders.get_order_by_id(
                    order_id)).generate_invoice()
                return self.app.response_class(status=201)
            except Exception as e:
                print(e)
                return self.app.response_class(status=500)

    def assign_checkout_form_router(self):
        @self.app.route('/checkout/', methods=["GET"])
        def checkout_form():
            lang = session.get("LANG", "en")
            uid = session.get("CURRENT_USER_ID", None)
            if lang == 'en':
                primary_font_family = 'Raleway'
                second_font_family = 'Poppins'
            elif lang == 'ar':
                primary_font_family = 'Cairo'
                second_font_family = 'Cairo'
            if not uid is None:
                user_data = self.database.users.get_user_by_id(uid)
                cart = user_data.cart
                return render_template(
                    'checkout/index.html',
                    uid=uid,
                    user_data=user_data,
                    lang=lang,
                    cfg=self.cfg,
                    content=self.content,
                    primary_font_family=primary_font_family,
                    second_font_family=second_font_family,
                    len=len,
                    database=self.database,
                    utils=self.utils,
                    cart=cart
                )
            params = dict(request.values)
            cart = []
            for prod in params['prods'].split('|'):
                if prod == '':
                    break
                cart.append({'id': list(prod.split(','))[0], 'size': list(prod.split(','))[1] if len(prod.split(
                    ',')) > 2 else None, 'color': list(prod.split(','))[2] if len(prod.split(',')) > 2 else None})
            return render_template(
                'checkout/index.html',
                lang=lang,
                cfg=self.cfg,
                content=self.content,
                primary_font_family=primary_font_family,
                second_font_family=second_font_family,
                len=len,
                database=self.database,
                utils=self.utils,
                cart=cart
            )
