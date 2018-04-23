from odoo import tools, models, fields, api

class Wizard(models.TransientModel):
	_name = 'employee_ideas.wizard'

	rating = fields.Selection([
			('1', 'Worst'),
			('2', 'Very Bad'),
            ('3', 'Bad'),
            ('4', 'Not Bad'),
            ('5', 'Good'),
            ('6', 'Very Good'),
            ],default='1')

	@api.model
	def _current_id(self):

	#	resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])[0]
	#	employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])[0]

		return self.env['employee.ideas'].browse(self._context.get('current_id', 1))

	@api.model
	def _current_employee(self):

		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])

		return employee.id

	@api.model
	def _current_department(self):

		resource = self.env['resource.resource'].search([('user_id','=', self.env.uid)])
		employee = self.env['hr.employee'].search([('resource_id','=', resource.id)])

		return employee.department_id

	comments = fields.Text('Comments', required=True)
	id_idea = fields.Many2one('employee.ideas',string='Ideas',required=True,default=_current_id,readonly=True)

	department = fields.Many2one('hr.department', string="Department", default=_current_department, readonly=True)
	employee = fields.Many2one('hr.employee', string="Employee", required=True, default=_current_employee, readonly=True)
