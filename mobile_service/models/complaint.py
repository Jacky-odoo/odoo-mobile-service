from odoo import models, fields

class MobileComplaintType(models.Model):
    _name = 'mobile_service.complaint'
    _rec_name = 'name'

    name = fields.Char(
        string="Complaint Type", 
        required=True,
        translate=True,
        trim=True)
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
