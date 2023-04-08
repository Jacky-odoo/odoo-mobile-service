from odoo import _, api, fields, tools, models
from odoo.http import request

class MobileServiceCrm(models.Model):
    _inherit = ["crm.lead"]
    #do this for show national code in mobile service in persian language
    national_code = fields.Char(string="national code")
    #do this for that service request that come from website
    from_net = fields.Boolean(string="Is from internet",readonly=True)