import sys
from odoo import api, SUPERUSER_ID

def run_verification(env):
    print("starting verification...")
    Product = env['product.product']
    Partner = env['res.partner']
    Code = env['product.customer.code']
    SaleOrder = env['sale.order']
    SaleLine = env['sale.order.line']

    # 1. Setup Data
    print("Setting up data...")
    product = Product.create({'name': 'Test Product Apple'})
    partner_specific = Partner.create({'name': 'Specific Customer'})
    partner_random = Partner.create({'name': 'Random Customer'})
    
    # Create Generic Code
    Code.create({
        'product_id': product.id,
        'partner_id': False,
        'product_code': 'APP-GENERIC'
    })
    
    # Create Specific Code
    Code.create({
        'product_id': product.id,
        'partner_id': partner_specific.id,
        'product_code': 'APP-SPECIFIC'
    })
    
    print("Data created.")

    # 2. Test Generic Scenario
    print("Testing Generic Scenario (Random Customer)...")
    so_generic = SaleOrder.create({'partner_id': partner_random.id})
    sol_generic = SaleLine.new({
        'order_id': so_generic,
        'product_id': product
    })
    sol_generic._onchange_product_id_customer_code()
    print(f"Generic Result: {sol_generic.customer_product_code}")
    
    if sol_generic.customer_product_code == 'APP-GENERIC':
        print("PASS: Generic code correctly applied.")
    else:
        print(f"FAIL: Expected APP-GENERIC, got {sol_generic.customer_product_code}")

    # 3. Test Specific Scenario
    print("Testing Specific Scenario (Specific Customer)...")
    so_specific = SaleOrder.create({'partner_id': partner_specific.id})
    sol_specific = SaleLine.new({
        'order_id': so_specific,
        'product_id': product
    })
    # Manually trigger onchange since 'new' records don't automatically trigger it the same way as UI
    sol_specific._onchange_product_id_customer_code()
    print(f"Specific Result: {sol_specific.customer_product_code}")

    if sol_specific.customer_product_code == 'APP-SPECIFIC':
        print("PASS: Specific code correctly applied.")
    else:
        print(f"FAIL: Expected APP-SPECIFIC, got {sol_specific.customer_product_code}")
        
    # 4. Cleanup (Rollback to avoid polluting DB)
    env.cr.rollback()
    print("Rollback successful. Verification complete.")

if __name__ == '__main__':
    # This block is executed when running via odoo-bin shell
    # The 'env' variable is automatically available in the shell context
    try:
        run_verification(env)
    except Exception as e:
        print(f"Error during verification: {e}")
        import traceback
        traceback.print_exc()

