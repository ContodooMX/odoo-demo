#!/usr/bin/env python3
import xmlrpc.client

# Conectar a Odoo vía XML-RPC
url = 'http://localhost:8070'
db = 'odoo19_v16'
username = 'oscar_vm1@tesch.edu.mx'  # Usuario admin
password = '12345'  # Contraseña admin de odoo.conf

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if not uid:
    print("ERROR: No se pudo autenticar")
    exit(1)

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

print("="*80)
print("HABILITANDO TODOS LOS PRODUCTOS PARA TODOS LOS CLIENTES")
print("="*80)

# 1. Obtener códigos existentes
print("\n1. Obteniendo productos con códigos...")
code_ids = models.execute_kw(db, uid, password,
    'product.customer.code', 'search', [[]])

codes = models.execute_kw(db, uid, password,
    'product.customer.code', 'read', [code_ids],
    {'fields': ['partner_id', 'product_id', 'product_code', 'product_name']})

# Crear diccionario de productos únicos
product_codes = {}
for code in codes:
    product_id = code['product_id'][0]
    if product_id not in product_codes:
        product_codes[product_id] = {
            'code': code['product_code'],
            'name': code['product_name'] or code['product_id'][1]
        }

print(f"   ✓ Encontrados {len(product_codes)} productos únicos")

# 2. Obtener todos los clientes
print("\n2. Obteniendo clientes...")
customer_ids = models.execute_kw(db, uid, password,
    'res.partner', 'search', [[['customer_rank', '>', 0]]])

print(f"   ✓ Encontrados {len(customer_ids)} clientes")

# 3. Crear registros
print("\n3. Creando registros...")
created = 0
skipped = 0

for customer_id in customer_ids:
    for product_id, data in product_codes.items():
        # Verificar si existe
        existing = models.execute_kw(db, uid, password,
            'product.customer.code', 'search', [[
                ['partner_id', '=', customer_id],
                ['product_id', '=', product_id]
            ]], {'limit': 1})
        
        if not existing:
            # Crear
            models.execute_kw(db, uid, password,
                'product.customer.code', 'create', [{
                    'partner_id': customer_id,
                    'product_id': product_id,
                    'product_code': data['code'],
                    'product_name': data['name']
                }])
            created += 1
            if created % 50 == 0:
                print(f"   Creados {created} registros...")
        else:
            skipped += 1

print(f"\n{'='*80}")
print(f"RESUMEN:")
print(f"{'='*80}")
print(f"✓ Productos únicos: {len(product_codes)}")
print(f"✓ Clientes totales: {len(customer_ids)}")
print(f"✓ Registros creados: {created}")
print(f"✓ Registros existentes: {skipped}")
print(f"{'='*80}")
print(f"\n✓ COMPLETADO! Todos los clientes ahora tienen todos los productos.\n")
