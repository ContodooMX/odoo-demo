{
    'name': 'NEDI Methodology',
    'version': '19.0.1.0.0',
    'category': 'Services/Project',
    'summary': 'Metodología NEDI 2026 para implementaciones de Odoo',
    'description': """
        Addon para gestionar proyectos de implementación de Odoo.
        - Gestión de proyectos
        - Cuestionarios de discovery
        - Procesos AS-IS
        - Catálogo de módulos
        - GAP Analysis
        - Generador de plan de trabajo
        - Reportes PDF
        - Dashboard
    """,
    'author': 'NEDI',
    'website': 'https://www.nedi.mx',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'project',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/methodology_questionnaire_data.xml',
        'data/methodology_module_data.xml',
        'data/methodology_task_template_data.xml',
        'views/methodology_menu.xml',
        'views/methodology_project_views.xml',
        'views/methodology_questionnaire_views.xml',
        'views/methodology_asis_views.xml',
        'views/methodology_module_views.xml',
        'views/methodology_gap_views.xml',
        'views/methodology_task_template_views.xml',
        'wizards/wizard_views.xml',
        'reports/report_templates.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
