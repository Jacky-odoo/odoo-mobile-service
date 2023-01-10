from odoo import models, fields, api, _


class MobileWarranty(models.Model):
    _name = 'mobile.warranty'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Warranty Serial",
                       indexed=True,
                       readonly=True,
                       copy=False,)
    brand_id = fields.Many2one('mobile.brand',
                               string="Mobile Brand")
    model_id = fields.Many2one('brand.model',
                               string="Model",
                               domain="[('mobile_brand_name','=',brand_id)]")
    color = fields.Char(string='Color',
                        help="Color of the device",
                        required=False)
    code_hamta = fields.Char(string="Code",
                             help="A code that show Hamta number")
    imei1 = fields.Char(string="IMEI 1",
                        indexed=True)
    imei2 = fields.Char(string="IMEI 2",
                        indexed=True)
    part_number = fields.Char(string="Part Number")

    importer_id = fields.Many2one('res.partner',
                                  string="Importer Company",
                                  help="")
    warranty_id = fields.Many2one('res.partner',
                                  string="Warranty Company",
                                  help="")
    descriptions = fields.Text(string="Note",
                               help="Extra Note on The Warranty")

    #
    # Create a new name based on the sequnce.
    #
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'mobile.service.warranty') or '/'
        return super(MobileWarranty, self).create(vals)
