from odoo import models, fields

class MethodologyTaskTemplate(models.Model):
    _name = 'methodology.task.template'
    _description = 'Template de Tarea'
    _order = 'phase, sequence, id'

    name = fields.Char(string='Nombre de Tarea', required=True)
    module_id = fields.Many2one('methodology.module.catalog', string='Módulo')
    phase = fields.Selection([
        ('phase_0', 'Fase 0 - Familiarización'),
        ('phase_1', 'Fase 1 - Descubrimiento'),
        ('phase_2', 'Fase 2 - Implementación'),
        ('phase_3', 'Fase 3 - Optimización'),
        ('phase_4', 'Fase 4 - Cierre'),
    ], string='Fase', required=True)
    task_type = fields.Selection([
        ('config', 'Configuración'),
        ('migration', 'Migración de Datos'),
        ('training', 'Capacitación'),
        ('uat', 'Pruebas UAT'),
        ('doc', 'Documentación'),
        ('support', 'Soporte'),
    ], string='Tipo', default='config')
    estimated_hours = fields.Float(string='Horas Estimadas', required=True)
    description = fields.Text(string='Descripción')
    sequence = fields.Integer(string='Secuencia', default=10)
    active = fields.Boolean(string='Activo', default=True)
