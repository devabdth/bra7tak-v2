import json
from content import Content
from utils import Utils
from database.database import Database
from config import Config
from flask import Flask, render_template, url_for, request, redirect, session, send_file
from plugins.pos_calcs import POSCalculations
import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../../')


class POSSubRouter:
    def __init__(self, app: Flask):
        self.app: Flask = app
        self.cfg: Config = Config()
        self.database: Database = Database()
        self.utils: Utils = Utils()
        self.content: Content = Content()
        self.pos_calcs: POSCalculations= POSCalculations(self.database)

    def setup(self):
        self.assign_pos_index()

    def assign_pos_index(self):
        @self.app.route('/webapp/adminstration/pos/', methods=['GET'])
        def pos_index():
            aid = session.get("CURRENT_ADMIN_ID", None)
            if aid is None:
                return redirect('{}/webapp/adminstration/login/'.format(self.cfg.base_url))

            admin_data = self.database.admins.get_admin_by_id(aid)

            self.database.products.refresh_all_products()
            return render_template(
                'adminstration/pos/index.html',
                db=self.database,
                content=self.content,
                utils=self.utils,
                calcs= self.pos_calcs,
            )


