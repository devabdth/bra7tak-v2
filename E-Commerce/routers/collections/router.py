import sys
sys.path.insert(0, '../')


from flask import Flask, render_template, url_for, session

from config import Config
from content import Content
from database.database import Database
from layout.layout import Layout


class CollectionsRouter:
	def __init__(self, app: Flask):
		self.app= app
		self.cfg: Config= Config()
		self.database: Database= Database()
		self.layout: Layout= Layout()
		self.content: Content= Content()


	def setup(self):
		self.assign_single_collection()


	def assign_single_collection(self):
		@self.app.route('/collections/<collection_id>')
		def single_collection_index(collection_id):
			collection = self.database.collections.get_collection_by_id(collection_id)
			if collection == None:
				return redirect('{}/404/collection/'.format(self.cfg.base_url))

			lang = session.get("LANG", "en")
			uid= session.get("CURRENT_USER_ID", None)
			if lang == 'en':
				primary_font_family= 'Raleway'
				second_font_family= 'Poppins'
			elif lang == 'ar':
				primary_font_family= 'Cairo'
				second_font_family= 'Cairo'

			if collection is None:
				return render_template(
					'global/not_found.html',
					lang= lang,
					cfg= self.cfg,
				)
			if not uid is None:
				user_data= self.database.users.get_user_by_id(uid)
				return render_template(
					'collections/single_collection/index.html',
					uid= uid,
					user_data= user_data,
					collection= collection,
					lang= lang,
					cfg= self.cfg,
					content= self.content,
					primary_font_family= primary_font_family,
					second_font_family= second_font_family,
					len= len,
					database= self.database,
					layout= self.layout
				)
			return render_template(
				'collections/single_collection/index.html',
				lang= lang,
				collection= collection,
				cfg= self.cfg,
				content= self.content,
				primary_font_family= primary_font_family,
				second_font_family= second_font_family,
				len= len,
				database= self.database,
				layout= self.layout
			)

