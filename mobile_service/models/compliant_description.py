
class MobileComplaintTypeTemplate(models.Model):
    _name = 'mobile.complaint.description'
    _rec_name = 'description'

    complaint_type_template = fields.Many2one(
        'mobile.complaint', string="Complaint Type Template", required=True)
    description = fields.Text(string="Complaint Description")


