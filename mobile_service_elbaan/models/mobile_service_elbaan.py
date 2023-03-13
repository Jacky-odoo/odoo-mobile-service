from odoo import models, fields, _
from datetime import datetime


class MobileServiceElbaanShop(models.Model):
    _inherit = 'mobile_service.service'
    substate_evaluation = fields.Selection(
        selection=[('evaluation', 'Evaluation'),
                   ('ppsupply', 'Parts/phone supply'),
                   ('repairs', 'Repairs')],
        string='Evaluation Sub States',
        track_visibility='always',
        default='evaluation',
        tracking=True)


    ################################################################################
    #              State Machin: Actions
    ################################################################################


    # Action for SUB States in mobile service elbaan that we create in mobile service ---------->
    def action_needparts_service(self):
        self.substate_evaluation = 'ppsupply'

    def action_bpfone_service(self):
        if self.is_in_warranty:
             self.service_state = 'quality'

    def action_notavailable_service(self):
        if self.is_in_warranty:
             self.substate_evaluation = 'ppsupply'
        else:
             self.service_state = 'quality'

    def action_rpable_service(self):
         self.substate_evaluation = 'repairs'

    def action_repairabledmobile_service(self):
        if self.is_in_warranty:
            self. substate_evaluation = 'ppsupply'
        else:
            self.service_state = 'customer'

    def action_unrepairablemobile_service(self):
        if self.is_in_warranty:
             self.substate_evaluation = 'repairs'
        else:
             self.service_state = 'quality'

    def action_needpart_service(self):
        if self.is_in_warranty:
             self.substate_evaluation = 'ppsupply'
        else:
             self.service_state = 'customer'

    