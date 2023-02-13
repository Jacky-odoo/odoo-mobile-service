from odoo import models, fields, api, _
from odoo.tools import date_utils


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
        string="Mobile Brand")
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

    color = fields.Char(
        string='Color',
        help="Color of the device",
        required=False)
    code_hamta = fields.Char(
        size=64,
        index=True,
        string="Code",
        help="A code that show Hamta number")
    imei1 = fields.Char(
        string="IMEI 1",
        size=32,
        indexed=True)
    imei2 = fields.Char(
        string="IMEI 2",
        size=32,
        indexed=True)
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

    start_date = fields.Date(string="Start Date", tracking=True)
    expire_date = fields.Date(string="Expire Date", tracking=True)

    @api.onchange("start_date")
    def _onchange_expire_date(self):
        if self.start_date:
            self.expire_date = date_utils.add(self.start_date, months=18)
            self.state = 'valid'
        else:
            self.expire_date = False
            self.start_date = False
            self.state = 'draft'

    #
    # Create a new name based on the sequnce.
    #
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'mobile_service.warranty.sequence') or '/'
        return super(MobileWarranty, self).create(vals)


    def canceled_date_state(self):
        #TO-DO
        self.state = 'canceled'