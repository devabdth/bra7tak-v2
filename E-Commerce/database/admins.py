import os
import json
import secrets


class Admin:
	def __init__(self, username: str, access_key: str, name: str, accesses: list, log: dict, aid: str):
		self.aid= aid
		self.username= username
		self.access_key= access_key
		self.name= name
		self.accesses= accesses
		self.log= log



class Admins:
	def __init__(self):
		self.load()

	def load(self):
		with open(os.path.join(os.path.dirname(__file__), '../jsons/admins.json'), 'r') as f:
			self.admins_file_data: dict= dict(json.loads(f.read()))
			f.close()

			self.admins_data: dict= {ad['aid']: ad for ad in self.admins_file_data.values()}


	def create_admin(self, admin_data: dict) -> bool:
		try:
			self.admins_data['{}'.format(len(self.admins_data))]= {
				"aid": str(secrets.token_hex(12)),
				'name': admin_data['name'],
				'username': admin_data['username'],
				'accessKey': admin_data['accessKey'],
				'accesses': admin_data['activeAccesses'],
				'log': {}
			}

			with open(os.path.join(os.path.dirname(__file__), '../jsons/admins.json'), 'w') as f:
				json.dump(self.admins_data, f)
				f.close()

			return True
		except Exception as e:
			print(e)
			return False


	def get_admin_by_id(self, aid: str):
		self.load()
		return self.admins_data[aid]

	def get_admin_by_username(self, admin_username: str):
		self.load()
		for admin in self.admins_data.values():
			if admin['username'] == admin_username:
				return admin

		return None

	def delete_admin(self, aid):
		del self.admins_data[aid]
		with open(os.path.join(os.path.dirname(__file__), '../jsons/admins.json'), 'w') as f:
			json.dump(self.admins_data, f)
			f.close()

		return True

