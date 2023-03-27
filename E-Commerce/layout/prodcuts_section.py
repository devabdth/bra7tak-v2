from .ad_banners import AdBanner
class ProductsSection:
    def __init__(
        self, products_ids: list, side_ad: AdBanner,
        see_more_action_link: str, is_grid: bool
    ):
        self.products_ids= products_ids
        self.side_ad= side_ad
        self.see_more_action_link= see_more_action_link
        self.is_grid= is_grid