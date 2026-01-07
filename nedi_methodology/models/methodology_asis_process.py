from odoo import models, fields, api

class MethodologyAsisProcess(models.Model):
    _name = 'methodology.asis.process'
    _description = 'Proceso AS-IS'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'

    name = fields.Char(string='Nombre del Proceso', required=True, tracking=True)
    code = fields.Char(string='Código')
    project_id = fields.Many2one('methodology.project', string='Proyecto', required=True, ondelete='cascade')
    business_process = fields.Selection([
        ('scm', 'SCM - Cadena de Suministro'),
        ('sls', 'SLS - Ventas'),
        ('svc', 'SVC - Servicios'),
        ('mfg', 'MFG - Manufactura'),
        ('hrm', 'HRM - Recursos Humanos'),
        ('fin', 'FIN - Finanzas'),
    ], string='Proceso de Negocio', required=True)
    functional_area = fields.Char(string='Área Funcional')
    description = fields.Text(string='Descripción General')
    frequency = fields.Selection([
        ('daily', 'Diario'),
        ('weekly', 'Semanal'),
        ('monthly', 'Mensual'),
        ('eventual', 'Eventual'),
    ], string='Frecuencia', default='daily')
    volume_monthly = fields.Integer(string='Volumen Mensual')
    trigger = fields.Text(string='¿Qué inicia el proceso?', required=True)
    systems_used = fields.Text(string='Sistemas Actuales')
    pain_points = fields.Text(string='Problemas / Puntos de Dolor', required=True)
    documents_generated = fields.Text(string='Documentos que Genera')
    criticality = fields.Selection([
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('critical', 'Crítica'),
    ], string='Criticidad', default='medium', tracking=True)
    responsible_id = fields.Many2one('res.partner', string='Responsable')
    step_ids = fields.One2many('methodology.asis.step', 'process_id', string='Pasos del Proceso')
    step_count = fields.Integer(compute='_compute_step_count')
    sequence = fields.Integer(string='Secuencia', default=10)

    @api.depends('step_ids')
    def _compute_step_count(self):
        for record in self:
            record.step_count = len(record.step_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code'):
                # Handle possible missing keys or batching manually if needed, 
                # though here we just need to ensure we don't access vals as a list
                project_id = vals.get('project_id')
                if project_id:
                    count = self.search_count([('project_id', '=', project_id)])
                    vals['code'] = f"ASIS-{count + 1:03d}"
        return super().create(vals_list)
