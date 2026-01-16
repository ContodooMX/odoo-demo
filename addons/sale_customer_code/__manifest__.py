{
    'name': 'Customer Product Codes',
    'version': '19.0.1.0.0',
    'summary': 'Add customer specific product codes to sale orders',
    'category': 'Sales',
    'author': 'Antigravity',
    'depends': ['sale_management', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/product_customer_code_data.xml',
        'views/product_customer_code_views.xml',
        'views/sale_order_views.xml',
        'views/report_sale_order.xml',
    ],
    'installable': True,
    'application': False,
}
