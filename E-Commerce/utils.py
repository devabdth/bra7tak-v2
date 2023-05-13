from invoice_gen.app import InvoiceGenerator
from pandas import to_datetime


class Utils:
    def __init__(self):
        self.inv_gen = InvoiceGenerator
        self.accesses= [
            'Overview',
            'Shipping Informations',
            'Inventory',
            'Orders',
            'POS',
            'Categories',
            'Products',
            'Banners',
            'Users',
            'Admins'
        ]

        self.jobs= [
            'Adminstration',
            'Executive',
            'Executive Assistant',
            'Advisor',
            'Manager',
            'HR Manager',
            'Product Manager',
            'Project Manager',
            'Finance Manager',
            'Quality Manager',
            'Process Manager',
            'Marketing Manager',
            'Operations Manager',
            'Marketing Specialist',
            'Business Analyst',
            'Customer Service Representative',
            'Sales Representative',
            'Social Media Representative',
            'Social Media Moderator',
            'Accountant',
            'Adminstrative Assistant',
            'Accountant',
            'Chief Executive Officer (CEO)',
            'Chief Operating Officer (COO)',
            'Chief Financial Officer (CFO)',
            'Chief Marketing Officer (CMO)',
            'Chief Technology Officer (CTO)',
            'Branch Manager',
            'Branch Agent',
            'IT',
            'Technical Support Manager',
            'Technical Support Agent',
            'Technical Support Assistant',
            'Technical Support Advisor',
            'E-Commerce Manager',
            'E-Commerce Admin',
            'E-Commerce Maintainer',
            'Help Desk',
            'Office Manager',
            'Office Boy',
            'Inventory Manager',
            'Inventory Agent',
            'Inventroy Admin',
            'Content Creator',
            'Content Advisor',
            'Content Reviewer',
            'Copywriter',
            'Supervisor',
            'Superintendent',
            'Overseer',
            'Domain Manager',
        ]

        self.hiring_models= [
            'Full Time',
            'Part Time',
            'Freelancer',
            'Milestone Based'
        ]
        self.status_names = {
            "-3": {
                "en": "Pending",
                "ar": "قيد الإنتظار",
            },
            "-2": {
                "en": "Returned",
                "ar": "مُرتجع",
            },
            "-1": {
                "en": "Canceled",
                "ar": "ملغي",
            },
            "0": {
                "en": "Stocked",
                "ar": "تم التخزين",
            },
            "1": {
                "en": "In Delivery",
                "ar": "قيد التوصيل",
            },
            "2": {
                "en": "Delivered",
                "ar": "تم التوصيل"
            },
        }

    def sum_scopes(self, statuses_reports):
        pass

    def format_date(self, date, show_hour: bool = False):
        if show_hour:
            parts = date.split(' ')
            return "{} / {} / {}<br>{} : {}".format(
                parts[0].split('-')[0],
                parts[0].split('-')[1],
                parts[0].split('-')[2],
                parts[1].split(':')[0],
                parts[1].split(':')[1],
            )

        else:
            return "{} / {} / {}".format(
                date.split('-')[0],
                date.split('-')[1],
                date.split('-')[2]
            )

    def format_date_from_timestamp(self, timestamp):
        from datetime import datetime, timezone
        date = to_datetime(timestamp, unit='ms')
        print(date)
        return self.format_date(str(date), show_hour=True)

    def format_price(self, price, show_curr: bool = True, show_full: bool = False):
        if show_full:
            exp = '{:20,.2f}'
        else:
            exp = '{:20,.0f}'

        if show_curr:
            return "EGP {}".format(
                exp.format(price)
            )
        return "{}".format(
            exp.format(price)
        )

    def cart_calculations(self, cart: list, city_code: int = None) -> dict:
        import sys
        sys.path.insert(0, '../')

        from database.database import Database
        database: Database = Database()

        cart = [ci['id'] for ci in cart]
        cart_: dict = {}
        products_price = 0
        total_vat = 0
        total_shipping_fee = 0

        cart_['PRODUCTS_LENGTH'] = len(cart)
        uniques: list = set(cart)
        cart_['PRODUCTS'] = [
            {
                'COUNT': cart.count(unique),
                'PRODUCT_DATA': database.products.get_product_by_id(unique)
            } for unique in uniques
        ]
        for prod in cart_['PRODUCTS']:
            if prod['COUNT'] < 2:
                products_price += (prod['COUNT'] *
                                   prod['PRODUCT_DATA'].pricing['currentPrice'])
                total_vat += (prod['COUNT'] * prod['PRODUCT_DATA']
                              .pricing['currentPrice']) * prod['PRODUCT_DATA'].vat
            if prod['COUNT'] >= 2 and prod['COUNT'] < 4:
                products_price += (prod['COUNT'] *
                                   prod['PRODUCT_DATA'].pricing['twoPiecesPrice'])
                total_vat += (prod['COUNT'] * prod['PRODUCT_DATA']
                              .pricing['twoPiecesPrice']) * prod['PRODUCT_DATA'].vat
            if prod['COUNT'] >= 4 and prod['COUNT'] < 6:
                products_price += (prod['COUNT'] *
                                   prod['PRODUCT_DATA'].pricing['fourPiecesPrice'])
                total_vat += (prod['COUNT'] * prod['PRODUCT_DATA']
                              .pricing['fourPiecesPrice']) * prod['PRODUCT_DATA'].vat
            if prod['COUNT'] >= 6 and prod['COUNT'] < 12:
                products_price += (prod['COUNT'] *
                                   prod['PRODUCT_DATA'].pricing['sixPiecesPrice'])
                total_vat += (prod['COUNT'] * prod['PRODUCT_DATA']
                              .pricing['sixPiecesPrice']) * prod['PRODUCT_DATA'].vat
            if prod['COUNT'] >= 12:
                products_price += (prod['COUNT'] *
                                   prod['PRODUCT_DATA'].pricing['dozinPiecesPrice'])
                total_vat += (prod['COUNT'] * prod['PRODUCT_DATA']
                              .pricing['dozinPiecesPrice']) * prod['PRODUCT_DATA'].vat

        cart_['PRODUCTS_PRICE'] = products_price
        cart_['TOTAL_VAT'] = total_vat
        cart_['TOTAL_PRICE'] = products_price + total_vat + total_shipping_fee
        return cart_
    
    def calculate_avg(self, input_):
        if len(input_) == 0:
            return 0
        return sum(input_) / len(input_)
