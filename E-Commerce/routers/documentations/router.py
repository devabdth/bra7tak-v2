from utils import Utils
from layout.layout import Layout
from database.database import Database
from content import Content
from config import Config
from flask import Flask, render_template, url_for, session
import sys
sys.path.insert(0, '../')


class DocumentationsRouter:
	def __init__(self, app: Flask):
		self.cfg: Config = Config()
		self.app = app
		self.content: Content = Content()
		self.database: Database = Database()
		self.layout: Layout = Layout()
		self.utils: Utils = Utils()

	def setup(self):
		self.assign_refund_policy()
		self.assign_privacy_policy()
		self.assign_terms_and_conditions()

	def assign_refund_policy(self):
		@self.app.route('/refundPolicy/')
		@self.app.route('/refund_policy/')
		def refund_policy():
			lang = session.get("LANG", "en")
			uid= session.get("CURRENT_USER_ID", None)
			if lang == 'en':
				primary_font_family= 'Raleway'
				second_font_family= 'Poppins'
			elif lang == 'ar':
				primary_font_family= 'Cairo'
				second_font_family= 'Cairo'
			if not uid is None:
				user_data= self.database.users.get_user_by_id(uid)
				return render_template(
					'refund_policy/index.html',
					database= self.database,
					len= len,
					uid= uid,
					user_data= user_data,
					lang= lang,
					cfg= self.cfg,
					content= self.content,
					primary_font_family= primary_font_family,
					second_font_family= second_font_family,
					utils= self.utils
				)
			return render_template(
				'refund_policy/index.html',
				database= self.database,
				len= len,
				lang= lang,
				cfg= self.cfg,
				content= self.content,
				primary_font_family= primary_font_family,
				second_font_family= second_font_family,
				utils= self.utils
			)




	def assign_privacy_policy(self):
		@self.app.route('/privacyPolicy/')
		@self.app.route('/privacy_policy/')
		def privacy_policy():
			lang = session.get("LANG", "en")
			uid= session.get("CURRENT_USER_ID", None)
			if lang == 'en':
				primary_font_family= 'Raleway'
				second_font_family= 'Poppins'
			elif lang == 'ar':
				primary_font_family= 'Cairo'
				second_font_family= 'Cairo'
			if not uid is None:
				user_data= self.database.users.get_user_by_id(uid)
				return render_template(
					'privacy_policy/index.html',
					database= self.database,
					len= len,
					uid= uid,
					user_data= user_data,
					lang= lang,
					cfg= self.cfg,
					content= self.content,
					primary_font_family= primary_font_family,
					second_font_family= second_font_family,
					utils= self.utils
				)
			return render_template(
				'privacy_policy/index.html',
				database= self.database,
				len= len,
				lang= lang,
				cfg= self.cfg,
				content= self.content,
				primary_font_family= primary_font_family,
				second_font_family= second_font_family,
				utils= self.utils
			)




	def assign_terms_and_conditions(self):
		@self.app.route('/termsAndConditions/')
		@self.app.route('/terms_and_conditions/')
		def terms_and_conditions():
			lang = session.get("LANG", "en")
			uid= session.get("CURRENT_USER_ID", None)
			if lang == 'en':
				primary_font_family= 'Raleway'
				second_font_family= 'Poppins'
			elif lang == 'ar':
				primary_font_family= 'Cairo'
				second_font_family= 'Cairo'
			if not uid is None:
				user_data= self.database.users.get_user_by_id(uid)
				return render_template(
					'terms_and_conditions/index.html',
					database= self.database,
					len= len,
					uid= uid,
					user_data= user_data,
					lang= lang,
					cfg= self.cfg,
					content= self.content,
					primary_font_family= primary_font_family,
					second_font_family= second_font_family,
					utils= self.utils
				)
			return render_template(
				'terms_and_conditions/index.html',
				database= self.database,
				len= len,
				lang= lang,
				cfg= self.cfg,
				content= self.content,
				primary_font_family= primary_font_family,
				second_font_family= second_font_family,
				utils= self.utils
			)

