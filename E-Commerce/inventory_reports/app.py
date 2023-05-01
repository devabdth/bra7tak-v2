from io import BytesIO
from csv import writer
from utils import Utils
from pandas import DataFrame
from database.products import Product
from database.database import Database
import sys
sys.path.insert(0, '../')


class InventoryReports:
    @staticmethod
    def generate_single_product_report(product: Product):

        material = [
            [
                "Index", "Color", "Size", "Pieces", "Total Stock Price"
            ],
        ]
        index = 1
        for color in product.inventory:
            for size in product.inventory[color]:
                material.append([
                    index, color,
                    size, product.inventory[color][size],
                    Utils().format_price(
                        product.inventory[color][size] * product.pricing['stockPrice']).replace('  ', '')
                ])
                index += 1

        buffer = BytesIO()

        df = DataFrame(material)
        df.to_excel(buffer)
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_multiple_products_report(products: list):

        material = [
            [
                "Index", "Product", "Color", "Size", "Pieces", "Total Stock Price"
            ],
        ]
        index = 1
        for product in products:
            for color in product.inventory:
                for size in product.inventory[color]:
                    material.append([
                        index, product.name['en'],  color,
                        size, product.inventory[color][size],
                        Utils().format_price(
                            product.inventory[color][size] * product.pricing['stockPrice']).replace('  ', '')
                    ])
                    index += 1

        buffer = BytesIO()

        df = DataFrame(material)
        df.to_excel(buffer)
        buffer.seek(0)
        return buffer
