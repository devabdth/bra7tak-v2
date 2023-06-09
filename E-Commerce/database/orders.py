from config import Config
import pymongo
import time
import datetime
from bson.objectid import ObjectId
from .pos import POS
from .inventory import Inventory
from .products import Products
import sys
sys.path.insert(0, '../')


class Order:
    def __init__(
            self, id: str, address: str, address_two: str, city_code: str, products: list,
            vat: float, price: int, shipping_fees: int, status: int, uid: str,
            placed_in: str, username: str, user_email: str, user_phone: str, aid: str,
            police_number: int, gender: int, comment: str, shpr: str
    ):

        self.id = id
        self.username = username
        self.user_email = user_email
        self.user_phone = user_phone
        self.address = address
        self.address_two = address_two
        self.city_code = city_code
        self.products = products
        self.vat = vat
        self.price = price
        self.shipping_fees = shipping_fees
        self.status = status
        self.uid = uid
        self.placed_in = placed_in
        self.gender = gender
        self.aid = aid or None
        self.police_number = police_number
        self.comment = comment
        self.shpr = shpr

    def to_dict(self):
        return {
            "id": str(self.id),
            "_id": str(self.id),
            "username": self.username,
            "userEmail": self.user_email,
            "userPhone": self.user_phone,
            "address": self.address,
            "addressLineTwo": self.address_two,
            "cityCode": int(self.city_code),
            "products": self.products,
            "vat": int(self.vat),
            "price": int(self.price),
            "shippingFees": int(self.shipping_fees),
            "status": int(self.status),
            "uid": str(self.uid),
            "gender": int(self.gender),
            "placedIn": self.placed_in,
            "aid": self.aid,
            "policeNumber": self.police_number,
            "comment": self.comment,
            "shpr": self.shpr,
        }


