from odoo import models, fields, api, _
from odoo.addons.iap.tools import iap_tools
import requests


class MobileSmsComposer(models.TransientModel):
    _inherit = "sms.composer"
    server_ids = fields.Many2many(
        comodel_name='mobile_sms.server',
        relation='mobile_service_server_rel', 
        string="Server",
        store=True,
        help="this is server sms")
    
   