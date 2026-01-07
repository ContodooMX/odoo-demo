from odoo import models, fields

class MethodologyAnswer(models.Model):
    _name = 'methodology.answer'
    _description = 'Respuesta de Cuestionario'

    questionnaire_id = fields.Many2one('methodology.questionnaire', string='Cuestionario', required=True, ondelete='cascade')
    question_id = fields.Many2one('methodology.question.template', string='Pregunta', required=True)
    question_text = fields.Char(related='question_id.name', string='Pregunta', store=True)
    question_type = fields.Selection(related='question_id.question_type', string='Tipo', store=True)
    value_boolean = fields.Boolean(string='Respuesta Sí/No')
    value_selection = fields.Char(string='Respuesta Selección')
    value_text = fields.Text(string='Respuesta Texto')
    value_integer = fields.Integer(string='Respuesta Número')
    notes = fields.Text(string='Notas')
