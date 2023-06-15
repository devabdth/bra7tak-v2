import sys
sys.path.insert(0, '../')

from database.orders import Order
from database.products import Products
from io import BytesIO
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from reportlab_qrcode import QRCodeImage
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
import os

# Initi Font Family
pdfmetrics.registerFont(TTFont('Cairo', os.path.join(
    os.path.dirname(__file__), 'Cairo-Regular.ttf')))




class InvoiceGenerator:
    def __init__(self, order: Order, utils):
        self.shipping_options= Products.load_shipping_options()
        self.utils = utils
        self.order = order.to_dict()
        self.logo = ImageReader(os.path.join(
            os.path.dirname(__file__), 'logo.png'))
        self.path = os.path.abspath(os.path.join(os.path.join(os.path.dirname(
            __file__), '../routers/assets/invoices'), '{}.pdf'.format(self.order['id'])))

    def generate_invoice(self):
        canvas = Canvas(self.path, pagesize=A4, bottomup=0)
        canvas.setFillColorRGB(0.1, 0.1, 0.1)

        canvas.line(5*mm, 45*mm, 200*mm, 45*mm)
        canvas.line(15*mm, 120*mm, 195*mm, 120*mm)
        canvas.line(35*mm, 108*mm, 35*mm, 220*mm)
        canvas.line(115*mm, 108*mm, 115*mm, 220*mm)
        canvas.line(135*mm, 108*mm, 135*mm, 220*mm)
        canvas.line(160*mm, 108*mm, 160*mm, 220*mm)
        canvas.line(15*mm, 220*mm, 195*mm, 220*mm)

        canvas.translate(10*mm, 40*mm)
        canvas.scale(1, -1)
        canvas.drawImage(self.logo, 0, 0, width=48 *
                         mm, height=32*mm, mask='auto')

        canvas.scale(1, -1)
        canvas.translate(-10*mm, -40*mm)

        QRCodeImage(self.order['policeNumber'],
                    size=32*mm).drawOn(canvas, 170*mm, 8*mm)
        QRCodeImage(self.order['id'], size=32*mm).drawOn(canvas, 140*mm, 8*mm)

        canvas.setFont("Cairo", 5*mm)
        canvas.drawRightString(60*mm, 60*mm, "Address :")
        canvas.setFont("Cairo", 5*mm)
        canvas.drawRightString(
            190*mm, 60*mm, get_display(arabic_reshaper.reshape(str(self.order['address']))))

        canvas.setFont("Cairo", 5*mm)
        canvas.drawRightString(60*mm, 70*mm, "Follow-up Address :")
        canvas.setFont("Cairo", 5*mm)
        canvas.drawRightString(
            190*mm, 70*mm, get_display(arabic_reshaper.reshape(str(self.order['addressLineTwo']))))

        canvas.setFont("Cairo", 5*mm)
        canvas.drawRightString(60*mm, 80*mm, "Date :")
        canvas.setFont("Cairo", 5*mm)
        canvas.drawRightString(190*mm, 80*mm, self.order['placedIn'][:16])

        canvas.setFont("Cairo", 5*mm)
        canvas.drawRightString(60*mm, 90*mm, "Customer Name :")

        canvas.drawRightString(
            190*mm, 90*mm, get_display(arabic_reshaper.reshape(self.order['username'])))

        canvas.drawRightString(60*mm, 100*mm, "Phone No. :")
        canvas.setFont("Cairo", 5*mm)
        canvas.drawRightString(190*mm, 100*mm, self.order['userPhone'])

        canvas.roundRect(15*mm, 108*mm, 180*mm, 140*mm, 5*mm, stroke=1, fill=0)
        canvas.drawCentredString(75*mm, 118*mm, "Products")
        canvas.drawCentredString(148*mm, 118*mm, "Qty.")
        canvas.drawCentredString(125*mm, 118*mm, "Price")
        canvas.drawCentredString(178*mm, 118*mm, "Total")
        canvas.setFont("Cairo", 4*mm)
        canvas.drawCentredString(25*mm, 255*mm, "Comments")
        canvas.setFont("Cairo", 3*mm)
        canvas.drawCentredString(30*mm, 260*mm, str(self.order['comment'][:500]))

        current_line = 130*mm
        index = 1
        cart = []
        for product in self.order['products']:
            cart.append({
                'id': product['id'],
                "color": product['color'] if 'color' in product.keys() else None,
                "size": product['size'] if 'size' in product.keys() else None
            })
        cart = self.utils.cart_calculations(cart)
        for product in cart['PRODUCTS'][:7]:
            canvas.setFont("Cairo", 5*mm)
            canvas.drawCentredString(25*mm, current_line, str(index))
            canvas.setFont("Cairo", 5*mm)
            canvas.drawCentredString(
                75*mm, current_line, product['PRODUCT_DATA'].name['en'])
            canvas.setFont("Cairo", 5*mm)
            canvas.drawCentredString(
                148*mm, current_line, str(product['COUNT']))
            if product['COUNT'] < 2:
                canvas.drawCentredString(
                    125*mm, current_line, str(product['PRODUCT_DATA'].pricing['currentPrice']))
                canvas.drawCentredString(170*mm, current_line, "{} L.E.".format(str(self.utils.format_price(
                    product['COUNT'] * product['PRODUCT_DATA'].pricing['currentPrice'], show_curr=False, show_full=True))))
            if product['COUNT'] >= 2 and product['COUNT'] < 4:
                canvas.drawCentredString(
                    125*mm, current_line, str(product['PRODUCT_DATA'].pricing['twoPiecesPrice']))
                canvas.drawCentredString(170*mm, current_line, "{} L.E.".format(str(self.utils.format_price(
                    product['COUNT'] * product['PRODUCT_DATA'].pricing['twoPiecesPrice'], show_curr=False, show_full=True))))
            if product['COUNT'] >= 4 and product['COUNT'] < 6:
                canvas.drawCentredString(
                    125*mm, current_line, str(product['PRODUCT_DATA'].pricing['fourPiecesPrice']))
                canvas.drawCentredString(170*mm, current_line, "{} L.E.".format(str(self.utils.format_price(
                    product['COUNT'] * product['PRODUCT_DATA'].pricing['fourPiecesPrice'], show_curr=False, show_full=True))))
            if product['COUNT'] >= 6 and product['COUNT'] < 12:
                canvas.drawCentredString(
                    125*mm, current_line, str(product['PRODUCT_DATA'].pricing['sixPiecesPrice']))
                canvas.drawCentredString(170*mm, current_line, "{} L.E.".format(str(self.utils.format_price(
                    product['COUNT'] * product['PRODUCT_DATA'].pricing['sixPiecesPrice'], show_curr=False, show_full=True))))
            if product['COUNT'] >= 12:
                canvas.drawCentredString(
                    125*mm, current_line, str(product['PRODUCT_DATA'].pricing['dozinPiecesPrice']))
                canvas.drawCentredString(170*mm, current_line, "{} L.E.".format(str(self.utils.format_price(
                    product['COUNT'] * product['PRODUCT_DATA'].pricing['dozinPiecesPrice'], show_curr=False, show_full=True))))
            current_line += 12*mm
            index += 1

        canvas.setFont("Cairo", 10)
        canvas.drawRightString(60*mm, 230*mm, "Products Price:")
        canvas.setFont("Cairo", 5*mm)
        canvas.drawRightString(80*mm, 230*mm, str(cart['PRODUCTS_PRICE']))

        canvas.setFont("Cairo", 10)
        canvas.drawRightString(150*mm, 230*mm, "VAT:")
        canvas.setFont("Cairo", 5*mm)
        canvas.drawRightString(170*mm, 230*mm, str(cart['TOTAL_VAT']))

        canvas.setFont("Cairo", 10)
        canvas.drawRightString(60*mm, 240*mm, "Shipping Fees:")
        canvas.setFont("Cairo", 5*mm)
        canvas.drawRightString(80*mm, 240*mm, str(self.shipping_options[str(self.order['cityCode'])]['fees']))

        canvas.setFont("Cairo", 10)
        canvas.drawRightString(150*mm, 240*mm, "Total:")
        canvas.setFont("Cairo", 5*mm)
        canvas.drawRightString(170*mm, 240*mm, str(cart['TOTAL_PRICE']))

        canvas.setFont("Cairo", 12)
        canvas.drawCentredString(
            105*mm, 290*mm, "All Copyrights reserved © Cubers IO Inc, 2023")

        canvas.showPage()
        canvas.save()
        return self.path
