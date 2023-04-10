
from odoo import models, fields


class MobileServiceTermsAndConditions(models.Model):
    _name = 'mobile_service.term.condition'
    _rec_name = 'name'
    _description="Mobile Term Condition"

    name = fields.Char(
        String="Terms and condition",
        compute="_find_id")

    description = fields.Text(
        string="Description")

    def _find_id(self):
        for item in self:
            item.name = item.id or ''
