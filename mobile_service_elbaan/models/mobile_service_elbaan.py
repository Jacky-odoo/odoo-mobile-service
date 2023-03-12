from odoo import models,fields, _
from datetime import datetime


class MobileServiceElbaanShop(models.Model):
    _inherit = ['mobile_service.service']
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

    # States that we create ---------->


    def action_draftmobile_service(self):
        """
        this is called when a record set in first level
        """
        self.service_state = 'draft'

    def action_accept_service(self):
        """
        this is called when a record set in second level
        """
        self.accept_date = datetime.now()
        self.service_state = 'accepted'

    def action_acceptmobile_service(self):
        """
        this is called after draft this is Customer action and notification
        """
        self.service_state = 'customer'

    def action_easmobile_service(self):
        """
        this called after Customer action and notification and this is Evalution and service
        """
        self.service_state = 'evaluation'

    def action_qcsmobile_service(self):
        """
        this called after Evalution and service and this is quality Control and shipping
        """
        self.service_state = 'quality'

    def action_finmobile_service(self):
        """
        this called after quality Control and shipping this is Delivery state
        to this level can send information to crm , Print , send email
        """
        self.return_date = datetime.now()
        self.service_state = 'delivered'
