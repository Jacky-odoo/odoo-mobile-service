from odoo import models, fields, api, _


class ProductProduct(models.Model):
    _inherit = 'product.template'

    is_a_parts = fields.Boolean(
        'Is a Mobile Part', default=False,
        help="Specify if the product is a mobile part or not.")

    brand_name = fields.Many2one('mobile.brand', String="Brand", help="Select a mobile brand for the part")
    model_name = fields.Many2one('brand.model', String="Model Name", domain="[('mobile_brand_name','=',brand_name)]",
                                 help="Select a model for the part")
    model_colour = fields.Char(string="Colour", help="colour for the part")
    extra_descriptions = fields.Text(string="Note")