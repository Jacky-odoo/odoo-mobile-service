from odoo import _, api, fields, tools, models
from odoo.http import request

class MobileServiceCrm(models.Model):
    _inherit = ["crm.lead"]
    national_code = fields.Char(string="national code")
#! Connect To Mobile Service and Create this item for this fields
    def register_to_mobile_service(self):
        # Create CRM and record this fields
        Model = request.env['mobile_service.service']
        Model.sudo().create({
            'name': self.name,
            'street': self.street,
            'contact_no': self.mobile,
            'email_id': self.email_from,
            'service_state': self.description,
            'accept_dated' : self.ate_open,
            'warranty_id.expire_date' : self.date_closed,
            'partner_id' : self.person_id.id,
            'national_code' : self.national_code,
        })