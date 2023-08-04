from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    presale_order_id = fields.Many2one('presale.order', string='Presale Order' , readonly=True)
