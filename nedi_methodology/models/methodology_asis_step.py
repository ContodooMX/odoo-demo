from odoo import models, fields

class MethodologyAsisStep(models.Model):
    _name = 'methodology.asis.step'
    _description = 'Paso de Proceso AS-IS'
    _order = 'sequence, id'

    process_id = fields.Many2one('methodology.asis.process', string='Proceso', required=True, ondelete='cascade')
    sequence = fields.Integer(string='#', default=10)
    name = fields.Char(string='Descripción del Paso', required=True)
    responsible = fields.Char(string='Responsable')
    tool_used = fields.Char(string='Herramienta')
    duration_minutes = fields.Integer(string='Duración (min)')
    is_approval = fields.Boolean(string='¿Es Aprobación?')
    pain_point = fields.Text(string='Problema de este paso')
