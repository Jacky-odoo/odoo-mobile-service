from odoo import _, api, fields, tools, models
from odoo.http import request

class MobileServiceCrm(models.Model):
    _inherit = ["crm.lead"]
    national_code = fields.Char(string="national code")
    from_net = fields.Boolean(string="Is from internet",readonly=True)