from odoo import models, fields, api

class MethodologyQuestionnaire(models.Model):
    _name = 'methodology.questionnaire'
    _description = 'Cuestionario Aplicado'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre', compute='_compute_name', store=True)
    project_id = fields.Many2one('methodology.project', string='Proyecto', required=True, ondelete='cascade')
    template_id = fields.Many2one('methodology.questionnaire.template', string='Plantilla', required=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('in_progress', 'En Progreso'),
        ('completed', 'Completado'),
    ], string='Estado', default='draft', tracking=True)
    date_started = fields.Datetime(string='Fecha Inicio')
    date_completed = fields.Datetime(string='Fecha Completado')
    completed_by = fields.Many2one('res.users', string='Completado Por')
    answer_ids = fields.One2many('methodology.answer', 'questionnaire_id', string='Respuestas')
    progress = fields.Float(string='Progreso', compute='_compute_progress', store=True)

    @api.depends('template_id', 'project_id')
    def _compute_name(self):
        for record in self:
            if record.template_id and record.project_id:
                record.name = f"{record.project_id.name} - {record.template_id.name}"
            else:
                record.name = "Nuevo Cuestionario"

    @api.depends('answer_ids.value_boolean', 'answer_ids.value_text', 'answer_ids.value_selection', 'answer_ids.value_integer')
    def _compute_progress(self):
        for record in self:
            total = len(record.template_id.question_ids) if record.template_id else 0
            if total:
                answered = len(record.answer_ids.filtered(lambda a: a.value_boolean or a.value_selection or a.value_text or a.value_integer))
                record.progress = (answered / total) * 100
            else:
                record.progress = 0

    def action_start(self):
        self.write({'state': 'in_progress', 'date_started': fields.Datetime.now()})
        for question in self.template_id.question_ids:
            self.env['methodology.answer'].create({
                'questionnaire_id': self.id,
                'question_id': question.id,
            })

    def action_complete(self):
        self.write({'state': 'completed', 'date_completed': fields.Datetime.now(), 'completed_by': self.env.user.id})

    def action_reset(self):
        self.write({'state': 'draft'})
        self.answer_ids.unlink()
