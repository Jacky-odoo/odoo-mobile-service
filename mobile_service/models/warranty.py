from odoo import models, fields, api, _
from odoo.tools import date_utils
from odoo.exceptions import  UserError
from datetime import datetime ,date
class MobileWarranty(models.Model):
    _name = 'mobile_service.warranty'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True

    name = fields.Char(
        string="Warranty Serial",
        indexed=True,
        readonly=True,
        copy=False,)

    brand_id = fields.Many2one(
        comodel_name='mobile_service.brand',
        string="Mobile Brand",
        required=True)
    model_id = fields.Many2one(
        comodel_name='mobile_service.brand.model',
        string="Model",
        domain="[('brand_id','=',brand_id)]",
        required=True)
    importer_id = fields.Many2one(
        comodel_name='res.partner',
        string="Importer Company",
        help="",
        required=True)
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
        compute='_compute_warranty_is_expire',
        string='Warranty expire',
        help="Specify if the product warranty is expired.",
        copy=False)
    color = fields.Char(
        string='Color',
        help="Color of the device",
        required=False)
    code_hamta = fields.Char(
        size=64,
        index=True,
        string="Code",
        help="A code that show Hamta number",
        required=True)
    imei1 = fields.Char(
        string="IMEI 1",
        size=32,
        indexed=True,
        required=True)
    imei2 = fields.Char(
        string="IMEI 2",
        size=32,
        indexed=True,
        required=True)
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
        track_visibility='always')

    start_date = fields.Date(string="Start Date", tracking=True,required=True)
    expire_date = fields.Date(string="Expire Date", tracking=True)
    #!Check start date of warranty and plus 18 month
    #!else start and expire date go to empty and state go to draft
    @api.onchange("start_date")
    def _onchange_expire_date(self):
        if self.start_date:
            self.expire_date = date_utils.add(self.start_date, months=18)
        else:
            self.expire_date = False
            self.start_date = False
            self.state = 'draft'

    @api.depends('warranty_id')
    def _compute_warranty_is_expire(self):
            if (self.start_date and self.expire_date) and ((datetime.strptime(str(self.expire_date),'%Y-%m-%d')-datetime.strptime(str(date.today()),'%Y-%m-%d')).days >= 1):
                self.warranty_is_expire=False
                self.color=(datetime.strptime(str(self.expire_date),'%Y-%m-%d')-datetime.strptime(str(date.today()),'%Y-%m-%d')).days
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
        #TO-DO
        self.state = 'valid'
    def action_canceled_state(self):
        #TO-DO
        self.state = 'canceled'