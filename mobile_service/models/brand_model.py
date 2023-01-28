from odoo import models, fields


class MobileBrandModels(models.Model):
    _name = 'mobile_service.brand.model'
    _rec_name = 'name'

    brand_id = fields.Many2one(
        comodel_name='mobile_service.brand',
        string="Mobile Brand",
        index=True,
        required=True)
    name = fields.Char(
        string="Model Name",
        required=True,
        translate=True)
    image = fields.Image(
        string="Image",
        max_height=800,
        max_width=800,
        verify_resolution=True,
        help="This image used in wizard")
    internal_ref = fields.Char(
        size=16,
        trim=True,
        translate=False,
        help="Used in url and internal usages",
        string="Inranal Refrence",
        index=True,
        group_operator="count")
