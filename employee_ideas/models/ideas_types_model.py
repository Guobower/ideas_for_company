# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EmployeeIdeasTypes(models.Model):

	_name = 'idea.types'
	
	_description = 'Idea Types'
	
	ideas = fields.One2many('employee.ideas', string='EmployeeIdeas')
	
	name = fields.Char('Name', required=True)
	
	minimum_vote = fields.Integer('Minimum Vote')
	
	maximum_vote = fields.Integer('Maximum Vote')
	
	total_ideas = fields.Integer('Total Ideas', default=lambda self: self._get_total_ideas(), readonly=True, store=False)
	
	department = fields.Many2one('hr.department', 'Department')
	
	manager = fields.Char('Manager')
	
	tree_department = fields.One2many('idea.types', 'department')
	
	@api.model
	def _get_total_ideas(self) :
		sum = 0
		for idea in ideas :
			sum += 1
		return sum