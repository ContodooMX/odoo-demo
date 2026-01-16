#!/usr/bin/env python3
"""
Script para obtener UUIDs de facturas desde Odoo
Ejecutar desde la carpeta de Odoo
"""

import sys
import os

# Agregar el path de Odoo
sys.path.insert(0, os.path.dirname(__file__))

try:
    import odoo
    from odoo import api, SUPERUSER_ID
    
    # Configurar Odoo
    odoo.tools.config.parse_config(['-c', 'odoo.conf'])
    
    # Conectar a la base de datos
    db_name = odoo.tools.config['db_name']
    
    with api.Environment.manage():
        registry = odoo.registry(db_name)
        with registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            
            print("=" * 80)
            print("FACTURAS CON UUID DISPONIBLES")
            print("=" * 80)
            print()
            
            # Buscar facturas publicadas con UUID
            invoices = env['account.move'].search([
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('l10n_mx_edi_cfdi_uuid', '!=', False)
            ], limit=10, order='invoice_date desc')
            
            if not invoices:
                print("❌ No se encontraron facturas con UUID")
                print()
                print("Buscando facturas publicadas sin UUID...")
                invoices = env['account.move'].search([
                    ('move_type', '=', 'out_invoice'),
                    ('state', '=', 'posted')
                ], limit=10, order='invoice_date desc')
            
            print(f"Encontradas {len(invoices)} facturas:")
            print()
            
            for inv in invoices:
                uuid = inv.l10n_mx_edi_cfdi_uuid or "SIN UUID"
                print(f"Factura: {inv.name}")
                print(f"  Cliente: {inv.partner_id.name}")
                print(f"  Total: ${inv.amount_total:,.2f}")
                print(f"  Saldo: ${inv.amount_residual:,.2f}")
                print(f"  UUID: {uuid}")
                print()
            
            print("=" * 80)
            print("SELECCIONA 2 FACTURAS PARA LA PRUEBA")
            print("=" * 80)
            print()
            print("Copia los UUIDs de 2 facturas que quieras usar para la prueba.")
            print()
            
except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("Alternativa: Ejecutar consulta SQL directamente")
    print()
    print("psql -U odoo -d nombre_base_datos -c \"")
    print("SELECT name, partner_id, amount_total, amount_residual, l10n_mx_edi_cfdi_uuid")
    print("FROM account_move")
    print("WHERE move_type = 'out_invoice' AND state = 'posted'")
    print("ORDER BY invoice_date DESC LIMIT 10;\"")
