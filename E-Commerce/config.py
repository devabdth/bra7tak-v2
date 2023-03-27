from os import environ
from dotenv import load_dotenv

class Config:
	def __init__(self):
		load_dotenv()
		self.port = environ['PORT'] if 'PORT' in environ else 3030
		self.debug = (environ['MODE'] if 'MODE' in environ else 0) == 0
		self.auth_key = environ['AUTH_KEY'] if 'AUTH_KEY' in environ else '1234567890'
		self.base_url = environ['BASE_URL'] if 'BASE_URL' in environ else 'http://127.0.0.1:{}'.format(self.port)
		self.meta_key= environ['META_KEY'] if 'META_KEY' in environ else "lsdkfjsldcmsslf;a;ldskfjjweporwpfs;dlfjw;mcwe"
		
		#self.db_url= environ['DB_URL'] if 'DB_URL' in environ else "mongodb://localhost/bra7tak"
		self.db_url= environ['DB_URL'] if 'DB_URL' in environ else "mongodb+srv://website:dXqqOKLEjWc0bTQT@cluster0.hr5uyvd.mongodb.net/?retryWrites=true&w=majority"
		self.facebook = environ['FACEBOOK'] if 'FACEBOOK' in environ else "None"
		self.instagram= environ['INSTAGRAM'] if 'INSTAGRAM' in environ else "None"
		self.linkedin = environ['LINKEDIN'] if 'LINKEDIN' in environ else "None"
		self.twitter= environ['TWITTER'] if 'TWITTER' in environ else "None"
		self.tiktok = environ['TIKTOK'] if 'TIKTOK' in environ else "None"

		self.email_model_email= environ['EMAIL_MODEL_EMAIL'] if 'EMAIL_MODEL_EMAIL' in environ else ""
		self.email_model_access_key= environ['EMAIL_MODEL_AUTH_KEY'] if 'EMAIL_MODEL_AUTH_KEY' in environ else ""
		self.meta_description = environ['DESCRIPTION'] if 'DESCRIPTION' in environ else "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus vitae mauris in tortor ornare mollis ac nec nisi. Donec in felis dui. Sed velit tellus, convallis nec congue et, vulputate sit amet sem. Aliquam lorem tellus, faucibus at eros in, facilisis tristique ipsum. Vestibulum a pretium quam. Suspendisse tristique purus ac arcu maximus, vel malesuada sapien dictum. Sed a convallis lectus."

		self.supported_checkout_methods: dict= {
			0: {
				"title": 'cashOnDelivery',
				"supported": True
			},
			1: {
				"title": 'paypal',
				"supported": False
			},
			2: {
				"title": 'creditCard',
				"supported": False
			},
			3: {
				"title": 'points',
				"supported": False
			},
			4: {
				"title": 'vouchers',
				"supported": False
			},
		}
