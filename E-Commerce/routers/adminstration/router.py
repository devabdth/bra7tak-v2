from .sub_routers.inventory import InventorySubRouter
from .sub_routers.auth import AuthSubRouter
from .sub_routers.categories import CategoriesSubRouter
from .sub_routers.banners import BannersSubRouter
from .sub_routers.settings import SettingsSubRouter
from .sub_routers.orders import OrdersSubRouter
from .sub_routers.users import UsersSubRouter
from .sub_routers.products import ProductsSubRouter
from .sub_routers.pos import POSSubRouter
from layout.layout import Layout
from database.database import Database
from content import Content
from config import Config
from flask import Flask, request, redirect, url_for, render_template, session
import sys
sys.path.insert(0, '../')


class AdminstrationRouter:
    def __init__(self, app: Flask):
        self.app: Flask = app
        self.cfg: Config = Config()
        self.content: Content = Content()
        self.database: Database = Database()
        self.layout: Layout = Layout()

    def setup(self):
        ProductsSubRouter(app=self.app).setup()
        UsersSubRouter(app=self.app).setup()
        OrdersSubRouter(app=self.app).setup()
        SettingsSubRouter(app=self.app).setup()
        BannersSubRouter(app=self.app).setup()
        CategoriesSubRouter(app=self.app).setup()
        AuthSubRouter(app=self.app).setup()
        InventorySubRouter(app=self.app).setup()
        POSSubRouter(app=self.app).setup()
