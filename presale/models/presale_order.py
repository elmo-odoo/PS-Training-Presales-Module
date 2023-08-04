from odoo import api, fields, models


class PresaleOrder(models.Model):
    _name = 'presale.order'
    _description = 'Presales Orders'

    name = fields.Char(string='Preorder Reference',
                       required=True, copy=False, readonly=True,
                       default='New')

    active = fields.Boolean('Active', default=True)

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed')
        ],
        string='Status',
        readonly=True, copy=False,
        default='draft'
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",
        required=True, readonly=False, change_default=True)

    order_line_ids = fields.One2many('presale.order.line', 'order_id', string='Order Lines')

    sale_order_id = fields.Many2one('sale.order', string='Sale Order', copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', "New") == "New":
                vals['name'] = self.env['ir.sequence'].next_by_code('presale.order') or "New"

        return super().create(vals_list)

    def validate_action(self):
        for record in self:
            SaleOrder = self.env['sale.order']

            # Create sale order
            sale_order_line_vals = [
                (0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'price_unit': line.price,
                })
                for line in self.order_line_ids
            ]

            sale_order_vals = {
                'partner_id': self.partner_id.id,
                'presale_order_id': self.id,
                'order_line': sale_order_line_vals,
            }

            sale_order = SaleOrder.create(sale_order_vals)

            # Confirm the sale order
            sale_order.action_confirm()

            # Update stage and link presale order to sale order
            record.write(
                {'state': 'confirmed', 'sale_order_id': sale_order.id})

            # Send email to pre-order creator
            template = template = self.env.ref('presale.email_template_presale')
            template.send_mail(record.id, force_send=True)

        return True

    @api.model
    def archive_confirmed_presale_orders(self):
        confirmed_orders = self.search([('state', '=', 'confirmed')])
        confirmed_orders.write({'active': False})
