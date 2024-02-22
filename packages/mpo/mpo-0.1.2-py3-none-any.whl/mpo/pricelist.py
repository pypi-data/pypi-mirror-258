
class PriceListMapper():

    def to_odoo(self,prestashop):

        price_list = {
            "name" : prestashop.get("name" ,""),
            "prestashop_id" : prestashop.get("id" ,"1")
        }

        price_list_item = {
            "applied_on" : "3_global",
            "compute_price" : "percentage",
            "percent_price" : prestashop.get("reduction"),
        }

        return price_list , price_list_item