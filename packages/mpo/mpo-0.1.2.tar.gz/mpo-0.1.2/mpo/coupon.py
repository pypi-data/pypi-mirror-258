

class CouponMapper():

    lang = '1'

    def __init__(self,lang='1') -> None:
        self.lang = lang

    def to_odoo(self,prestashop):

        tax_reduction = "tax_excluded"

        discount_type = "fixed_amount"

        if float(prestashop["reduction_amount"]) <= 0:
            discount_type = "percentage"

        if bool( prestashop["reduction_tax"] ):
            tax_reduction = "tax_included"

        odoo = {
            "name": prestashop["name"],
            "active": bool(prestashop['active']),
            "program_type": "promotion_program",
            "rule_partners_domain": False,
            "rule_min_quantity": prestashop["quantity_per_user"],
            "rule_minimum_amount": prestashop["minimum_amount"],
            "promo_code_usage": "code_needed",
            "promo_code": prestashop["code"],
            "rule_date_from": prestashop["date_from"],
            "rule_date_to": prestashop["date_to"],
            "reward_type": "discount",
            "reward_product_id": False,
            "reward_product_quantity": prestashop["quantity_per_user"],
            "promo_applicability": "on_current_order",
            "discount_percentage": prestashop["reduction_percent"],
            "discount_fixed_amount": prestashop["reduction_amount"],
            "discount_apply_on": "on_order",
            "rule_minimum_amount_tax_inclusion": tax_reduction,
            "maximum_use_number": 0,
            "validity_duration": 0,
            "discount_type": discount_type

        }

        return odoo

    def to_prestashop(self, odoo):

        min_amount = "0"

        # if float(odoo["rule_minimum_amount"]) > 0 :
        #     min_amount = "1"
        
        return {
            "cart_rule": {
            "id_customer": "0",
            "date_from": odoo["rule_date_from"],
            "date_to": odoo["rule_date_to"],
            "description": "",
            "quantity_per_user": odoo["rule_min_quantity"],
            "partial_use": "1",
            "code": odoo["promo_code"],
            "minimum_amount": odoo["rule_minimum_amount"],
            "active": "1",
            'name': {'language': {
                    'attrs': {'id': self.lang},
                    'value': odoo['name'],}
            },
            "minimum_amount_tax": min_amount,
            "reduction_percent": float(odoo["discount_percentage"]),
            "reduction_amount": float(odoo["discount_fixed_amount"])
            } 
        }
