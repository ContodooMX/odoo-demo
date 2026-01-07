from odoo import models, fields
from datetime import timedelta

class WizardGenerateWorkplan(models.TransientModel):
    _name = 'methodology.generate.workplan.wizard'
    _description = 'Generar Plan de Trabajo'

    project_id = fields.Many2one('methodology.project', string='Proyecto', required=True)
    module_ids = fields.Many2many('methodology.module.catalog', 'methodology_wiz_mod_rel', 'wizard_id', 'module_id', string='Módulos a Implementar', required=True)
    start_date = fields.Date(string='Fecha de Inicio', required=True, default=fields.Date.today)
    include_base_tasks = fields.Boolean(string='Incluir tareas base', default=True)

    def action_generate(self):
        self.ensure_one()
        Project = self.env['project.project']
        project = Project.search([('name', '=', self.project_id.name)], limit=1)
        if not project:
            project = Project.create({
                'name': self.project_id.name,
                'partner_id': self.project_id.partner_id.id,
            })
        
        Task = self.env['project.task']
        TaskTemplate = self.env['methodology.task.template']
        current_date = self.start_date
        tasks_created = 0
        
        domain = [('module_id', 'in', self.module_ids.ids)]
        if self.include_base_tasks:
            domain = ['|', ('module_id', '=', False), ('module_id', 'in', self.module_ids.ids)]
        
        templates = TaskTemplate.search(domain, order='phase, sequence')
        
        for template in templates:
            hours = template.estimated_hours or 8
            days = max(1, int(hours / 8))
            Task.create({
                'name': f"[{template.phase}] {template.name}",
                'project_id': project.id,
                'allocated_hours': hours,
                'date_deadline': current_date + timedelta(days=days),
                'description': template.description or '',
            })
            tasks_created += 1
            current_date += timedelta(days=days)
        
        self.project_id.write({'project_id': project.id})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Plan de Trabajo Generado',
                'message': f'Se crearon {tasks_created} tareas.',
                'type': 'success',
            }
        }
