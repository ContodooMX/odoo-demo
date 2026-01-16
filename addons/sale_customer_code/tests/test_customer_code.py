from odoo.tests.common import TransactionCase
from odoo import Command

class TestCustomerCode(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'Test Partner'})
        cls.product = cls.env['product.product'].create({'name': 'Test Product', 'list_price': 100.0})
        cls.customer_code = cls.env['product.customer.code'].create({
            'partner_id': cls.partner.id,
            'product_id': cls.product.id,
            'product_code': 'EAN123456',
            'product_name': 'Test Product Customer Name'
        })
        cls.SaleOrder = cls.env['sale.order']

    def test_customer_code_onchange(self):
        """Test that the customer code is automatically populated on Sale Order Line"""
        sale_order = self.SaleOrder.create({
            'partner_id': self.partner.id,
        })
        
        # Simulate creating a line with the product
        # The _onchange_product_customer_code should be triggered if we use Form view simulation or manually call it
        # But since we are backend testing without Form(), we rely on the create/write mechanics if 'compute' is triggered
        # The field is computed with @api.depends or onchange.
        
        # Let's verify the compute logic first
        line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'product_id': self.product.id,
        })
        
        # Force recompute or check if it was computed on create
        # Use _compute_customer_product_code if it's not stored or if it didn't trigger
        # The field definition says: compute='_compute_customer_product_code', store=True
        
        self.assertEqual(line.customer_product_code, 'EAN123456', "Customer Code should be populated automatically")
        
    def test_customer_code_update(self):
        """Test changing product updates the code"""
        sale_order = self.SaleOrder.create({
            'partner_id': self.partner.id,
        })
        line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'product_id': self.product.id,
        })
        self.assertEqual(line.customer_product_code, 'EAN123456')
        
        # Create another product without code
        product2 = self.env['product.product'].create({'name': 'Product 2'})
        
        line.product_id = product2
        # Since it is stored and computed, we might need to trigger recomputation or it happens automatically due to dependency
        line._compute_customer_product_code()
        
        self.assertFalse(line.customer_product_code, "Customer Code should be cleared for product without code")
