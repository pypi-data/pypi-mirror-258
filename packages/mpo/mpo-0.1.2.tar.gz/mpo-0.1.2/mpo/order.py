from datetime import datetime


class OrderMapper():

    lang = '1'

    def __init__(self,lang='1') -> None:
        self.lang = lang

    def to_odoo(self, prestashop, env):
        partner = self._get_partner_for_odoo(prestashop['id_customer'], env)

        if partner:
            tax_amount = float(prestashop['total_paid_tax_incl']) - float(prestashop['total_paid_tax_excl'])  # noqa: E501
            order = {
                'prestashop_id': prestashop['id'],
                'note': prestashop.get('note','') ,
                'partner_id': partner,
                'partner_invoice_id': partner,
                'partner_shipping_id': partner,
                'amount_total': prestashop['total_paid'],
                'amount_tax': tax_amount,
                'carrier_id': self._get_carrier(prestashop['id_carrier'], env),
                'state' : 'sale',
                'date_order' :  datetime.strptime(prestashop['date_add'],'%Y-%m-%d %H:%M:%S'),
                'prestashop_order_state' : self._get_prestashop_state(prestashop['current_state'],env),
                'prestashop_invoice_number' : prestashop['invoice_number'],
                'prestashop_delivery_number' : prestashop['delivery_number'],
            }

            return order
        return None

    def to_prestashop(self, odoo, env):
        partner = self._get_partner(odoo['partner_id'], env, True)

        if partner:

            # tax = odoo['amount_total'] - odoo['amount_tax']

            tax = 0
            total_paid = 0
            total = 0

            order = {
                'order': {
                    'id_lang': self.lang,
                    'id_customer': partner,
                    'note': odoo['note'],
                    # 'total_paid' : odoo['amount_total'],
                    # 'total_paid_tax_incl' : odoo['amount_total'],
                    # 'total_paid_tax_excl' : tax,
                    # 'total_products' : odoo['amount_total'],
                    # 'total_products_wt' : odoo['amount_total'],
                    # 'total_paid_real' : odoo['amount_total'],

                    'total_paid' : total_paid,
                    'total_paid_tax_incl' : total,
                    'total_paid_tax_excl' : tax,
                    'total_products' : total,
                    'total_products_wt' : total,
                    'total_paid_real' : total,


                    'payment': 'esp',
                    'module': 'ps_odoo',
                    'id_carrier': '3',
                    'id_currency': '1',
                    'id_cart': '1',
                    'id_address_invoice': partner,
                    'id_address_delivery': partner,
                    'conversion_rate': '1',

                }
            }

            return order

        return None

    def _get_partner(self, id, env, odoo=False):
        if odoo:
            partner = env['res.partner'].browse(id)
            if partner.exists():
                return partner.prestashop_id
            else:
                return None

        partner = env['res.partner'].search([('prestashop_id', '=', id)],limit=1)
        
        if partner.exists():
            return partner.id

        return None
    
    def _get_partner_for_odoo(self,id,env):
        partner = env['res.partner'].search([('prestashop_id', '=', id)],limit=1)
        if partner.exists():
            return partner.id
        return None
    
    def _get_prestashop_state(self,id , env):
        order_state = env['sale.order.state'].search([('prestashop_id', '=', id)],limit=1)
        if order_state.exists():
            return order_state.id
        return None

    def _get_carrier(self, id, env, odoo=False):
        if odoo:
            carrier = env['delivery.carrier'].browse(id)
            if carrier.exists():
                return carrier.prestashop_id
            else:
                return None

        carrier = env['delivery.carrier'].search([('prestashop_id', '=', id)])
        if carrier.exists():
            return carrier.id

        return None

    def order_line(self,order_id,values, env):
        product = self._get_product(values['product_id'],env)
        
        if product.exists():
            tax_id = self._get_tax(0,env)
            odoo_order_line = {
                'order_id' : order_id,
                'prestashop_id' : values['id'],
                'product_uom_qty': values['product_quantity'],
                'name' : values['product_name'],
                'price_unit' : values['product_price'],
                'product_id': product.id,
                'product_template_id' : product.product_tmpl_id.id,
                'tax_id': tax_id
            }
            return odoo_order_line
        return None
    
    def _get_product(self,id, env):
        return env['product.product'].search([('prestashop_id', '=', id)],limit=1)


    def _get_tax(self,id,env):
        tax = env['account.tax'].search([('prestashop_id', '=', id)],limit=1)
        if tax.exists():
            return [[6, False, [tax.id]]]
        else:
            return [[6, False, []]]