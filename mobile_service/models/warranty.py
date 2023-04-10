from odoo import models, fields, api, _
from odoo.tools import date_utils
from odoo.exceptions import  UserError
from datetime import datetime ,date
class MobileWarranty(models.Model):
    _name = 'mobile_service.warranty'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True
    _description="Mobile warranty"

    name = fields.Char(
        string="Warranty Serial",
        index=True,
        readonly=True,
        copy=False,)

    brand_id = fields.Many2one(
        comodel_name='mobile_service.brand',
        string="Mobile Brand",
        required=True)
    model_id = fields.Many2one(
        comodel_name='mobile_service.brand.model',
        string="Model",
        domain="[('brand_id','=',brand_id)]")
    importer_id = fields.Many2one(
        comodel_name='res.partner',
        string="Importer Company",
        help="")
    warranty_id = fields.Many2one(
        comodel_name='res.partner',
        string="Warranty Company",
        help="")
    company_id = fields.Many2one(
        comodel_name='res.company',
        string="Company",
        required=True,
        default=lambda self: self.env.company,
        help="This is company id")
    warranty_is_expire = fields.Boolean(
        compute='_onchange_expire_date',
        string='Warranty expire',
        help="Specify if the product warranty is expired.",
        default=False,
        copy=False)
    color = fields.Char(
        string='Color',
        help="Color of the device")
    code_hamta = fields.Char(
        size=64,
        index=True,
        string="Code Hamta",
        help="A code that show Hamta number")
    imei1 = fields.Char(
        string="IMEI 1",
        size=32,
        index=True,
        required=True)
    imei2 = fields.Char(
        string="IMEI 2",
        size=32,
        index=True)
    part_number = fields.Char(
        size=32,
        index=True,
        string="Part Number")

    descriptions = fields.Text(
        string="Note",
        help="Extra Note on The Warranty")

    state = fields.Selection(
        selection=[('draft', 'Draft'),
                   ('valid', 'Valid'),
                   ('canceled', 'Canceled')],
        string='Status',
        default='draft',
        tracking=True)

    start_date = fields.Date(string="Start Date", tracking=True)
    expire_date = fields.Date(string="Expire Date", tracking=True)
    #!Check start date of warranty and plus 18 month
    #!else start and expire date go to empty and state go to draft
    @api.onchange("start_date")
    def _onchange_expire_date(self):
        #When change start date We added expire date and then if start date is false other 
        if self.start_date:
            self.expire_date = date_utils.add(self.start_date, months=18)
        else:
            self.expire_date = False
            self.start_date = False
            self.state = 'draft'
        #!Compute that warranty is expire or no
        if (self.start_date and self.expire_date) and ((datetime.strptime(str(self.expire_date),'%Y-%m-%d')-datetime.strptime(str(date.today()),'%Y-%m-%d')).days >= 1):
            self.warranty_is_expire=False
        else:
            self.warranty_is_expire=True

    #!Create a new name based on the sequnce.
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'mobile_service.warranty.sequence') or '/'
        return super(MobileWarranty, self).create(vals)
    
    
    #!When we will delete a warranty
    def unlink(self):
        for i in self:
            if i.state != 'draft':
                raise UserError(
                    _('You cannot delete an Assigned warranty'))
        return super(MobileWarranty, self).unlink()

    def action_valid_state(self):
        if self.model_id and self.brand_id and self.company_id and self.start_date and self.code_hamta and self.importer_id and self.warranty_id:
            self.state = 'valid'
        else:
        #!Create an Error in warranty 
            return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('You must Fill This Fields for warranty: %s.',self.name),
                'message': _('IMEI ,Brand ,Model ,Importer and warranty Company ,Start Date'),
                'type': 'danger',
                'sticky': True,  #True/False will display for few seconds if false
                'next': {'type': 'ir.actions.act_window_close'},
                },
            }
    def action_canceled_state(self):
        #TO-DO
        self.state = 'canceled'