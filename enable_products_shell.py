import logging
_logger = logging.getLogger(__name__)

def enable_all_products():
    """Habilita todos los productos para todos los clientes"""
    from odoo import api, SUPERUSER_ID
    from odoo.modules.registry import Registry
    
    db_name = 'odoo19_v16'
    registry = Registry(db_name)
    
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        _logger.info("="*80)
        _logger.info("HABILITANDO TODOS LOS PRODUCTOS PARA TODOS LOS CLIENTES")
        _logger.info("="*80)
        
        # Obtener códigos existentes
        existing_codes = env['product.customer.code'].search([])
        
        # Productos únicos con sus códigos
        product_codes = {}
        for code in existing_codes:
            if code.product_id.id not in product_codes:
                product_codes[code.product_id.id] = {
                    'code': code.product_code,
                    'name': code.product_name or code.product_id.name
                }
        
        _logger.info(f"Productos únicos: {len(product_codes)}")
        
        # Obtener todos los clientes
        all_customers = env['res.partner'].search([('customer_rank', '>', 0)])
        _logger.info(f"Clientes totales: {len(all_customers)}")
        
        # Crear registros
        created = 0
        for customer in all_customers:
            for product_id, data in product_codes.items():
                existing = env['product.customer.code'].search([
                    ('partner_id', '=', customer.id),
                    ('product_id', '=', product_id)
                ], limit=1)
                
                if not existing:
                    env['product.customer.code'].create({
                        'partner_id': customer.id,
                        'product_id': product_id,
                        'product_code': data['code'],
                        'product_name': data['name']
                    })
                    created += 1
        
        cr.commit()
        _logger.info(f"Registros creados: {created}")
        _logger.info("COMPLETADO!")

enable_all_products()
