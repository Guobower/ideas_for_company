# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta
from datetime import datetime

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
	employee = fields.Many2one('res.users', string='Employee', defalut=lambda self: self.env.uid)
	create_date = fields.Date('Create Date', default=fields.Date.today())
	company = fields.Many2one('res.company', string='Company', defalut=lambda self: self.env.uid.company_id)
	department = fields.Many2one('hr.department', 'Department')
	deadline = fields.Date('Deadline', required=True, default = datetime.now() + timedelta(days=14))
	idea_type = fields.Many2one('idea.types', 'Idea Type')
	details = fields.Char('Details', required=True)
	votes = fields.Integer('Votes', compute='_vote')
	comments = fields.Char('Comments')
	rating = fields.Char('Rating')
	tree_notebook = fields.One2many('employee.ideas', 'employee')
	
	def waiting_progressbar(self):
		self.write({'state': 'waiting'})
		
	def approve_progressbar(self):
		self.write({'state': 'approved'})
		
	def reject_progressbar(self):
		self.write({'state': 'new'})
	
	def close_progressbar(self):
		self.write({'state': 'closed'})
