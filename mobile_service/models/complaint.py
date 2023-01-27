
class MobileComplaintType(models.Model):
    _name = 'mobile.complaint'
    _rec_name = 'complaint_type'

    complaint_type = fields.Char(string="Complaint Type", required=True)
