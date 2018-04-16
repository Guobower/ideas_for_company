from odoo import models, fields, api

class Votes(models.Model):
	_name = 'employee.ideas.votes'
	
	ideas_id = fields.Many2one('employee.ideas',string='Ideas',default=lambda self: context.get('ideas_id', False))
	
    employee = fields.Many2one('hr.employee', string='Employee', default=lambda self: self._get_default_employee(), readonly=True, store=True)
	
    department = fields.Many2one('hr.department', 'Department')
	
	rating = fields.Selection([
			(0, 'Worst'),
			(1, 'Very Bad'),
            (2, 'Bad'),
            (3, 'Not Bad'),
            (4, 'Good'),
            (5, 'Very Good'),
            ],default=0)

	comments = fields.Char('Comments', required=True)
	
	@api.model
	def _get_default_employee(self)  :
		user_id = self.env.uid
		employee_id = self._cr.execute('SELECT hr_employee.id FROM hr_employee, resource_resource, res_user WHERE hr_employee.id = resource_resource.id AND resource_resource.user_id = ' + user_id)
		return employee_id
		
	@api.multi
	def write(self, vals) :
		if vals.get('employee', False) :
			vals['employee'] = self._get_default_employee()
		
		return super(EmployeeIdeas, self).write(vals)
		
	@api.model
	def create(self, vals) :
		if vals['employee'] is None:
			vals['employee'] = self._get_default_employee()
		
		return super(EmployeeIdeas, self).write(vals)