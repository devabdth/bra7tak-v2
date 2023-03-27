import sys
sys.path.insert(0, '../')

from .ad_banners import AdBanner
from .prodcuts_section import ProductsSection

from config import Config

import os
import json


class Layout:
    def __init__(self):
        self.cfg: Config= Config()
        
        self.load()


    def load(self):

        with open(os.path.join(os.path.dirname(__file__), '../jsons/banners.json'), 'r') as f:
            self.banners_file_data= dict(json.loads(f.read()))
            f.close()
        self.all_banners= {
            x["id"]: AdBanner(
                subtitle= x["subtitle"],
                title= x["title"],
                pricing= x["pricing"],
                action_text= x["actionText"],
                action_link= x["actionLink"] or "", 
                card_action_link= x["cardActionLink"] or "", 
                asset= x["asset"],
                background_color= x["backgroundColor"],
                subtitle_color= x["subtitleColor"],
                title_color= x["titleColor"],
                action_background_color= x["actionBackgroundColor"],
                action_text_color= x["actionTextColor"],
                id= x["id"]
            ) for x in self.banners_file_data.values()
        }

        self.main_banner= self.all_banners["mainBanner"]
        self.sup_banner_one= self.all_banners["subBannerOne"]
        self.sup_banner_two= self.all_banners["subBannerTwo"]

    def update_banner(self, banner_dict):
        try:
            print(banner_dict)

            banner_dict['old']= int(banner_dict['old']) if banner_dict['old'] != "" else None
            banner_dict['new']= int(banner_dict['new']) if banner_dict['new'] != "" else None

            if banner_dict['old'] != None and banner_dict['new'] != None:
                banner_dict['pricing']= {}
                if banner_dict['old'] != None:
                    banner_dict['pricing']['perviousPrice']= banner_dict['old']
                if banner_dict['new'] != None:
                    banner_dict['pricing']['currentPrice']= banner_dict['new']
            else:
                banner_dict['pricing']= None

            del banner_dict['old']
            del banner_dict['new']

            banner_dict['asset']= 'nike-shoes.png'
            print(banner_dict['cardActionLink'])
            if banner_dict['id'] in self.banners_file_data.keys():
                del self.banners_file_data[banner_dict['id']]
                self.banners_file_data[banner_dict['id']]= banner_dict
            with open(os.path.join(os.path.dirname(__file__), '../jsons/banners.json'), 'w') as f:
                json.dump(self.banners_file_data, f)
                f.close()

            self.load()
            return True
        except Exception as e:
            print(e)
            return False


    def get_banner_by_id(self, bid):
        return self.all_banners[bid]
