# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta
from datetime import datetime
import logging

class EmployeeIdeas(models.Model):
	_rec_name = 'title'
	_name = 'employee.ideas'
	_inherit = ['mail.thread']
	_description = 'Employee Ideas'
	state = fields.Selection([
            ('new', 'New'),
            ('waiting', 'Waiting for Approval'),
            ('approved', 'Approved'),
            ('closed', 'Closed'),
            ],default='new')
	title = fields.Char('Title', required=True)
	employee = fields.Many2one('hr.employee', string='Employee', default=lambda self: self._get_default_employee())
	create_date = fields.Date('Create Date', default=fields.Date.today())
	company = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.name)
	department = fields.Many2one('hr.department', 'Department', default=lambda self: self._get_default_department())
	deadline = fields.Date('Deadline', required=True, default = datetime.now() + timedelta(days=14))
	idea_type = fields.Many2one('idea.types', 'Idea Type')
	details = fields.Char('Details', required=True)
	votes = fields.Integer('Votes')
	comments = fields.Char('Comments')
	rating = fields.Char('Rating')
	tree_notebook = fields.One2many('employee.ideas', 'employee')
	list_vote = fields.One2many('employee_ideas.wizard', 'id_idea', string='Votes', readonly=True)
	
	@api.model
	def _get_default_employee(self)  :
		user_id = self.env.uid
		employee_id = self._cr.execute('SELECT hr_employee.id FROM hr_employee, resource_resource, res_user WHERE hr_employee.id = resource_resource.id AND resource_resource.user_id = ' + user_id)
		return employee_id
		
	@api.model
	def _get_default_department(self) :
		user_id = self.env.uid
		department_id = self._cr.execute('SELECT hr_department.id FROM hr_department, hr_employee WHERE hr_department.id = hr_employee.department_id AND hr_employee.id = ' + self.employee)
		return department_id

	@api.multi
	def waiting_progressbar(self):
		self.write({'state': 'waiting'})
		for idea in self:
			if idea.employee.user_id != self.env.user:
				raise ValidationError('Only the responsible can do this!')
				return super(EmployeeIdeas, self).waiting_progressbar()
			else:
				return self.write({'state': 'waiting'})

	def approve_progressbar(self):
		self.write({'state': 'approved'})

	def reject_progressbar(self):
		self.write({'state': 'new'})

	def close_progressbar(self):
		self.write({'state': 'closed'})
	
	@api.multi
	def do_give_vote(self):
		_logger = logging.getLogger(__name__)
		_logger.debug('ID:'+ str(self.id))
		return{
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'employee_ideas.wizard',
			'target': 'new',
			'type': 'ir.actions.act_window',
			'context': {'current_id': self.id},
		}
