import os
import json
from datetime import datetime
import time
from pandas import DataFrame, concat
import secrets

class ShippingProvider:
    def __init__(
            self, id: str, name: str, del_days: dict, fees: dict
        ):
        self.id= id
        self.name= name
        self.del_days= del_days
        self.fees= fees

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'del_days': self.del_days,
            'fees': self.fees,
        }

    
class ShippingProviders:
    def __init__(self):
        self.read_data()

    def read_data(self):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../jsons/shippingProviders.json'))) as f:
            data= dict(json.loads(f.read()))
            self.shipping_providers= [
                ShippingProvider(
                    id= entry['id'],
                    name= entry['name'],
                    fees= entry['fees'],
                    del_days= entry['del_days'],
                ) for entry in data.values()
            ]
    

    def write_data(self):
        data= {
            sh.id: sh.to_dict() for sh in self.shipping_providers
        }
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../jsons/shippingProviders.json')), 'w') as f:
            json.dump(data, f)
    

    def delete_shipping_provider(self, sh_id):
        try:
            for sh in self.shipping_providers:
                if sh.id == sh_id:
                    del self.shipping_providers[self.shipping_providers.index(sh)]
                    self.write_data()
                    return True
        except Exception as e:
            return False
            

    def create_shipping_provider(self, name, fees, del_days):
        try:
            sh= ShippingProvider(
                id= str(secrets.token_hex(12)),
                name= name, fees= fees, del_days= del_days,
            )

            self.shipping_providers.append(sh)
            self.write_data()
            return True
        except Exception as e:
            print(e)
            return False

    def update_shipping_provider(self, sh_id, payload):
        try:
            for sh in self.shipping_providers:
                if sh.id == sh_id:
                    if 'name' in payload.keys():
                        sh.name= payload['name']
                    if 'fees' in payload.keys():
                        sh.fees= payload['fees']
                    if 'del_days' in payload.keys():
                        sh.del_days= payload['del_days']

                    self.write_data()
                    return True
            return False
        except Exception as e:
            print(e)
            return False
