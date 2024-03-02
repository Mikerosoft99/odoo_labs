# -- coding: utf-8 --
{
    'name': 'To Do App',
    'summary': """This is my ITI ToDo app""",
    'description': """A simple Todo app developed as a project for ITI.""",
    'category': 'Project',
    'version': '1.0',
    'author': 'Kerollos Samy Fawzy',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menus.xml',
        'views/todo_ticket_views.xml',
    ],
    'application': True,
}
