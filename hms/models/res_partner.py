from odoo import models, fields, api, exceptions


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='Related Patient', groups='base.group_user')
    vat = fields.Char(string='Tax ID', required=True)

    @api.constrains('email')
    def _check_duplicate_email(self):
        for partner in self:
            if partner.email:
                existing_patient = self.env['hms.patient'].search([('email', '=', partner.email)])
                if existing_patient:
                    raise exceptions.ValidationError('This email is already associated with a patient.')

    def unlink(self):
        linked_to_patient = self.filtered(lambda partner: partner.related_patient_id)
        if linked_to_patient:
            raise exceptions.UserError("You cannot delete a customer linked to a patient.")
        return super(ResPartner, self - linked_to_patient).unlink()
