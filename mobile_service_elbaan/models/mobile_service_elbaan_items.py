from odoo import models, fields, _
from datetime import datetime
import re


class MobileServiceElbaanItemms(models.Model):
    _name = 'mobile_service.items'
    _description = 'Elbaan Company Additional Items'
    _rec_name = 'name'

    name = fields.Char(
        string="Mobile Items",
        translate=True,
        trim=True,
        required=True)
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
        string="Internal Refrence",
        index=True,
        group_operator="count",
        required=True)
    active=fields.Boolean('Active',default=True, store=True, readonly=False)
    