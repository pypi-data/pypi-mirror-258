from cleantxt import text

# prestashop type (simple,virtual,pack)
# odoo type (service,consu, product)

# virtual => service
# simple,pack => product

class ProductMapper():

    lang = '1'

    def __init__(self,lang='1') -> None:
        self.lang = lang

    def to_odoo(self, prestashop, env):

        details_type = 'product'

        if prestashop['type'] == 'virtual':
            details_type = 'service'


        record = env['product.category'].search(
            [('prestashop_id', '=', prestashop['id_category_default'])], limit=1)

        if record.exists():
            categ_id = record.id
        else:
            return (None,None,None,None)

        odoo_product = {
            "prestashop_id": prestashop['id'],
            "type": details_type,
            "name": prestashop['name'],
            "detailed_type": details_type,
            "list_price": prestashop['price'],
            "categ_id": categ_id,
            "description": prestashop['description'],
            "qty_available" : prestashop['quantity'],
            "short_description" : prestashop['description_short'],
            "default_code" : prestashop['reference'],
        }

        if prestashop['ean13']:
            odoo_product['barcode'] = prestashop['ean13']

        if prestashop['available_for_order'] == "1":
            odoo_product['available_in_pos'] = True
        

        option_values = []
        images = []
        combinations = []

        if 'associations' in prestashop:

            if 'product_option_values' in prestashop['associations']:
                option_values = prestashop['associations']['product_option_values']

            if 'combinations'  in prestashop['associations']:
                combinations = prestashop['associations']['combinations']

            if 'images' in prestashop['associations']:
                images = prestashop['associations']['images']

        re = (odoo_product,option_values,images,combinations)

        return re

    def to_prestashop(self, odoo,values=None,write=False,categ_id=None):

        presta_type = 'simple'
        product_type = odoo['detailed_type']
        name = ""

        if product_type == 'service':
            presta_type = 'virtual'
        
        if write :
            if values.get('categ_id'):
                c = odoo.env['product.category'].browse(values['categ_id'])
                categ = c.prestashop_id
            else:
                categ = odoo.categ_id.prestashop_id

            if values.get('name'):
                name = values['name']
            else:
                name = odoo['name']

            
        else:
            categ = categ_id

        presta_product = {
            'product': {
                'active': '1',
                'state': '1',
                'show_price' : "1",
                'name': {'language': {
                    'attrs': {'id': self.lang},
                    'value': name,
                }},

                'link_rewrite': {'language': {
                    'attrs': {'id': self.lang},
                    'value': self._fix_for_url(name),
                }},
                'type': presta_type,
                'id_category_default': categ,
                'available_for_order' : "1",
                'minimal_quantity' : "1",
                'redirect_type': "301-category",

            }
        }

        if write:

            if values.get('barcode'):
                presta_product['product']['ean13'] = values['barcode']
            elif odoo.barcode:
                presta_product['product']['ean13'] = odoo['barcode']
            

            if values.get('list_price'):
                presta_product['product']['price'] = values['list_price']
            elif odoo.list_price:
                presta_product['product']['price'] = odoo['list_price']

            if values.get('description'):
                presta_product['product']['description'] = {'language': {
                    'attrs': {'id': self.lang},
                    'value': values['description'],
                },
                }
            elif odoo.description:
                presta_product['product']['description'] = {'language': {
                    'attrs': {'id': self.lang},
                    'value': odoo['description'],
                },
                }
            
            if values.get('available_in_pos'):
                presta_product['product']['available_for_order']  = "1"
            elif odoo.available_in_pos:
                presta_product['product']['available_for_order']  = "1"

            if values.get('short_description'):
                presta_product['product']['description_short']  = values['short_description']
            elif odoo.short_description:
                presta_product['product']['description_short']  = odoo.short_description
            
            if values.get('default_code'):
                presta_product['product']['reference']  = values['default_code']
            elif odoo.default_code:
                presta_product['product']['reference']  = odoo.default_code

        else:
            if odoo.get('barcode'):
                presta_product['product']['ean13'] = odoo['barcode']
            
            if odoo.get('list_price'):
                presta_product['product']['price'] = odoo['list_price']
        
            if odoo.get('description'):
                presta_product['product']['description'] = {'language': {
                    'attrs': {'id': self.lang},
                    'value': odoo['description'],
                },
                }
            
            if odoo.get('available_in_pos'):
                presta_product['product']['available_for_order']  = "1"

            
            if odoo.get('short_description'):
                presta_product['product']['description_short']  = odoo['short_description']
            
            if odoo.get('default_code'):
                presta_product['product']['reference']  = odoo['default_code']

        # associations

        # product categories

        presta_product['product']['associations'] = {'categories': []}

        presta_product['product']['associations']['categories'].append({
            'category':   {'id': categ},
        })

        if write:

            return presta_product['product']
        
        return presta_product

    def add_option_line(self, values, env):
        # values = {'product_attribute_value_id': 1, 'attribute_line_id': 71}

        attrib_line = env['product.template.attribute.line'].browse(values['attribute_line_id'])
        attrib_value = env['product.attribute.value'].browse(values['product_attribute_value_id'])


        if attrib_line.exists() and attrib_value.exists():

            id_product = attrib_line.product_tmpl_id.prestashop_id
            attribute_value_id = attrib_value.prestashop_id

            return {
                'combination': {
                    'id_product': id_product,
                    'minimal_quantity': '1',
                    'associations': {'product_option_values': {'product_option_value' : {'id': attribute_value_id} } },  # noqa: E501
                }
            }



        return None

    def _fix_for_url(self, txt):
        txt = text.clean_text(txt, do_lower=True, whitespace=False)
        txt = txt.replace(' ', '-')
        return txt

