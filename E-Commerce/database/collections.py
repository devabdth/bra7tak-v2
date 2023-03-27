from .products import Products

import pymongo as pymongo
import os
import json

class Collection:
	def __init__(self, name: dict, msg: dict, bio: dict, id: str, products: list, deadline: int= 0):
		self.name= name
		self.msg= msg
		self.bio= bio
		self.id= id
		self.products= products
		self.deadline= deadline


class Collections:
	def __init__(self, client: pymongo.MongoClient):
		self.products: Products = Products(client)

		with open(os.path.join(os.path.dirname(__file__), '../jsons/collections.json'), "r", encoding="cp866") as f:
			self.collections_file_data= dict(json.loads(f.read()))
		self.flash_sell: Collection= Collection(
			name= self.collections_file_data["0"]["name"],
			bio= self.collections_file_data["0"]["bio"],
			msg= self.collections_file_data["0"]["msg"],
			id= "0",
			products= self.products.get_multiple_products_by_id(self.collections_file_data["0"]["products"]),
			deadline= self.collections_file_data["0"]["deadline"]
		) if "0" in self.collections_file_data.keys() else None


		if "0" in self.collections_file_data.keys():
			del self.collections_file_data["0"]

		self.all_collections= {
			x["id"]: Collection(
				name= x["name"],
				bio= x["bio"],
				msg= x["msg"],
				id= "0",
				products= self.products.get_multiple_products_by_id(x["products"]),
				deadline= x["deadline"]
			)
			for x in self.collections_file_data.values()
		}

	def get_collection_by_id(self, collection_id):
		for col in self.all_collections.values():
			if str(col.id) == collection_id:
				return col
