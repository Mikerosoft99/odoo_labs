from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class Patient(models.Model):
    _name = 'hms.patient'
    _description = "Hospital Management System"
    _rec_name = "full_name"

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float(string="CR Ratio")
    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O')
    ])
    pcr = fields.Boolean(string="PCR")
    image = fields.Binary(attachment=True, store=True)
    address = fields.Text()
    age = fields.Integer(compute='_compute_age')
    full_name = fields.Char(compute='_compute_full_name')
    department_id = fields.Many2one('hms.department', string="Department", domain="[('is_opened', '=', True)]")
    doctor_ids = fields.Many2many('hms.doctor', string="Doctors")
    department_capacity = fields.Integer(related='department_id.capacity')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default='undetermined')
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string='Log History')
    email = fields.Char(string="Email", required=True, unique=True)

    _constraints = [
        ('unique_email', 'UNIQUE(email)', 'Email must be unique!'),
    ]

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            email_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})$"
            if not re.match(email_regex, record.email):
                raise ValidationError("Invalid email format!")

    def action_undetermined(self):
        for rec in self:
            rec.state = 'undetermined'

    def action_good(self):
        for rec in self:
            rec.state = 'good'

    def action_fair(self):
        for rec in self:
            rec.state = 'fair'

    def action_serious(self):
        for rec in self:
            rec.state = 'serious'

    # ➢ With each change of the state a new log record is being
    # created with a description of (State changed to
    # NEW_STATE)
    def write(self, vals):
        old_state = self.state
        res = super(Patient, self).write(vals)
        if 'state' in vals and vals['state'] != old_state:
            state_field = self._fields['state']
            new_state_label = dict(state_field.selection).get(vals['state'])
            self.log_ids.create({
                'patient_id': self.id,
                'created_by': self.env.user.id,
                'description': f"State changed to {new_state_label}"
            })
        return res

    # compute full_name
    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            if record.last_name:
                record.full_name = f"{record.first_name} {record.last_name}"
            else:
                record.full_name = record.first_name

    # compute age
    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                delta = today - record.birth_date
                record.age = int(delta.days / 365)
            else:
                record.age = 0

    # ➢ The Doctors field is a many2many tags and should be
    # readonly until the department is being selected
    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            self.doctor_ids = [(6, 0, [])]
            self.doctor_ids = [(4, doctor.id) for doctor in self.department_id.doctors]

    # If The pcr field is checked, the CR ratio field should be
    # mandatory
    @api.constrains('pcr', 'cr_ratio')
    def _check_pcr_cr_ratio(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError("CR Ratio is mandatory when PCR is checked.")

    # ➢ The PCR field should be automatically checked if the age is
    # lower than 30 and show a warning message that it has
    # been checked
    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': "PCR Checked",
                    'message': "PCR has been automatically checked due to the age being less than 30.",
                }
            }

    # to add patient in department (fix doctor problem)
    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            self.doctor_ids = [(6, 0, [])]
            self.doctor_ids = [(4, doctor.id) for doctor in self.department_id.doctor_ids]


class PatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log'

    patient_id = fields.Many2one('hms.patient', string='Patient', required=True)
    created_by = fields.Many2one('res.users', default=lambda self: self.env.user, required=True)
    date = fields.Date(default=fields.Date.today, required=True)
    description = fields.Text()
