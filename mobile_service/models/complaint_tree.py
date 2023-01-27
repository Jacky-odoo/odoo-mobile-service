class MobileComplaintTree(models.Model):
    _name = 'mobile.complaint.tree'
    _rec_name = 'complaint_type_tree'

    complaint_id = fields.Many2one('mobile.service')

    complaint_type_tree = fields.Many2one(
        'mobile.complaint', 
        string="Category", 
        required=True)
    description_tree = fields.Many2one('mobile.complaint.description',
                                       string="Description",
                                       domain="[('complaint_type_template','=',complaint_type_tree)]")
