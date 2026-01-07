from odoo import models, fields, api

class MethodologyQuestionnaireTemplate(models.Model):
    _name = 'methodology.questionnaire.template'
    _description = 'Plantilla de Cuestionario'
    _order = 'sequence, id'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código', required=True)
    description = fields.Text(string='Descripción')
    business_process = fields.Selection([
        ('scm', 'SCM - Cadena de Suministro'),
        ('sls', 'SLS - Ventas'),
        ('svc', 'SVC - Servicios'),
        ('mfg', 'MFG - Manufactura'),
        ('hrm', 'HRM - Recursos Humanos'),
        ('fin', 'FIN - Finanzas'),
    ], string='Proceso de Negocio', required=True)
    sequence = fields.Integer(string='Secuencia', default=10)
    active = fields.Boolean(string='Activo', default=True)
    question_ids = fields.One2many('methodology.question.template', 'questionnaire_template_id', string='Preguntas')
    industry_ids = fields.Many2many('res.partner.industry', string='Industrias Aplicables', help='Dejar vacío si aplica a todas')
    question_count = fields.Integer(compute='_compute_question_count')

    @api.depends('question_ids')
    def _compute_question_count(self):
        for record in self:
            record.question_count = len(record.question_ids)
