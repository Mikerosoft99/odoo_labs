from odoo import models, fields


class TodoTicket(models.Model):
    _name = 'todo.ticket'
    _description = 'Todo Ticket'
    _rec_name = 'name'

    name = fields.Char('Name')
    number = fields.Integer('Number')
    tag = fields.Char('Tag')
    state = fields.Selection([
        ('new', 'New'),
        ('doing', 'Doing'),
        ('done', 'Done')],
        'State')
    file = fields.Binary('File')
    description = fields.Text('Description')
