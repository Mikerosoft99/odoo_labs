from odoo import models, fields


class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = "Doctors"

    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    image = fields.Binary(string="Image")
