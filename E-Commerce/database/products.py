from config import Config
import os
import pymongo
import time
import datetime
from bson.objectid import ObjectId


import sys
sys.path.insert(0, '../')


class Product:
    def __init__(
        self, id: str, name: dict, bio: dict, pricing: float, assets: list,
        category: int, sub_category: int, avg_del_days: dict,
        code: str, specs: dict, vat: float = 0.14, shipping_fees: dict = {}, colors: list = [], sizes: list = []
    ):
        self.id = id
        self.name = name
        self.bio = bio
        self.assets = assets
        self.category = category
        self.sub_category = sub_category
        self.code = code
        self.pricing = pricing
        self.avg_del_days = avg_del_days
        self.specs = specs
        self.vat = vat
        self.shipping_fees = shipping_fees
        self.colors = colors
        self.sizes = sizes

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "bio": self.bio,
            "assets": self.assets,
            "category": self.category,
            "subCategory": self.sub_category,
            "code": self.code,
            "pricing": self.pricing,
            "avgDelDays": self.avg_del_days,
            "specs": self.specs,
            "vat": self.vat,
            "shippingFees": self.shipping_fees,
            "colors": self.colors or "",
            "sizes": self.sizes or "",
        }


class Products:
    def __init__(self, client: pymongo.MongoClient):
        self.cfg: Config = Config()
        self.client: pymongo.MongoClient = client
        self.database = self.client["bra7tak"]
        self.products_collection = self.database["products"]
        self.all_products = []
        self.refresh_all_products()

        self.load_shipping_options()

    def load_shipping_options(self):
        import csv
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../csvs/shippingOptions.csv')), newline='') as f:
            reader = csv.reader(f)
            shipping_options = {}

            for line in reader:
                if not line[0] == 'cityId':
                    shipping_options[line[0]] = {
                        'durations': line[1],
                        'fees': line[2],
                    }

            self.shipping_options = shipping_options

    def update_shipping_options(self, new_shipping_options):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../csvs/shippingOptions.csv')), newline='', mode='w') as f:
            f.write('cityId,duration,fee\n')
            for key in new_shipping_options:
                print(new_shipping_options[key])
                f.write('{},{},{}\n'.format(
                    key,
                    new_shipping_options[key]['durations'],
                    new_shipping_options[key]['fees'],
                ))
            self.load_shipping_options()
            return True

    def create_product_from_dict(self, dict_) -> Product:
        return Product(
            id=dict_['_id'],
            name=dict_['name'],
            bio=dict_['bio'],
            assets=dict_['assets'],
            category=dict_['category'],
            sub_category=int(dict_['subCategory']),
            code=dict_['code'],
            pricing=dict_['pricing'],
            avg_del_days=dict_['avgDelDays'],
            specs=dict_['specs'],
            vat=dict_['vat'],
            shipping_fees=dict_['shippingFees'],
            colors=dict_['colors'],
            sizes=dict_['sizes']
        )

    def refresh_all_products(self):
        self.all_products = [self.create_product_from_dict(
            product) for product in list(self.products_collection.find())]

    def get_product_by_id(self, product_id) -> Product:
        products = self.products_collection.find({'_id': ObjectId(product_id)})
        return self.create_product_from_dict(dict(list(products)[0]))

    def get_all_products(self):
        self.refresh_all_products()
        return self.all_products

    def get_multiple_products_by_id(self, ids: list):
        products = self.products_collection.find({'_id': {'$in': [ObjectId(
            _id) if type(_id) is str else ObjectId(_id['id']) for _id in ids]}})
        return [self.create_product_from_dict(dict(prod)) for prod in list(products)]

    def get_all_products_by_category(self, cat_id: int):
        products = self.products_collection.find({
            'category': cat_id,
        })
        return [self.create_product_from_dict(dict(prod)) for prod in list(products)]

    def get_products_by_filterization(self, search_params):
        if len(search_params.keys()) == 0:
            self.refresh_all_products()
            return self.all_products

        products = self.all_products

        if 'token' in search_params.keys():
            products = [prod if (search_params['token'].replace('%20', ' ') in prod.name['en'].lower(
            ) or search_params['token'].replace('%20', ' ') in prod.name['ar'].lower()) else None for prod in products]
        while None in products:
            products.remove(None)

        if 'cats' in search_params.keys():
            products = [prod if (str(prod.category) in list(
                search_params['cats'].split(','))) else None for prod in products]
        while None in products:
            products.remove(None)

        if 'minPrice' in search_params.keys():
            products = [prod if (prod.pricing['currentPrice'] >= int(
                search_params['minPrice'])) else None for prod in products]
        while None in products:
            products.remove(None)

        if 'maxPrice' in search_params.keys():
            products = [prod if (prod.pricing['currentPrice'] <= int(
                search_params['maxPrice'])) else None for prod in products]
        while None in products:
            products.remove(None)

        return list(products)

    def get_products_similer_to(self, similers: list):
        return self.all_products

    def update_product(self, product_: dict, files) -> bool:
        try:
            product: Product = self.get_product_by_id(product_["id"])
            for asset in product.assets:
                if asset not in product_["assets"]:
                    path_ = os.path.abspath(os.path.join(os.path.dirname(
                        __file__), '../routers/assets/products/{}-{}'.format(product_["id"], asset)))
                    if asset in product_["assets"]:
                        product_["assets"].remove(asset)
                    if os.path.exists(path_):
                        os.remove(path_)

            newAssetsNames = []
            for file_ in files.values():
                newAssetsNames.append("{}.{}".format(
                    list(files.values()).index(file_), file_.filename.split('.')[-1]))
                file_.save(os.path.abspath(os.path.join(os.path.dirname(__file__), '../routers/assets/products/{}-{}.{}'.format(
                    product.id, list(files.values()).index(file_), file_.filename.split('.')[-1]))))
                product_["assets"].remove(file_.filename)

            product.code = product_["code"]
            product.name = product_["name"]
            product.bio = product_["bio"]
            product.specs = product_["specs"]
            product.pricing = product_["pricing"]
            product.vat = product_["vat"]
            assets_ = list(set(list(newAssetsNames + product_["assets"])))
            product.assets = ["{}.{}".format(assets_.index(
                asset_name), asset_name.split('.')[-1]) for asset_name in assets_]
            product.avg_del_days = product_["avgDelDays"]
            product.shipping_fees = product_["shippingFees"]
            product.category = product_["category"]
            product.sub_category = int(product_["subCategory"])
            product.colors = product_['colors']
            product.sizes = product_['sizes']
            self.products_collection.find_one_and_update(
                {'_id': ObjectId(product.id)}, {'$set': product.to_dict()})
            self.refresh_all_products()

            return True
        except Exception as e:
            print(e)
            return False

    def create_product(self, product_: dict, files) -> bool:
        try:

            product: Product = Product(
                id="fsdfsd",
                code=product_["code"],
                name=product_["name"],
                bio=product_["bio"],
                specs=product_["specs"],
                pricing=product_["pricing"],
                vat=product_["vat"],
                assets=["{}.{}".format(list(product_["assets"]).index(asset), list(product_["assets"])[
                        product_["assets"].index(asset)].split('.')[-1]) for asset in product_["assets"]],
                avg_del_days=product_["avgDelDays"],
                shipping_fees=product_["shippingFees"],
                category=product_["category"],
                sub_category=int(product_["subCategory"]),
                colors=product_['colors'],
                sizes=product_['sizes']
            )
            product = self.products_collection.insert_one(product.to_dict())
            self.refresh_all_products()
            if product.inserted_id is not None:
                for file_ in files.values():
                    file_.save(os.path.abspath(os.path.join(os.path.dirname(__file__), '../routers/assets/products/{}-{}.{}'.format(
                        product.inserted_id, list(files.values()).index(file_), file_.filename.split('.')[-1]))))

            return product.inserted_id != None
        except Exception as e:
            print(e)
            return False

    def delete_product(self, prodId):
        try:
            self.products_collection.delete_one({'_id': ObjectId(prodId)})
            return True
        except Exception as e:
            print(e)
            return False
            raise e
