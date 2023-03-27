from layout.layout import Layout
from database.database import Database
from content import Content
from config import Config

from flask import Flask, render_template, url_for, session, redirect, request

import sys
sys.path.insert(0, '../')


class LoginRouter:
    def __init__(self, app: Flask):
        self.app: Flask = app
        self.content: Content = Content()
        self.database: Database = Database()
        self.layout: Layout = Layout()
        self.cfg: Config = Config()

    def setup(self):
        self.assign_login_index()

    def assign_login_index(self):
        @self.app.route('/login/', methods=["GET"])
        @self.app.route('/entryAuth/', methods=["GET"])
        def login_index():
            if session.get('CURRENT_USER_ID', None) != None:
                return redirect('/profile/')

            params = dict(request.values)
            if 'customRecall' in params.keys():
                custom_recall = params['customRecall'] or None
                if not custom_recall is None:
                    custom_recall = "{}/{}".format(
                        self.cfg.base_url,
                        custom_recall
                    )
            else:
                custom_recall = None

            custom_email = params['email'] if 'email' in params.keys() else ''

            lang = session.get("LANG", "en")
            if lang == 'en':
                primary_font_family = 'Raleway'
                second_font_family = 'Poppins'
            elif lang == 'ar':
                primary_font_family = 'Cairo'
                second_font_family = 'Cairo'

            if not session.get('CURRENT_URER_ID', None) is None:
                return redirect('{}/profile/'.format(self.cfg.base_url))

            return render_template(
                'login/index.html',
                lang=lang,
                cfg=self.cfg,
                content=self.content,
                primary_font_family=primary_font_family,
                second_font_family=second_font_family,
                database=self.database,
                layout=self.layout,
                len=len,
                custom_recall=custom_recall,
                custom_email=custom_email
            )
