# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta
from datetime import datetime

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
	
	employee = fields.Many2one('hr.employee', string='Employee', default=lambda self: self._get_default_employee(), store=True, readonly=True)
	
	create_date = fields.Date('Create Date', default=fields.Date.today(), store=True, readonly=True)
	
	company = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id, store=True, readonly=True)
	
	department = fields.Many2one('hr.department', 'Department', default=lambda self: self._get_default_department(), store=True, readonly=True)
	
	deadline = fields.Date('Deadline', required=True, default = datetime.now() + timedelta(days=14), store=True, readonly=True)
	
	idea_type = fields.Many2one('idea.types', 'Idea Type')
	
	details = fields.Char('Details', required=True)
	
	votes = fields.One2many('employee.ideas.votes', 'ideas_id')
	
	tree_notebook = fields.One2many('employee.ideas', 'employee')
	
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
	def write(self, vals) :
		if vals.get('employee', False) :
			vals['employee'] = self._get_default_employee()
			
		if vals.get('create_date', False) :
			vals['create_date'] = fields.Date.today()
			
		if vals.get('company', False) :
			vals['company'] = self.env.user.company_id
			
		if vals.get('department', False) :
			vals['department'] = self._get_default_department()
			
		if vals.get('deadline', False) :
			vals['deadline'] = datetime.now() + timedelta(days=14)
		
		return super(EmployeeIdeas, self).write(vals)
		
	@api.model
	def create(self, vals) :
		if vals['employee'] is None:
			vals['employee'] = self._get_default_employee()
			
		if vals['create_date'] is None :
			vals['create_date'] = fields.Date.today()
			
		if vals['company'] is None :
			vals['company'] = self.env.user.company_id
			
		if vals['department'] is None :
			vals['department'] = self._get_default_department()
			
		if vals['deadline'] is None :
			vals['deadline'] = datetime.now() + timedelta(days=14)
		
		return super(EmployeeIdeas, self).write(vals)
		
	def show_wizard(self) :
		
		query = 'SELECT COUNT(id) FROM employee_ideas WHERE idea_type = "' + self.idea_type + '"'
		
		total_votes = self._cr.execute(query)
		
		if(self.idea_type.maximum_vote > total_votes) :
			return {
				'name' : 'Employee Votes',
				'type' : 'ir.actions.act_window',
				'res_model' : 'employee.ideas.votes',
				'view_mode' : 'form',
				'view_type' : 'form',
				'target' : 'new',
				'context' : {'ideas_id' : self._origin.id},
			}
		else :
			return {} # Maksimal Vote Terlampaui
	
	def waiting_progressbar(self):
		self.write({'state': 'waiting'})
		
	def approve_progressbar(self):
		self.write({'state': 'approved'})
		
	def reject_progressbar(self):
		self.write({'state': 'new'})
	
	def close_progressbar(self):
		self.write({'state': 'closed'})