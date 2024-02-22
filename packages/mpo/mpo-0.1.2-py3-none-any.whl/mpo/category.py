from cleantxt import text

class CategoryMapper():

    lang = '1'

    def __init__(self,lang='1') -> None:
        self.lang = lang


    def to_odoo(self, prestashop, default, env):
        categ = {
            'name': prestashop['name'],
            'prestashop_id': prestashop['id'],
            'prestashop_description': prestashop['description']
        }

        if prestashop.get('id_parent'):
            categ['parent_id'] = self._get_parrent_id(
                prestashop['id_parent'], default, env, True)

        return categ

    def to_prestashop(self, odoo, default, env):
        categ = {
            'active': '1',
            'name': {
                'language': {
                    'attrs': {'id': self.lang},
                    'value': text.clean_text(odoo['name'], whitespace=False, do_lower=False, alphnum=False, accent=False, ascii=True),
                }
            },
            'link_rewrite': {
                'language': {
                    'attrs': {'id': self.lang},
                    'value': self._fix_for_url(odoo['name']),
                }
            },
        }

        if odoo.get('prestashop_description'):
            categ['description'] = {
                'language': {
                    'attrs': {'id': self.lang},
                    'value': odoo['prestashop_description'],
                }
            }

        if odoo.get('parent_id'):
            categ['id_parent'] = self._get_parrent_id(
                odoo['parent_id'], default, env, False)

        return {'category': categ}

    def _fix_for_url(self, txt):
        txt = text.clean_text(txt, do_lower=True, whitespace=False)
        txt = txt.replace(' ', '-')
        return txt

    def _get_parrent_id(self, id, default, env, odoo=False):

        if odoo:
            categ = env['product.category'].search([('prestashop_id', '=', id)])
            if categ.exists():
                return categ.id
            return None

        if isinstance(id,str) or isinstance(id,int):
            categ = env['product.category'].browse(id)
            if categ:
                return categ.prestashop_id
            return default
        elif isinstance(id,type(env['product.category'].browse(1))):
            return id.prestashop_id

        return default

