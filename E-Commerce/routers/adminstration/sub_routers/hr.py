from json import dumps as jsonParser
import json
from content import Content
from utils import Utils
from database.database import Database
from config import Config
from flask import Flask, render_template, url_for, request, redirect, session, send_file
import sys
import os
from io import BytesIO
from pypdf import PdfMerger
sys.path.insert(0, '../')
sys.path.insert(0, '../../')


class HRSubRouter:
    def __init__(self, app: Flask):
        self.app: Flask = app
        self.cfg: Config = Config()
        self.database: Database = Database()
        self.utils: Utils = Utils()
        self.content: Content = Content()

    def setup(self):
        self.assign_hr_index()
        self.assign_create_agent()
        self.assign_update_agent()
        self.assign_withdraw_agent_salary()

    def assign_withdraw_agent_salary(self):
        @self.app.route('/webapp/adminstration/hr/withdraw/', methods=['PATCH'])
        def withdraw_agent_salary():
            try:
                url_params= dict(request.values)
                agent_data= self.database.hr.get_agent_by_id(url_params['id'])
                salary_value= (agent_data['salary'] + sum(agent_data['bonuses'])) - sum(agent_data['deciplines'])
                self.database.hr.update_agent({'id': url_params['id'], 'bonuses': [], 'deciplines': []})
                self.database.pos.add_entry(mode='output', direction= f'Salary: ({agent_data["name"]})', amount=salary_value, recorded_by=session.get('CURRENT_ADMIN_ID'))
                return self.app.response_class(status= 200)
            except Exception as e:
                print(e)
                return self.app.response_class(status= 500)
            

    def assign_update_agent(self):
        @self.app.route('/webapp/adminstration/hr/', methods=["PATCH"])
        def update_agent():
            body= dict(json.loads(request.data))
            if not body['mode'] == None:
                res= self.database.hr.kpi(mode= body['mode'], agent_id= body['id'], amount= int(body['amount']))
                if res:
                    return self.app.response_class(status= 200)
                return self.app.response_class(status= 500)
            else:
                return self.app.response_class(status= 500)
                

    def assign_create_agent(self):
        @self.app.route('/webapp/adminstration/hr/', methods=["POST"])
        def create_agent():
            try:
                body= dict(json.loads(request.data))
                res= self.database.hr.create_agent(body)
                if res:
                    return self.app.response_class(status= 201)
                
                return self.app.response_class(status= 500)
                
            except Exception as e:
                print(e)
                return self.app.response_class(status=500)

    def assign_hr_index(self):
        @self.app.route('/webapp/adminstration/hr/', methods=["GET"])
        def hr_index():
            params = dict(request.values)

            aid = session.get("CURRENT_ADMIN_ID", None)
            if aid is None:
                return redirect('{}/webapp/adminstration/login/'.format(self.cfg.base_url))

            admin_data = self.database.admins.get_admin_by_id(aid)
            self.database.hr.init_data()
            return render_template(
                'adminstration/hr/index.html',
                cfg=self.cfg,
                database=self.database,
                content=self.content,
                admin_data=admin_data,
                utils=self.utils,
                len=len,
                lang="en",
                dumps=json.dumps,
            )
