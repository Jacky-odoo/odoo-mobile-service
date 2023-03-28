# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    server_special = fields.Boolean(string="Special Server")
    server_id = fields.Many2one(
        comodel_name='mobile_sms.server',
        string="Server",
        config_parameter='mobile_sms.server.name',
        help="this is server sms")
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            server_special=self.env['ir.config_parameter'].sudo().get_param('mobile_sms.server_special')
        )
        return res
    
    @api.model
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('mobile_sms.server_special', self.server_special)

    