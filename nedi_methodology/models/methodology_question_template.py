from odoo import models, fields

class MethodologyQuestionTemplate(models.Model):
    _name = 'methodology.question.template'
    _description = 'Pregunta de Cuestionario'
    _order = 'sequence, id'

    questionnaire_template_id = fields.Many2one('methodology.questionnaire.template', string='Cuestionario', required=True, ondelete='cascade')
    name = fields.Char(string='Pregunta', required=True)
    code = fields.Char(string='Código')
    question_type = fields.Selection([
        ('boolean', 'Sí/No'),
        ('selection', 'Selección'),
        ('text', 'Texto'),
        ('integer', 'Número'),
    ], string='Tipo', required=True, default='boolean')
    selection_options = fields.Text(string='Opciones')
    help_text = fields.Text(string='Texto de Ayuda')
    sequence = fields.Integer(string='Secuencia', default=10)
    is_required = fields.Boolean(string='Obligatoria')
    functional_area = fields.Char(string='Área Funcional')
