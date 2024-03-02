from odoo import models, fields


class Department(models.Model):
    _name = 'hms.department'
    _description = "Hospital Departments"

    name = fields.Char(string="Name", required=True)
    capacity = fields.Integer(string="Capacity")
    is_opened = fields.Boolean(string="Is Opened")
    patients = fields.One2many('hms.patient', 'department_id', string="Patients")
