import pymongo
import time
import datetime
from bson.objectid import ObjectId


import sys
sys.path.insert(0, '../')

from config import Config
class User:
	def __init__(
		self, name: str, phone: str, email: str, password: str, id: str, favourites: list, cart: list,
		address_line_one: str, address_line_two: str, gender: int, city_code: int, fav_categories: list,
		orders: list, joined_in: str
	):

		self.id= id
		self.name= name
		self.phone= phone
		self.email= email
		self.password= password
		self.favourites= favourites
		self.fav_categories= fav_categories
		self.cart= cart
		self.address_line_one= address_line_one
		self.address_line_two= address_line_two
		self.gender= gender
		self.city_code= city_code
		self.orders= orders
		self.joined_in= joined_in

	def to_dict(self):
		return {
			"id": str(self.id),
			"name": self.name,
			"phone": self.phone,
			"email": self.email,
			"password": self.password,
			"favourites": self.favourites,
			"favCategories": self.fav_categories,
			"cart": self.cart,
			"addressLineOne": self.address_line_one,
			"addressLineTwo": self.address_line_two,
			"gender": self.gender,
			"cityCode": self.city_code,
			"orders": self.orders,
			"joined_in": self.joined_in,
		}



class Users:
	def __init__(self, client: pymongo.MongoClient):
		self.cfg: Config= Config()
		self.client: pymongo.MongoClient =client
		self.database = self.client["bra7tak"]
		self.users_collection = self.database["users"]

	def create_user(self, payload) -> str:
		try:
			user_= User(
				id= "",
				name=payload["name"],
				email=payload["email"],
				password=payload["password"],
				phone=payload["phone"],
				address_line_one=payload["addressLineOne"],
				address_line_two=payload["addressLineTwo"],
				gender= int(payload["gender"]),
				city_code= int(payload["city"]),
				favourites= [],
				fav_categories= [],
				cart= [],
				orders= [],
				joined_in= str(datetime.date.today())
			)
			user_ = self.users_collection.insert_one(user_.to_dict())

			return str(user_.inserted_id)
		except Exception as e:
			print(e)	
			return None

	def get_all_users(self, search_params):
		return list(self.users_collection.find())
		

	def get_user_by_id(self, uid: str):
		users = self.users_collection.find({'_id': ObjectId(uid)})
		return self.create_user_from_dict(dict(list(users)[0]))

	def get_user_by_username(self, email: str):
		users = self.users_collection.find({'email': email})
		if len(list(users)) == 0:
			return None
		return self.create_user_from_dict(dict(list(users)[0]))


	def check_email_uniquness(self, email):
		users= self.users_collection.find({'email': email})
		return len(list(users)) == 0

	def update_user_data(self, uid: str, user_data):
		try:
			result = self.users_collection.find_one_and_update({'_id': ObjectId(uid)}, {'$set': user_data if type(user_data) is dict else user_data.to_dict()})
			print(self.get_user_by_id(uid))
			return True
		except Exception as e:
			print(e)
			return False


	def delete_user(self, uid: str):
		return True


	def create_user_from_dict(self, dict_: dict):
		return User(
			id= dict_['_id'],
			name= dict_['name'],
			phone= dict_['phone'],
			email= dict_['email'],
			password= dict_['password'],
			favourites= dict_['favourites'],
			fav_categories= dict_['favCategories'],
			cart= dict_['cart'],
			address_line_one= dict_['addressLineOne'],
			address_line_two= dict_['addressLineTwo'],
			gender= int(dict_['gender']),
			city_code= int(dict_['cityCode']),
			orders= [str(order) for order in dict_['orders']],
			joined_in= dict_['joined_in'],
		)

