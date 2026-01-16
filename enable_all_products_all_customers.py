#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para habilitar TODOS los productos para TODOS los clientes
"""

import sys
import os

# Agregar path de Odoo
odoo_path = r'c:\Users\alber\PycharmProjects\odoo19\odoo'
sys.path.insert(0, odoo_path)

# Configurar Odoo
os.chdir(r'c:\Users\alber\PycharmProjects\odoo19')

import odoo
from odoo.api import Environment

# Cargar configuración
odoo.tools.config.parse_config(['-c', 'odoo.conf', '--addons-path', 'odoo/addons,enterprise,addons'])

db_name = 'odoo19_v16'

print("="*80)
print("HABILITANDO TODOS LOS PRODUCTOS PARA TODOS LOS CLIENTES")
print("="*80)

# Inicializar registry
from odoo.modules.registry import Registry
registry = Registry(db_name)

with registry.cursor() as cr:
    uid = odoo.SUPERUSER_ID
    ctx = {}
    env = Environment(cr, uid, ctx)
    
    print("\n1. Obteniendo productos con códigos EAN...")
    existing_codes = env['product.customer.code'].search([])
    
    # Crear diccionario de productos únicos
    product_codes = {}
    for code in existing_codes:
        if code.product_id.id not in product_codes:
            product_codes[code.product_id.id] = {
                'code': code.product_code,
                'name': code.product_name or code.product_id.name
            }
    
    print(f"   ✓ Encontrados {len(product_codes)} productos únicos")
    
    print("\n2. Obteniendo todos los clientes...")
    all_customers = env['res.partner'].search([
        ('customer_rank', '>', 0),
        ('is_company', '=', True)
    ])
    print(f"   ✓ Encontrados {len(all_customers)} clientes")
    
    print("\n3. Creando registros...")
    created = 0
    skipped = 0
    
    for customer in all_customers:
        for product_id, product_data in product_codes.items():
            existing = env['product.customer.code'].search([
                ('partner_id', '=', customer.id),
                ('product_id', '=', product_id)
            ], limit=1)
            
            if not existing:
                env['product.customer.code'].create({
                    'partner_id': customer.id,
                    'product_id': product_id,
                    'product_code': product_data['code'],
                    'product_name': product_data['name']
                })
                created += 1
                if created % 50 == 0:
                    print(f"   Creados {created} registros...")
                    cr.commit()
            else:
                skipped += 1
    
    cr.commit()
    
    print(f"\n{'='*80}")
    print(f"RESUMEN:")
    print(f"{'='*80}")
    print(f"✓ Productos únicos: {len(product_codes)}")
    print(f"✓ Clientes totales: {len(all_customers)}")
    print(f"✓ Registros creados: {created}")
    print(f"✓ Registros existentes: {skipped}")
    print(f"{'='*80}")
    print(f"\n✓ COMPLETADO!\n")
