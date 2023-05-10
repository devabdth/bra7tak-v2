from uuid import uuid4
import secrets
from layout.layout import Layout
from layout.ad_banners import AdBanner
import json
import os
import sys
sys.path.insert(0, '../')


class Category:
    def __init__(self, name: dict, bio: dict, id: str, products: list, subcats: list):
        self.name = name
        self.bio = bio
        self.id = id
        self.products = products
        self.subcats = subcats

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "bio": self.bio or {},
            "id": self.id,
            "products": self.products or [],
            "subcats": self.subcats or [],
        }


class Categories:
    def __init__(self):
        self.layout: Layout = Layout()
        self.load()

    def load(self):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../jsons/categories.json')), 'r', encoding="cp866") as f:
            self.categories_file_data = dict(json.load(f))
        self.all_categories: list = [
            Category(
                id=x['id'],
                name=x['name'],
                bio=x['bio'],
                products=x['products'],
                subcats=[
                    Category(
                        name=y['name'],
                        id=y['id'],
                        products=y['products'],
                        bio=y['bio'],
                        subcats=None,
                    )
                    for y in x['subcats']
                ]
            )
            for x in self.categories_file_data.values()
        ]

        self.all_categories_dicts: list = []
        for cat in self.all_categories:
            subcats_dicts = []
            for subcat in cat.subcats:
                subcat_dict = subcat.to_dict()
                del subcat_dict['subcats']
                subcats_dicts.append(subcat_dict)
            cat.subcats = subcats_dicts

            self.all_categories_dicts.append(cat.to_dict())

    def get_category_by_id(self, id):
        for cat in self.all_categories:
            if str(id) == str(cat.id):
                return cat

    def get_sub_category_by_id(self, cid, scid):
        for cat in self.all_categories:
            if str(cid) == str(cat.id):
                for scat in cat.subcats:
                    if str(scid) == str(scat["id"]):
                        return scat

    def delete_category(self, cid):
        try:
            for category in self.all_categories_dicts:
                if category["id"] == cid:
                    self.all_categories_dicts.remove(category)

            with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../jsons/categories.json')), 'w', encoding="utf-8") as f:
                dict_ = {cat['id']: cat for cat in self.all_categories_dicts}
                json.dump(dict_, f)
                f.close()

            return True
        except Exception as e:
            print(e)
            return False

    def update_category(self, category: dict, icon, cover) -> bool:
        try:
            for cat_dict in self.all_categories_dicts:
                if cat_dict['id'] == category['id']:
                    cat_dict['name'] = category['name']
                    cat_dict['bio'] = category['bio']
                    cat_dict['subcats'] = [
                        {
                            "name": {
                                "en": subcat['name']['en'],
                                "ar": subcat['name']['ar'],
                            },
                            "bio": None,
                            "id": "{}".format(category['subcats'].index(subcat)),
                            "products": [],
                            "subcats": None
                        } for subcat in category['subcats']
                    ]

                    del self.all_categories_dicts[self.all_categories_dicts.index(
                        cat_dict)]
                    self.all_categories_dicts.append(cat_dict)
            with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../jsons/categories.json')), 'w', encoding="utf-8") as f:
                dict_ = {cat['id']: cat for cat in self.all_categories_dicts}
                json.dump(dict_, f)
                f.close()

            if icon != None:
                if not os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), '../routers/assets/categories/icons/'))):
                    os.mkdir(os.path.abspath(os.path.join(os.path.dirname(
                        __file__), '../routers/assets/categories/icons/')))
                icon.save(os.path.abspath(os.path.join(os.path.dirname(
                    __file__), '../routers/assets/categories/icons/'+category['id'] + '.' + icon.filename.split('.')[-1])))
            if cover != None:
                if not os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), '../routers/assets/categories/covers/'))):
                    os.mkdir(os.path.abspath(os.path.join(os.path.dirname(
                        __file__), '../routers/assets/categories/covers/')))
                cover.save(os.path.abspath(os.path.join(os.path.dirname(
                    __file__), '../routers/assets/categories/covers/'+category['id'] + '.' + cover.filename.split('.')[-1])))

            return True
        except Exception as e:
            print(e)
            return False

    def create_category(self, category: dict, icon, cover) -> bool:
        try:
            category['id'] = str(secrets.token_hex(12))
            print(category['id'])
            category['products'] = []
            category['subcats'] = [
                {
                    "name": {
                        "en": subcat['name']['en'],
                        "ar": subcat['name']['ar'],
                    },
                    "bio": None,
                    "id": "{}".format(category['subcats'].index(subcat)),
                    "products": [],
                    "subcats": None
                } for subcat in category['subcats']
            ]

            self.all_categories_dicts.append(category)
            with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../jsons/categories.json')), 'w', encoding="utf-8") as f:
                dict_ = {cat['id']: cat for cat in self.all_categories_dicts}
                json.dump(dict_, f)
                f.close()

            if icon != None:
                if not os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), '../routers/assets/categories/icons/'))):
                    os.mkdir(os.path.abspath(os.path.join(os.path.dirname(
                        __file__), '../routers/assets/categories/icons/')))
                icon.save(os.path.abspath(os.path.join(os.path.dirname(
                    __file__), '../routers/assets/categories/icons/'+category['id'] + '.' + icon.filename.split('.')[-1])))
            if cover != None:
                if not os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), '../routers/assets/categories/covers/'))):
                    os.mkdir(os.path.abspath(os.path.join(os.path.dirname(
                        __file__), '../routers/assets/categories/covers/')))
                cover.save(os.path.abspath(os.path.join(os.path.dirname(
                    __file__), '../routers/assets/categories/covers/'+category['id'] + '.' + cover.filename.split('.')[-1])))

            return True
        except Exception as e:
            print(e)
            return False
