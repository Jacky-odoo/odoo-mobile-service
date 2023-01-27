
from odoo import models, fields


class MobileServiceTermsAndConditions(models.Model):
    _name = 'moblie_service.term.condition'
    _rec_name = 'name'

    name = fields.Char(
        String="Terms and condition",
        compute="_find_id")

    description = fields.Text(
        string="Description")

    def _find_id(self):
        self.terms_id = self.id or ''
