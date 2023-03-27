from flask import Flask
from flask_session import Session
from flask_qrcode import QRcode

def setup(app: Flask):

	app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

	app.config["SESSION_PERMANENT"] = False
	app.config["SESSION_TYPE"] = "filesystem"
	app.config["DEBUG"]= True
	app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

	Session(app)
	QRcode(app)

	from routers.home.router import HomeRouter
	HomeRouter(app= app).setup()
	
	from routers.assets.router import AssetsRouter
	AssetsRouter(app= app).setup()

	from routers.categories.router import CategoriesRouter
	CategoriesRouter(app= app).setup()

	from routers.products.router import ProductsRouter
	ProductsRouter(app= app).setup()

	from routers.search.router import SearchRouter
	SearchRouter(app= app).setup()

	from routers.login.router import LoginRouter
	LoginRouter(app= app).setup()

	from routers.signup.router import SignUpRouter
	SignUpRouter(app= app).setup()

	from routers.signup_process.router import SignUpProcessRouter
	SignUpProcessRouter(app= app).setup()

	from routers.config.router import ConfigRouter
	ConfigRouter(app= app).setup()

	from routers.profile.router import ProfileRouter
	ProfileRouter(app= app).setup()

	from routers.collections.router import CollectionsRouter
	CollectionsRouter(app= app).setup()

	from routers.cart.router import CartRouter
	CartRouter(app= app).setup()

	from routers.favourites.router import FavouritesRouter
	FavouritesRouter(app= app).setup()

	from routers.users.router import UsersRouter
	UsersRouter(app= app).setup()

	from routers.not_found.router import NotFoundRouter
	NotFoundRouter(app= app).setup()

	from routers.checkout.router import CheckoutRouter
	CheckoutRouter(app= app).setup()

	from routers.adminstration.router import AdminstrationRouter
	AdminstrationRouter(app= app).setup()

	from routers.orders.router import OrdersRouter
	OrdersRouter(app= app).setup()
