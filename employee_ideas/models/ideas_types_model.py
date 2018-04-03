# -*- coding: utf-8 -*-
from odoo import models, fields, api
class EmployeeIdeasTypes(models.Model):
	_name = 'idea.types'
	_description = 'Idea Types'
	name = fields.Char('Name', required=True)
	minimum_vote = fields.Integer('Minimum Vote')
	maximum_vote = fields.Integer('Maximum Vote')
	total_ideas = fields.Integer('Total Ideas')
	department = fields.Many2one('hr.department', 'Department')
	manager = fields.Char('Manager')
	tree_department = fields.One2many('idea.types', 'department')
