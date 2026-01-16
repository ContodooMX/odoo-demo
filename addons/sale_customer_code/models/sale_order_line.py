from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    customer_product_code = fields.Char(
        string="CÓDIGO EAN",
        compute='_compute_customer_product_code',
        store=True,
        readonly=False,
        copy=False
    )

    @api.depends('order_id.partner_id', 'product_id')
    def _compute_customer_product_code(self):
        """Compute customer product code when partner or product changes"""
        for line in self:
            if line.order_id.partner_id and line.product_id:
                code_record = self.env['product.customer.code'].search([
                    ('partner_id', '=', line.order_id.partner_id.id),
                    ('product_id', '=', line.product_id.id)
                ], limit=1)
                line.customer_product_code = code_record.product_code if code_record else False
            else:
                line.customer_product_code = False

    @api.onchange('product_id')
    def _onchange_product_id_customer_code(self):
        """Auto-fill customer product code when product is selected"""
        if self.order_id.partner_id and self.product_id:
            code_record = self.env['product.customer.code'].search([
                ('partner_id', '=', self.order_id.partner_id.id),
                ('product_id', '=', self.product_id.id)
            ], limit=1)
            self.customer_product_code = code_record.product_code if code_record else False
        else:
            self.customer_product_code = False