class Orders:
    def __init__(self, client: pymongo.MongoClient, Utils):
        self.order_form = Order
        self.pos = POS()
        self.cfg: Config = Config()
        self.client: pymongo.MongoClient = client
        self.inventory = Inventory(self.client)
        self.products = Products(self.client)
        self.database = self.client["bra7tak"]
        self.orders_collection = self.database["orders"]
        self.utils = Utils()

    def create_order_from_dict(self, dict_: dict) -> Order:
        return Order(
            id=dict_['_id'],
            username=dict_['username'],
            user_email=dict_['userEmail'],
            user_phone=dict_['userPhone'],
            address=dict_['address'],
            address_two=dict_['addressLineTwo'],
            city_code=dict_['cityCode'],
            products=dict_['products'],
            gender=dict_['gender'] or 2,
            vat=dict_['vat'],
            price=dict_['price'],
            shipping_fees=dict_['shippingFees'],
            status=dict_['status'],
            uid=dict_['uid'],
            placed_in=dict_['placedIn'],
            aid=dict_['aid'],
            police_number=dict_['policeNumber'],
            comment=dict_['comment'],
            shpr=dict_['shpr']
        )

    def get_orders_by_uid(self, uid: str) -> list:
        orders = self.orders_collection.find({'uid': ObjectId(uid)})
        return [self.create_order_from_dict(dict(order)) for order in list(orders)]

    def get_all_orders_combined(self, params):
        if len(params.keys()) == 0:
            return [self.create_order_from_dict(dict(order)) for order in list(self.orders_collection.find().sort('policeNumber', -1))]

        filter_params = {}
        if params['status'] != '':
            filter_params['status'] = int(params['status'])
        if 'phone' in params.keys():
            filter_params['userPhone'] = {'$regex': params['phone']}
        if params['policeNumber'] != '':
            if int(params['policeNumber']) >= 1000000000:
                filter_params['policeNumber'] = int(params['policeNumber'])
            else:
                filter_params['policeNumber'] = {
                    '$gte': int(params['policeNumber'])}

        print(params)

        return [self.create_order_from_dict(dict(order)) for order in list(self.orders_collection.find(filter_params))]

    def get_all_orders(self, params):
        return {
            "PENDING": [self.create_order_from_dict(dict(order)) for order in list(self.orders_collection.find({
                'status': -3,
                'policeNumber': int(params['policeNumber']) if
                'policeNumber' in params.keys() and int(
                    params['policeNumber']) > 1000000000
                else
                {'$gte': int(params['policeNumber']) if 'policeNumber' in params.keys() else 0}}))
            ],
            "RETURNED": [self.create_order_from_dict(dict(order)) for order in list(self.orders_collection.find({
                'status': -2,
                'policeNumber': int(params['policeNumber']) if
                'policeNumber' in params.keys() and int(
                    params['policeNumber']) > 1000000000
                else
                {'$gte': int(params['policeNumber']) if 'policeNumber' in params.keys() else 0}}))
            ],
            "CANCELED": [self.create_order_from_dict(dict(order)) for order in list(self.orders_collection.find({
                'status': -1,
                'policeNumber': int(params['policeNumber']) if
                'policeNumber' in params.keys() and int(
                    params['policeNumber']) > 1000000000
                else
                {'$gte': int(params['policeNumber']) if 'policeNumber' in params.keys() else 0}}))
            ],
            "STOCKED": [self.create_order_from_dict(dict(order)) for order in list(self.orders_collection.find({
                'status': 0,
                'policeNumber': int(params['policeNumber']) if
                'policeNumber' in params.keys() and int(
                    params['policeNumber']) > 1000000000
                else
                {'$gte': int(params['policeNumber']) if 'policeNumber' in params.keys() else 0}}))
            ],
            "IN_DELIVERY": [self.create_order_from_dict(dict(order)) for order in list(self.orders_collection.find({
                'status': 1,
                'policeNumber': int(params['policeNumber']) if
                'policeNumber' in params.keys() and int(
                    params['policeNumber']) > 1000000000
                else
                {'$gte': int(params['policeNumber']) if 'policeNumber' in params.keys() else 0}}))
            ],
            "DELIVERED": [self.create_order_from_dict(dict(order)) for order in list(self.orders_collection.find({
                'status': 2,
                'policeNumber': int(params['policeNumber']) if
                'policeNumber' in params.keys() and int(
                    params['policeNumber']) > 1000000000
                else
                {'$gte': int(params['policeNumber']) if 'policeNumber' in params.keys() else 0}}))
            ],
        }

    def get_order_by_id(self, order_id):
        orders = self.orders_collection.find({'_id': ObjectId(order_id)})
        return self.create_order_from_dict(dict(list(orders)[0]))

    def update_order(self, oid, params, admin_id):
        try:
            order = self.orders_collection.find_one(
                {'_id': ObjectId(oid)})
            if 'status' in params.keys():
                if str(params['status']) == "2" or str(params['status']) == "1":
                    for product in order['products']:
                        self.inventory.withdraw_product(
                            product_id= product['id'],
                            color= product['color'],
                            size= product['size'],
                            quantity= 1,
                            admin_id= admin_id
                        )
                        self.inventory.record_order_withdraw(
                            order_id= oid,
                            products= [
                                {
                                    'productName': self.products.get_product_by_id(product['id']).name['en'],
                                    'product_id': product['id'], 'color': product['color'],
                                    'size': product['size'], "quantity": 1
                                } 
                            ],
                            admin_id= admin_id or '',
                            customer_name= order['username'],
                            customer_email= order['userEmail'],
                            customer_phone_number= order['userPhone'],

                        )
                if str(params['status']) == "2":
                    cart_cal = self.utils.cart_calculations(
                        order['products'], order['cityCode'])
                    self.pos.add_entry(
                        mode='input',
                        amount=cart_cal['PRODUCTS_PRICE'],
                        direction=f"Order: ({oid})",
                        recorded_by="Automated Process"
                    )

            self.orders_collection.find_one_and_update(
                {'_id': ObjectId(oid)}, {'$set': params})
            return True
        except Exception as e:
            print(e)
            return False

    def create_order(self, order: Order) -> str:
        try:
            from datetime import datetime
            if type(order) is not dict:
                order = order.to_dict()

            order["policeNumber"] = 1000000000 + \
                (self.orders_collection.count_documents({})) + 1
            order["placedIn"] = str(datetime.now())
            if "uid" in list(order.keys()) and order["uid"].strip() != '':
                order["uid"] = ObjectId(order["uid"])

            if 'id' in order.keys():
                del order['id']
            if '_id' in order.keys():
                del order['_id']

            order["status"] = -3

            order = self.orders_collection.insert_one(order)
            return order.inserted_id
        except Exception as e:
            print(e)
