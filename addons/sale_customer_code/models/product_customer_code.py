from odoo import models, fields, api

class ProductCustomerCode(models.Model):
    _name = 'product.customer.code'
    _description = 'Customer Product Code'
    _rec_name = 'product_code'

    partner_id = fields.Many2one('res.partner', string='Customer', required=False)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_code = fields.Char(string='Customer Code', required=True)
    product_name = fields.Char(string='Customer Product Name')
    
    _sql_constraints = [
        ('uniq_partner_product', 'unique(partner_id, product_id)', 'This product already has a code for this customer.')
    ]

    @api.constrains('partner_id', 'product_id')
    def _check_unique_generic_code(self):
        for record in self:
            if not record.partner_id:
                domain = [
                    ('partner_id', '=', False),
                    ('product_id', '=', record.product_id.id),
                    ('id', '!=', record.id)
                ]
                if self.search_count(domain) > 0:
                    raise models.ValidationError("This product already has a generic code.")
