from odoo import models, fields, api

class MethodologyProject(models.Model):
    _name = 'methodology.project'
    _description = 'Proyecto de Implementación NEDI'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Nombre del Proyecto', required=True, tracking=True)
    code = fields.Char(string='Código', required=True, copy=False, default='Nuevo')
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True, tracking=True)
    
    date_start = fields.Date(string='Fecha de Inicio', default=fields.Date.today, tracking=True)
    date_end_planned = fields.Date(string='Fecha Fin Planificada')
    date_end_real = fields.Date(string='Fecha Fin Real')
    
    industry_id = fields.Many2one('res.partner.industry', string='Industria/Giro')
    company_size = fields.Selection([
        ('micro', 'Micro (1-10 empleados)'),
        ('small', 'Pequeña (11-50 empleados)'),
        ('medium', 'Mediana (51-200 empleados)'),
        ('large', 'Grande (200+ empleados)'),
    ], string='Tamaño de Empresa', default='small', tracking=True)
    employee_count = fields.Integer(string='Número de Empleados')
    
    hour_package = fields.Selection([
        ('h16', 'H16 - 16 horas'),
        ('h40', 'H40 - 40 horas'),
        ('h80', 'H80 - 80 horas'),
        ('h120', 'H120 - 120 horas'),
        ('h160', 'H160 - 160 horas'),
    ], string='Paquete de Horas', default='h80', required=True, tracking=True)
    hourly_rate = fields.Float(string='Tarifa por Hora', default=1000.0)
    
    phase = fields.Selection([
        ('phase_0', 'Fase 0 - Familiarización'),
        ('phase_1', 'Fase 1 - Descubrimiento'),
        ('phase_2', 'Fase 2 - Implementación MVP'),
        ('phase_3', 'Fase 3 - Optimización'),
        ('phase_4', 'Fase 4 - Cierre'),
    ], string='Fase', default='phase_0', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('in_progress', 'En Progreso'),
        ('done', 'Terminado'),
        ('cancelled', 'Cancelado'),
    ], string='Estado', default='draft', tracking=True)
    
    project_id = fields.Many2one('project.project', string='Proyecto Odoo')
    notes = fields.Html(string='Notas')
    
    # Campos computados para Dashboard
    questionnaire_count = fields.Integer(compute='_compute_counts')
    asis_process_count = fields.Integer(compute='_compute_counts')
    gap_count = fields.Integer(compute='_compute_counts')
    gap_resolved_count = fields.Integer(compute='_compute_counts')
    total_estimated_hours = fields.Float(compute='_compute_counts')

    @api.onchange('employee_count')
    def _onchange_employee_count(self):
        if not self.employee_count:
            return
        if self.employee_count <= 10:
            self.company_size = 'micro'
        elif self.employee_count <= 50:
            self.company_size = 'small'
        elif self.employee_count <= 200:
            self.company_size = 'medium'
        else:
            self.company_size = 'large'

    @api.depends_context('lang')
    def _compute_counts(self):
        for record in self:
            record.questionnaire_count = self.env['methodology.questionnaire'].search_count([('project_id', '=', record.id)])
            record.asis_process_count = self.env['methodology.asis.process'].search_count([('project_id', '=', record.id)])
            gaps = self.env['methodology.gap'].search([('project_id', '=', record.id)])
            record.gap_count = len(gaps)
            record.gap_resolved_count = len(gaps.filtered(lambda g: g.state == 'resolved'))
            record.total_estimated_hours = sum(gaps.mapped('estimated_hours'))
            record.task_count = self.env['project.task'].search_count([('project_id', '=', record.project_id.id)]) if record.project_id else 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'Nuevo') == 'Nuevo':
                vals['code'] = self.env['ir.sequence'].next_by_code('methodology.project') or 'NEDI-001'
            
            # Auto-create Odoo Project if not provided
            if not vals.get('project_id'):
                project_vals = {
                    'name': vals.get('name'),
                    'partner_id': vals.get('partner_id'),
                    'description': f"Proyecto de implementación generado desde {vals.get('code', 'NEDI')}"
                }
                new_project = self.env['project.project'].create(project_vals)
                vals['project_id'] = new_project.id

        projects = super().create(vals_list)
        for project in projects:
            project._generate_initial_content()
        return projects

    def _generate_initial_content(self):
        self.ensure_one()
        # 1. Generar Tareas de Fase 0 (Familiarización)
        task_templates = self.env['methodology.task.template'].search([('phase', '=', 'phase_0')])
        if task_templates and self.project_id:
            Task = self.env['project.task']
            for tmpl in task_templates:
                Task.create({
                    'name': tmpl.name,
                    'project_id': self.project_id.id,
                    'description': tmpl.description,
                    'allocated_hours': tmpl.estimated_hours,
                    # 'user_ids': ... (asignar al usuario actual o manager)
                })

        # 2. Generar Cuestionarios por Defecto (según Industria)
        domain = []
        if self.industry_id:
            # Buscar plantillas que coincidan con la industria O que no tengan industria específica (generales)
            domain = ['|', ('industry_ids', '=', False), ('industry_ids', 'in', self.industry_id.id)]
        else:
            # Si no hay industria, solo las generales
            domain = [('industry_ids', '=', False)]
        
        questionnaire_templates = self.env['methodology.questionnaire.template'].search(domain)
        for q_tmpl in questionnaire_templates:
            # Evitar duplicados si ya existe
            existing = self.env['methodology.questionnaire'].search_count([
                ('project_id', '=', self.id),
                ('template_id', '=', q_tmpl.id)
            ])
            if not existing:
                self.env['methodology.questionnaire'].create({
                    'project_id': self.id,
                    'template_id': q_tmpl.id,
                    'state': 'draft',
                })

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done', 'date_end_real': fields.Date.today()})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_view_questionnaires(self):
        return {
            'name': 'Cuestionarios',
            'type': 'ir.actions.act_window',
            'res_model': 'methodology.questionnaire',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    def action_view_asis_processes(self):
        return {
            'name': 'Procesos AS-IS',
            'type': 'ir.actions.act_window',
            'res_model': 'methodology.asis.process',
            'view_mode': 'list,kanban,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    def action_view_gaps(self):
        return {
            'name': 'GAPs',
            'type': 'ir.actions.act_window',
            'res_model': 'methodology.gap',
            'view_mode': 'kanban,list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    def action_generate_workplan(self):
        return {
            'name': 'Generar Plan de Trabajo',
            'type': 'ir.actions.act_window',
            'res_model': 'methodology.generate.workplan.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_project_id': self.id},
        }

    def action_view_tasks(self):
        return {
            'name': 'Tareas del Proyecto',
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'view_mode': 'kanban,list,form',
            'domain': [('project_id', '=', self.project_id.id)],
            'context': {'default_project_id': self.project_id.id},
        }

    task_count = fields.Integer(compute='_compute_counts')
