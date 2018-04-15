from odoo import models, fields, api

class Wizard(models.TransientModel):
	_name = 'employee_ideas.wizard'
	
	rating = fields.Selection([
			('worst', 'Worst'),
			('very_bad', 'Very Bad'),
            ('bad', 'Bad'),
            ('not_bad', 'Not Bad'),
            ('good', 'Good'),
            ('very_good', 'Very Good'),
            ],default='worst')
	comments = fields.Char('Comments', required=True)