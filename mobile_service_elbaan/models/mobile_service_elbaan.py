from odoo import models, fields, api, _
from datetime import datetime
import re


class MobileServiceElbaanShop(models.Model):
    _inherit = 'mobile_service.service'
    _description = 'Mobile Service'
    substate_evaluation = fields.Selection(
        selection=[('evaluation', 'Evaluation'),
                   ('ppsupply', 'Parts/phone supply'),
                   ('repairs', 'Repairs')],
        string='Evaluation Sub States',
        default='evaluation',
        tracking=True)
    items_ids=fields.Many2many(
        comodel_name='mobile_service.items',
        relation='mobile_service_items_rel', 
        string="Included items",
        store=True,
        help="this is items mobile")
    appearance=fields.Text(string="Appearance")
    
    ################################################################################
    #              State Machin: Actions
    ################################################################################

    def action_view_serv(self):
        if self.service_state != 'evaluation':
            self.substate_evaluation='evaluation'
        self.ensure_one()
        ctx = dict(
            create=False,
        )
        return {
            'type': 'ir.actions.act_window',
            'name': _('Service'),
            'res_model': 'mobile_service.service',
            'view_mode': 'tree,form',
            'context': ctx
        }

    # Action for SUB States in mobile service elbaan that we create in mobile service ---------->
    def action_ppsuply_change(self):
        self.substate_evaluation = 'ppsupply'
        return self.action_view_serv()
    
    def action_needparts_service(self):
        return self.action_ppsuply_change()

    def action_bpfone_service(self):
        if self.is_in_warranty:
            return self.action_qcsmobile_service()

    def action_notavailable_service(self):
        if self.is_in_warranty:
             return self.action_ppsuply_change()
        else:
             return self.action_qcsmobile_service()

    def action_rpable_service(self):
         self.substate_evaluation = 'repairs'
         return self.action_view_serv()

    def action_repairabledmobile_service(self):
        if self.is_in_warranty:
           return self.action_rpable_service()
        return self.action_acceptmobile_service()

    def action_unrepairablemobile_service(self):
        if self.is_in_warranty:
             return self.action_ppsuply_change()
        else:
            return self.action_qcsmobile_service()

    def action_needpart_service(self):
        if self.is_in_warranty:
             return self.action_ppsuply_change()
        else:
             return self.action_acceptmobile_service()

    def print_mobile_service_action(self, access_uid=None):
        return {
            'type': 'ir.actions.report',
            'model': 'mobile_service.service',
            'name': 'mobile_service.service',
            'report_type': 'qweb-pdf',
            'binding_model_id': 'model_mobile_service.service',
            'report_name': 'mobile_service.mobile_service_ticket_template',
            'report_file': 'mobile_service.mobile_service_ticket_template'
        }