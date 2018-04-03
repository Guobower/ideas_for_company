from odoo import models, fields, api

class Wizard(models.TransientModel):
	_name = 'employee_ideas.wizard'
	
	rating = fields.Integer('Rating')
	comments = fields.Char('Comments')