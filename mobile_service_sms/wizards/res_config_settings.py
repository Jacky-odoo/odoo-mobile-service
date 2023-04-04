# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    server_special = fields.Boolean(
        string="Special Server",
        config_parameter='mobile_sms.server_special'
    )
    server_id = fields.Many2one(
        comodel_name='mobile_sms.server',
        string="Server",
        config_parameter='mobile_sms.server_id',
        help="this is server sms"
    )

    def action_view_servers(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Servers'),
            'res_model': 'mobile_sms.server',
            'view_mode': 'tree,form',
        }
