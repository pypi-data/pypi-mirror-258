
class TaxMapper():

    lang = '1'

    def __init__(self,lang='1') -> None:
        self.lang = lang

    def to_odoo(self, prestashop):
        return {
            'prestashop_id': prestashop['id'],
            'name': prestashop['name'],
            'active': prestashop['active'],
            'amount': prestashop['rate'],
        }

    def to_prestashop(self, odoo):
        return {
            'tax': {
                'active': odoo['active'],
                'rate': odoo['amount'],
                'name': {'language': {
                    'attrs': {'id': self.lang},
                    'value': odoo['name'],
                }
                },
            }
        }