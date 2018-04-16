{
	'name': 'Employee Ideas',
	'description': 'This module allow employees in the company to raise and create ideas and after approval of ideas other employees in departments can vote for that idea',
	'author': 'Gerry Agustian Juneu, Mufid J',
	'depends': ['base', 'mail', 'hr'],
	'application': True,
	'data': ['views/ideas_view.xml', 'views/employee_ideas_menu.xml', 'views/ideas_types.xml', 'security/ir.model.access.csv', 'reports/todo_report.xml', 'views/wizard.xml'],
}