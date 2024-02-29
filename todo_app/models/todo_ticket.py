from odoo import models, fields


class TodoTicket(models.Model):
    _name = 'todo.ticket'
    _description = 'Todo Ticket'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    number = fields.Integer(string='Number')
    tag = fields.Char(string='Tag')
    state = fields.Selection([
        ('new', 'New'),
        ('doing', 'Doing'),
        ('done', 'Done')],
        string='State')
    file = fields.Binary(string='File')
    description = fields.Text(string='Description')
