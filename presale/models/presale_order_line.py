from odoo import fields, models


class PresaleOrderLine(models.Model):
    _name = 'presale.order.line'
    _description = 'Presale Order Line'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    price = fields.Float(string='Price', required=True)
    order_id = fields.Many2one('presale.order', string='Presale Order', ondelete='cascade')
