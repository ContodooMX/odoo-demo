# Script para agregar códigos EAN manualmente
# Ejecuta este script desde el shell de Odoo

# Productos a agregar:
productos_ean = [
    {
        'cliente': 'Deco Addict',
        'producto_code': 'FURN_1118',
        'ean': 'FURN1118',
        'nombre': 'Escritorio de esquina'
    },
    {
        'cliente': 'Deco Addict',
        'producto_code': 'E-COM12',
        'ean': 'SILLA_CONF_ACERO',
        'nombre': 'Silla de conferencia acero'
    },
]

# Buscar y crear los códigos
for item in productos_ean:
    # Buscar cliente
    partner = env['res.partner'].search([('name', '=', item['cliente'])], limit=1)
    if not partner:
        print(f"Cliente '{item['cliente']}' no encontrado")
        continue
    
    # Buscar producto por código
    product = env['product.product'].search([('default_code', '=', item['producto_code'])], limit=1)
    if not product:
        print(f"Producto '{item['producto_code']}' no encontrado")
        continue
    
    # Verificar si ya existe
    existing = env['product.customer.code'].search([
        ('partner_id', '=', partner.id),
        ('product_id', '=', product.id)
    ])
    
    if existing:
        print(f"Ya existe código EAN para {item['producto_code']} - {item['cliente']}: {existing.product_code}")
    else:
        # Crear nuevo código
        env['product.customer.code'].create({
            'partner_id': partner.id,
            'product_id': product.id,
            'product_code': item['ean'],
            'product_name': item['nombre']
        })
        print(f"✓ Creado código EAN: {item['ean']} para {item['producto_code']}")

print("\n¡Listo! Códigos EAN agregados.")
