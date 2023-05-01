import pymongo
from bson import ObjectId
import secrets
from .pos import POS
from .products import Product, Products
from plugins.inventory_calcs import InventoryCalculations as InvCalc
from json import loads, dump
from pandas import DataFrame
from os.path import abspath, join, dirname
from datetime import datetime
from sys import path
path.insert(0, '../')


class Inventory:
    def __init__(self, client: pymongo.MongoClient):
        self.pos = POS()
        self.calc = InvCalc
        self.client: pymongo.MongoClient = client
        self.products = Products(self.client)
        self.inventory_log_path = abspath(
            join(dirname(__file__), '../jsons/inventoryLog.json'))
        self.inventory_requests_path = abspath(
            join(dirname(__file__), '../jsons/inventoryRequests.json'))

    def read_log_file(self):
        with open(self.inventory_log_path, 'r') as f:
            return dict(loads(f.read()))

    def read_requests_file(self):
        with open(self.inventory_requests_path, 'r') as f:
            return dict(loads(f.read()))

    def record_deposit(self, **payload):
        '''
            Payload Schema:
            {
                product: Product Object,
                color: "Color",
                size: "Size",
                quantity: Quantity | int,
                admin_id: "Admin Id",

            }
        '''
        snippet = {
            "productName": payload['product'].name['en'],
            "productStockPrice": payload['product'].pricing['stockPrice'],
            "quantity": payload['quantity'],
            "placedIn": str(datetime.now()),
            "depositedColor": payload['color'],
            "depositedSize": payload['size'],
            "deposittedBy": payload['admin_id']
        }

        log_data = self.read_log_file()
        with open(self.inventory_log_path, 'w') as f:
            log_data['deposits'].append(snippet)
            dump(log_data, f)

    def record_order_withdraw(self, **payload):
        '''
            Payload Schema:
            {
                "products": [{
                    "productName": "This is a product",
                    "product_id": "Product Id",
                    "color": "Desired Color",
                    "size": "Desired Size",
                    "quantity": Quantity | int,
                }],
                "order_id": "Order Id",
            }
        '''
        snippet = {
            "products": [
                {
                    "productName": product['productName'],
                    "product_id": product['product_id'],
                    "color": product['color'],
                    "size": product['size'],
                    "quantity": product['quantity']
                } for product in payload['products']
            ],
            "placedIn": str(datetime.now()),
            "order_id": payload['order_id'],
        }

        log_data = self.read_log_file()
        with open(self.inventory_log_path, 'w') as f:
            log_data['orderWithdraws'].append(snippet)
            dump(log_data, f)

    def record_deal_withdraw(self, **payload):
        '''
            Payload Schema:
            {
                "products": [{
                    "productName": "This is a product",
                    "product_id": "Product Id",
                    "color": "Desired Color",
                    "size": "Desired Size",
                    "quantity": Quantity | int,
                }],
                "admin_id": "Admin Id",
                "customer_name": "Customer Name",
                "customer_email": "Custoemr Email",
                "customer_phone_number": "Customer Phone Number",
            }
        '''

        snippet = {
            "products": [
                {
                    "productName": product['productName'],
                    "product_id": product['product_id'],
                    "color": product['color'],
                    "size": product['size'],
                    "quantity": product['quantity']
                } for product in payload['products']
            ],
            "admin_id": payload['admin_id'],
            "customer_name": payload['customer_name'],
            "customer_email": payload['customer_email'],
            "customer_phone_number": payload['customer_phone_number'],
            "placedIn": str(datetime.now()),
        }

        log_data = self.read_log_file()
        with open(self.inventory_log_path, 'w') as f:
            log_data['dealsWithdraws'].append(snippet)
            dump(log_data, f)

    def deposit_product(self, admin_id: str, product_id: str, color: str, size: str, quantity: int) -> bool:
        try:
            product = self.products.get_product_by_id(product_id)
            if color not in product.inventory.keys():
                product.inventory[color] = {}

            if size not in product.inventory[color].keys():
                product.inventory[color][size] = 0

            product.inventory[color][size] += quantity

            res = self.products.update_product(product.to_dict(), files={})
            if not res:
                raise Exception('Failed to update product data!')

            res = self.record_deposit(
                product=product,
                color=color,
                size=size,
                quantity=quantity,
                admin_id=admin_id,
            )

            res = self.pos.add_entry(
                'output',
                'Stock',
                product.pricing['stockPrice'] * quantity,
                admin_id)

            return True
        except Exception as e:
            print(e)
            return False

    def handle_request_interactions(self, mode: str, **kwargs):
        requests_data = self.read_requests_file()
        if mode == "create":
            if "products" not in kwargs.keys():
                raise Exception('Request body is missing.')

            rid = str(secrets.token_hex(12))
            snippet: dict = {
                "placedIn": str(datetime.now()),
                "products": kwargs["products"],
                "rid": rid,
            }

            requests_data["activeDepositRequests" if kwargs['rmode']
                          == "deposit" else "activeWithdrawRequests"][rid] = snippet
        elif mode == "archive":
            if not kwargs['rid'] in requests_data["activeDepositRequests" if kwargs['rmode']
                                                  == "deposit" else "activeWithdrawRequests"].keys():
                raise KeyError('Request not exists.')

            request = requests_data["activeDepositRequests" if kwargs['rmode']
                                    == "deposit" else "activeWithdrawRequests"][kwargs['rid']]

            del requests_data["activeDepositRequests" if kwargs['rmode']
                              == "deposit" else "activeWithdrawRequests"][kwargs['rid']]

            requests_data["archivedDepositRequests" if kwargs['rmode']
                          == "deposit" else "archivedWithdrawRequests"][kwargs['rid']] = request

        with open(self.inventory_requests_path, 'w') as f:
            dump(requests_data, f)

    def scopes_report(self):
        return InvCalc.multiple_products_status(self.products.all_products)
