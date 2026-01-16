#!/usr/bin/env python3
"""
Script to test customer product code auto-population
Run this script to verify if customer codes exist and test the logic
"""

import sys
sys.path.insert(0, 'c:/Users/alber/PycharmProjects/odoo19/odoo')

import odoo
from odoo import api, SUPERUSER_ID

# Configuration
DB_NAME = 'odoo19_v16'
CONFIG_FILE = 'c:/Users/alber/PycharmProjects/odoo19/odoo.conf'

# Initialize Odoo
odoo.tools.config.parse_config(['-c', CONFIG_FILE])
odoo.cli.server.report_configuration()

# Connect to database
with odoo.api.Environment.manage():
    registry = odoo.registry(DB_NAME)
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        print("=" * 80)
        print("CHECKING CUSTOMER PRODUCT CODES")
        print("=" * 80)
        
        # Get all customer codes
        codes = env['product.customer.code'].search([])
        print(f"\nTotal customer codes found: {len(codes)}")
        
        if codes:
            print("\nFirst 10 customer codes:")
            print("-" * 80)
            for code in codes[:10]:
                partner_name = code.partner_id.name if code.partner_id else "N/A"
                product_name = code.product_id.name if code.product_id else "N/A"
                print(f"Customer: {partner_name}")
                print(f"Product: {product_name}")
                print(f"Code: {code.product_code}")
                print(f"Partner ID: {code.partner_id.id}, Product ID: {code.product_id.id}")
                print("-" * 80)
        else:
            print("\n⚠️  WARNING: No customer product codes found in database!")
            print("You need to create customer codes in: Sales → Configuration → Códigos de Producto por Cliente")
        
        print("\n" + "=" * 80)
        print("TESTING AUTO-POPULATION LOGIC")
        print("=" * 80)
        
        # Get a sample customer and product
        partner = env['res.partner'].search([('customer_rank', '>', 0)], limit=1)
        product = env['product.product'].search([('sale_ok', '=', True)], limit=1)
        
        if partner and product:
            print(f"\nTest Customer: {partner.name} (ID: {partner.id})")
            print(f"Test Product: {product.name} (ID: {product.id})")
            
            # Check if a code exists for this combination
            test_code = env['product.customer.code'].search([
                ('partner_id', '=', partner.id),
                ('product_id', '=', product.id)
            ], limit=1)
            
            if test_code:
                print(f"✓ Customer code found: {test_code.product_code}")
            else:
                print("✗ No customer code found for this combination")
                print("  Creating a test code...")
                
                # Create a test code
                test_code = env['product.customer.code'].create({
                    'partner_id': partner.id,
                    'product_id': product.id,
                    'product_code': 'TEST-EAN-12345',
                    'product_name': 'Test Product Name'
                })
                print(f"✓ Test code created: {test_code.product_code}")
            
            cr.commit()
        else:
            print("\n⚠️  WARNING: Could not find test customer or product")
        
        print("\n" + "=" * 80)
        print("VERIFICATION COMPLETE")
        print("=" * 80)
