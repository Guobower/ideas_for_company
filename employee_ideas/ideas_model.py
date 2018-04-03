# -*- coding: utf-8 -*-
from odoo import models, fields, api 
class EmployeeIdeas(models.Model):
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
	employee = fields.Many2one('res.users', 'Employee')
	create_date = fields.Date('Create Date')
	company = fields.Many2one('res.company', 'Company')
	department = fields.Many2one('hr.department', 'Department')
	deadline = fields.Date('Deadline', required=True)
	idea_type = fields.Many2one('idea.types', 'Idea Type')
	details = fields.Char('Details', required=True)
	votes = fields.Integer('Votes', compute='_vote')
	comments = fields.Char('Comments')
	rating = fields.Char('Rating')
	tree_notebook = fields.One2many('employee.ideas', 'employee')
	@api.one
	def waiting_progressbar(self):
		self.write({'state': 'waiting'})
		
	@api.one
	def approve_progressbar(self):
		self.write({'state': 'approved'})
		
	@api.one
	def reject_progressbar(self):
		self.write({'state': 'new'})
	
	@api.one
	def close_progressbar(self):
		self.write({'state': 'closed'})
		
	@api.one
	def _vote(self):
		count = 10
		return count
