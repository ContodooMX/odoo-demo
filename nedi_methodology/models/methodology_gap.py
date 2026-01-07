from odoo import models, fields, api

class MethodologyGap(models.Model):
    _name = 'methodology.gap'
    _description = 'Brecha (GAP)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority_order, sequence, id'

    name = fields.Char(string='Descripción', required=True, tracking=True)
    code = fields.Char(string='Código', readonly=True, copy=False)
    project_id = fields.Many2one('methodology.project', string='Proyecto', required=True, ondelete='cascade')
    asis_process_id = fields.Many2one('methodology.asis.process', string='Proceso AS-IS', domain="[('project_id', '=', project_id)]")
    gap_type = fields.Selection([
        ('standard', 'Estándar - Odoo lo tiene'),
        ('config_advanced', 'Configuración Avanzada'),
        ('process_change', 'Cambio de Proceso'),
        ('dev_minor', 'Desarrollo Menor (1-5 días)'),
        ('dev_major', 'Desarrollo Mayor (1-4 semanas)'),
        ('integration', 'Integración Externa'),
        ('not_feasible', 'No Factible'),
    ], string='Tipo de GAP', required=True, tracking=True)
    priority = fields.Selection([
        ('blocker', 'Bloqueante'),
        ('high', 'Alta'),
        ('medium', 'Media'),
        ('low', 'Baja'),
    ], string='Prioridad', default='medium', tracking=True)
    priority_order = fields.Integer(compute='_compute_priority_order', store=True)
    state = fields.Selection([
        ('identified', 'Identificado'),
        ('analyzing', 'En Análisis'),
        ('decided', 'Decidido'),
        ('resolved', 'Resuelto'),
    ], string='Estado', default='identified', tracking=True)
    estimated_hours = fields.Float(string='Horas Estimadas')
    strategy = fields.Text(string='Estrategia Propuesta')
    decision = fields.Text(string='Decisión Tomada')
    decision_rationale = fields.Text(string='Justificación')
    responsible_id = fields.Many2one('res.users', string='Responsable')
    sequence = fields.Integer(string='Secuencia', default=10)

    @api.depends('priority')
    def _compute_priority_order(self):
        priority_map = {'blocker': 1, 'high': 2, 'medium': 3, 'low': 4}
        for record in self:
            record.priority_order = priority_map.get(record.priority, 5)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('methodology.gap') or 'GAP-001'
        return super().create(vals_list)

    def action_analyze(self):
        self.write({'state': 'analyzing'})

    def action_decide(self):
        self.write({'state': 'decided'})

    def action_resolve(self):
        self.write({'state': 'resolved'})

    def action_reset(self):
        self.write({'state': 'identified'})
