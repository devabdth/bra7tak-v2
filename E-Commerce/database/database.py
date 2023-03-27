from .categories import Categories
from .collections import Collections
from .products import Products
from .users import Users
from .orders import Orders
from .admins import Admins
from .bulks import Bulks

import pymongo as pymongo
import sys
sys.path.insert(0, '../')

from config import Config

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(Config().db_url)
        self.categories: Categories = Categories()
        self.collections: Collections = Collections(client= self.client)
        self.products: Products= Products(client= self.client)
        self.users: Users= Users(client= self.client)
        self.orders: Orders= Orders(client= self.client)
        self.admins: Admins= Admins()
