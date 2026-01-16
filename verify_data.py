#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

odoo_path = r'c:\Users\alber\PycharmProjects\odoo19\odoo'
sys.path.insert(0, odoo_path)
os.chdir(r'c:\Users\alber\PycharmProjects\odoo19')

import odoo
odoo.tools.config.parse_config(['-c', 'odoo.conf', '--addons-path', 'odoo/addons,enterprise,addons'])

from odoo.modules.registry import Registry
from odoo.api import Environment

db_name = 'odoo19_v16'
registry = Registry(db_name)

with registry.cursor() as cr:
    env = Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("VERIFICANDO DATOS...")
    print("="*80)
    
    # Verificar códigos existentes
    codes = env['product.customer.code'].search([])
    print(f"\n1. Códigos de cliente existentes: {len(codes)}")
    for code in codes[:5]:
        print(f"   - {code.partner_id.name}: {code.product_id.name} = {code.product_code}")
    
    # Verificar clientes
    customers = env['res.partner'].search([('customer_rank', '>', 0)])
    print(f"\n2. Clientes totales: {len(customers)}")
    for customer in customers[:5]:
        print(f"   - {customer.name}")
    
    # Verificar productos
    products = env['product.product'].search([], limit=5)
    print(f"\n3. Productos (muestra):")
    for product in products:
        print(f"   - {product.name}")
    
    print("\n" + "="*80)
