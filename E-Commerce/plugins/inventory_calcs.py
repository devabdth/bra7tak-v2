from pandas import DataFrame
from sys import path
path.insert(0, '../')


class InventoryCalculations:
    from database.products import Product

    @classmethod
    def get_inventory_scope_boundries(cls):
        from os.path import abspath, join, dirname
        from json import loads
        with open(abspath(join(dirname(__file__), '../jsons/metaInfo.json'))) as f:
            meta_info = dict(loads(f.read()))
            return meta_info['inventoryBoundries']

    @staticmethod
    def product_status(product: Product):
        boundries: dict = InventoryCalculations.get_inventory_scope_boundries()

        red_scope = []
        yellow_scope = []
        green_scope = []

        for k, v in product.inventory.items():
            for ik, iv in v.items():
                if iv <= boundries['redScope']:
                    red_scope.append(
                        {"color": k, "size": ik, "currentQuantity": iv})

                if boundries['redScope'] < iv <= boundries['yellowScope']:
                    yellow_scope.append(
                        {"color": k, "size": ik, "currentQuantity": iv})

                if boundries['greenScope'] <= iv:
                    green_scope.append(
                        {"color": k, "size": ik, "currentQuantity": iv})

        return {
            'productId': product.id,
            'productName': product.name['en'],
            'redScope': red_scope,
            'yellowScope': yellow_scope,
            'greenScope': green_scope,
        }

    @staticmethod
    def multiple_products_status(products: list):
        return [InventoryCalculations.product_status(prod) for prod in products]

    @staticmethod
    def multiple_products_status_df(products: list):
        boundries= [InventoryCalculations.product_status(prod) for prod in products]
        return DataFrame(boundries, columns=['productId', 'productName', 'redScope', 'yellowScope', 'greenScope'])


    @staticmethod
    def calculate_total_pieces(inventory: dict):
        stock= 0
        for color in inventory.values():
            for size in color.values():
                stock+= size

        return stock