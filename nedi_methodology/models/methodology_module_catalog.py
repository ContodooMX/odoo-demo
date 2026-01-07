from odoo import models, fields

class MethodologyModuleCatalog(models.Model):
    _name = 'methodology.module.catalog'
    _description = 'Catálogo de Módulos Odoo'
    _order = 'business_process, sequence, name'

    name = fields.Char(string='Nombre', required=True)
    technical_name = fields.Char(string='Nombre Técnico', required=True)
    business_process = fields.Selection([
        ('scm', 'SCM - Cadena de Suministro'),
        ('sls', 'SLS - Ventas'),
        ('svc', 'SVC - Servicios'),
        ('mfg', 'MFG - Manufactura'),
        ('hrm', 'HRM - Recursos Humanos'),
        ('fin', 'FIN - Finanzas'),
    ], string='Proceso de Negocio', required=True)
    functional_area = fields.Char(string='Área Funcional')
    description = fields.Text(string='Descripción')
    estimated_hours = fields.Float(string='Horas Estimadas')
    is_base = fields.Boolean(string='Es Base')
    odoo_edition = fields.Selection([
        ('community', 'Community'),
        ('enterprise', 'Enterprise'),
        ('both', 'Ambas'),
    ], string='Edición', default='both')
    sequence = fields.Integer(string='Secuencia', default=10)
    active = fields.Boolean(string='Activo', default=True)
