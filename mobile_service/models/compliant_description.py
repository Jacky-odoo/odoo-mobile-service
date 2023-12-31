from odoo import models, fields


class MobileComplaintTypeTemplate(models.Model):
    _name = 'mobile_service.complaint.description'
    _rec_name = 'name'
    _description="Mobile complaint description"

    name = fields.Char(
        size=64,
        index=True,
        string="Complaint Types",
        help="Name of the description")
    description = fields.Text(
        string="Complaint Description")
    complaint_id = fields.Many2one(
        comodel_name='mobile_service.complaint',
        string="Complaint",
        index=True,
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
        string="Inranal Refrence",
        index=True,
        group_operator="count",
        required=True)
    active=fields.Boolean('Active',default=True, store=True, readonly=False)