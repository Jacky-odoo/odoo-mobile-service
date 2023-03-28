from odoo import models, fields, api, _


class ProductProduct(models.Model):
    _inherit = 'product.template'
    _description=" "

    is_a_parts = fields.Boolean(
        string='Is a Mobile Part',
        default=False,
        help="Specify if the product is a mobile part or not.")
    brand_id = fields.Many2one(
        comodel_name='mobile_service.brand',
        string="Brand",
        help="Select a mobile brand for the part")
    model_id = fields.Many2one(
        comodel_name='mobile_service.brand.model',
        string="Model Name",
        domain="[('brand_id','=',brand_id)]",
        help="Select a model for the part")
    model_color = fields.Char(
        string='Color',
        help="Color for the part")
