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
	employee = fields.Many2one('hr.employee', string='Employee', default=lambda self: self.env.uid)
	create_date = fields.Date('Create Date', default=fields.Date.today())
	company = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.name)
	department = fields.Many2one('hr.department', 'Department')
	deadline = fields.Date('Deadline', required=True, default = datetime.now() + timedelta(days=14))
	idea_type = fields.Many2one('idea.types', 'Idea Type')
	details = fields.Char('Details', required=True)
	votes = fields.Integer('Votes')
	comments = fields.Char('Comments')
	rating = fields.Char('Rating')
	tree_notebook = fields.One2many('employee.ideas', 'employee')
	list_vote = fields.One2many('employee_ideas.wizard', 'id_idea', string='Votes', readonly=True)

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
