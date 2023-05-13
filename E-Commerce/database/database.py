from config import Config
from .categories import Categories
from .collections import Collections
from .products import Products
from .users import Users
from .orders import Orders
from .admins import Admins
from .bulks import Bulks
from .inventory import Inventory
from .pos import POS
from .shipping_providers import ShippingProviders
from .hr import HR

from utils import Utils
import pymongo as pymongo
import sys
sys.path.insert(0, '../')


class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(Config().db_url)
        self.categories: Categories = Categories()
        self.collections: Collections = Collections(client=self.client)
        self.products: Products = Products(client=self.client)
        self.users: Users = Users(client=self.client)
        self.orders: Orders = Orders(client=self.client, Utils= Utils)
        self.admins: Admins = Admins()
        self.inventory: Inventory = Inventory(client=self.client)
        self.pos: POS= POS()
        self.shipping_providers= ShippingProviders()
        self.hr= HR()
