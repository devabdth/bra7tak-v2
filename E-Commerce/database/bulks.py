class Bulk:
	def __init__(self, id: str, title: str, bio: str, products: list, total_price: float, total_vat: float, shipping_fees: dict, asset_file: str):
		self.id= id
		self.title= title
		self.bio= bio
		self.products= products
		self.total_price= total_price
		self.total_vat= total_vat
		self.shipping_fees= shipping_fees
		self.asset_file= asset_file

	def to_dict(self):
		return {
			"id": self.id,
			"title": self.title,
			"bio": self.bio,
			"products": self.products,
			"totalPrice": self.total_price,
			"totalVat": self.total_vat,
			"shippingFees": self.shipping_fees,
			"assetFile": self.asset_file
		}


class Bulks:
	def __init__(self):
		self.bulk= Bulk(
			id="sdfsdfdsf",
			title= "Buy Six get 2",
			bio= "Lorem Ispum",
			total_price= 5000,
			total_vat= 50,
			products= ['{}'.format(x) for x in range(1,6)],
			shipping_fees= {
				0: 20
			},
			asset_file= "nike-shoes.png"
		)


	def get_bulk_by_id(self, bid) -> Bulk:
		return self.bulk