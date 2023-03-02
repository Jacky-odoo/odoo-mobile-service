from odoo import _, api, fields, tools, models


class MobileServiceCrm(models.Model):
    _inherit = ["crm.lead"]
    national_code = fields.Char(string="national code")
