from flask import Flask
from flask_session import Session
from flask_qrcode import QRcode
import os
import json


def setup(app: Flask):
	setup_app(app)
	setup_files()
	setup_routers(app)

def setup_app(app: Flask):
	app.config.update(SESSION_COOKIE_SAMESITE="None",
					  SESSION_COOKIE_SECURE=True)

	# App Configuration
	app.config["SESSION_PERMANENT"] = False
	app.config["SESSION_TYPE"] = "filesystem"
	app.config["DEBUG"] = True
	app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

	# Setup Extensions
	Session(app)
	QRcode(app)


def setup_routers(app: Flask):
	# Routers Assignment
	from routers.home.router import HomeRouter
	HomeRouter(app=app).setup()

	from routers.assets.router import AssetsRouter
	AssetsRouter(app=app).setup()

	from routers.categories.router import CategoriesRouter
	CategoriesRouter(app=app).setup()

	from routers.products.router import ProductsRouter
	ProductsRouter(app=app).setup()

	from routers.search.router import SearchRouter
	SearchRouter(app=app).setup()

	from routers.login.router import LoginRouter
	LoginRouter(app=app).setup()

	from routers.signup.router import SignUpRouter
	SignUpRouter(app=app).setup()

	from routers.signup_process.router import SignUpProcessRouter
	SignUpProcessRouter(app=app).setup()

	from routers.config.router import ConfigRouter
	ConfigRouter(app=app).setup()

	from routers.profile.router import ProfileRouter
	ProfileRouter(app=app).setup()

	from routers.collections.router import CollectionsRouter
	CollectionsRouter(app=app).setup()

	from routers.cart.router import CartRouter
	CartRouter(app=app).setup()

	from routers.favourites.router import FavouritesRouter
	FavouritesRouter(app=app).setup()

	from routers.users.router import UsersRouter
	UsersRouter(app=app).setup()

	from routers.not_found.router import NotFoundRouter
	NotFoundRouter(app=app).setup()

	from routers.checkout.router import CheckoutRouter
	CheckoutRouter(app=app).setup()

	from routers.orders.router import OrdersRouter
	OrdersRouter(app=app).setup()

	from routers.documentations.router import DocumentationsRouter
	DocumentationsRouter(app=app).setup()

	# Adminstration Routers Assignment
	from routers.adminstration.router import AdminstrationRouter
	AdminstrationRouter(app=app).setup()

def setup_files():
	# Directories Creation
	dirs= ['./jsons/', './csvs/']
	for dir_ in dirs:
		if not os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), dir_))):
			os.mkdir(dir_)	
	# Files Creation
	files= [
		{
			'file_path': './jsons/admins.json',
			'initial_data': {},
		},
		{
			'file_path': './jsons/categories.json',
			'initial_data': {},
		},
		{
			'file_path': './jsons/collections.json',
			'initial_data': {},
		},
		{
			'file_path': './jsons/banners.json',
			'initial_data': {
				"mainBanner": {},
				"subBannerTwo": {},
				"subBannerOne": {},
			},
		},
		{
			'file_path': './jsons/inventoryLog.json',
			'initial_data': {
				"deposits": [],
				"withdraws": [],
				"orderWithdraws": [],
				"dealsWithdraws": []				
			},
		},
		{
			'file_path': './jsons/inventoryRequests.json',
			'initial_data': {
				"activeDepositRequests": {},
				"archivedDepositRequests": {},
				"archivedWithdrawRequests": {},
				"activeWithdrawRequests": {},
			},
		},
		{
			'file_path': './jsons/pos.json',
			'initial_data': {"inputs": [], "outputs": []},
		},
		{
			'file_path': './jsons/metaInfo.json',
			'initial_data': {
				"inventoryBoundries": {
					"redScope": 0,
					"yellowScope": 0,
					"greenScope": 0,
				}
			},
		},
		{
			'file_path': './csvs/shippingOptions.csv',
			'initial_data': "cityId,duration,fee\n0,0,0\n1,0,0\n2,0,0\n3,0,0\n4,0,0\n5,0,0\n6,0,0\n7,0,0\n8,0,0\n9,0,0\n10,0,0\n11,0,0\n12,0,0\n13,0,0\n14,0,0\n15,0,0\n16,0,0\n17,0,0\n18,0,0\n19,0,0\n20,0,0\n21,0,0\n22,0,0\n23,0,0\n24,0,0\n25,0,0\n26,0,0",
		},
		{
			'file_path': './jsons/shippingProviders.json',
			'initial_data': {}
		},
		{
			'file_path': './jsons/agents.json',
			'initial_data': {}
		},
	]

	for file_ in files:
		if not os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), file_['file_path']))):
			with open(file_['file_path'], 'w') as f:
				json.dump(file_['initial_data'], f)


