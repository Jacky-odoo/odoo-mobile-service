from odoo import models, fields


class MobileComplaintTree(models.Model):
    """
    A relation between service, complaint and description
    """
    _name = 'moblie_service.complaint.tree'
    _rec_name = 'complaint_type_tree'

    service_id = fields.Many2one(
        comodel_name='mobile_service.service',
        required=True,
        string="Service")
    complaint_id = fields.Many2one(
        comodel_name='mobile_service.complaint',
        string="Complaint",
        required=True)
    complaint_description_id = fields.Many2one(
        comodel_name='mobile_service.complaint.description',
        string="Complaint Description",
        domain="[('complaint_type_template','=',complaint_type_tree)]")
