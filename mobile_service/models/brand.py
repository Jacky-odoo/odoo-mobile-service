from datetime import datetime, date, timedelta
from odoo import models, fields, api, _


class MobileBrand(models.Model):
    _name = 'mobile.brand'
    _rec_name = 'name'

    name = fields.Char(string="Mobile Brand",
                       translate=True,
                       trim=True,
                       required=True)

    model_ids = fields.One2many(comodel_name="brand.model",
                                inverse_name='mobile_brand_name',
                                string="Models")

    model_count = fields.Integer(compute='_model_brand_count',
                                 string='# Mobile Brand Count',
                                 copy=False)
    image = fields.Image(string="Image For Brand",
                         max_height=800,
                         max_width=800,
                         verify_resolution=True,
                         help="This image used in wizard")
    internal_ref = fields.Char(size=16,
                               trim=True,
                               translate=False,
                               help="Used in url and internal usages",
                               string="Inranal Refrence",
                               index=True,
                               group_operator="count")

    def _model_brand_count(self):
        self.ensure_one()
        self.model_count = self.env['brand.model'].search(
            [('mobile_brand_name', '=', self.id)], count=True)

    def action_view_brand_count(self):
        self.ensure_one()
        ctx = dict(
            create=False,
        )
        action = {
            'name': _("Brandes"),
            'type': 'ir.actions.act_window',
            'res_model': 'brand.model',
            'target': 'current',
            'context': ctx
        }
        model_ids = self.env['brand.model'].search(
            [('mobile_brand_name', '=', self.id)])
        inv_ids = []
        for each in model_ids:
            inv_ids.append(each.id)
        if len(inv_ids) == 1:
            model_id = inv_ids and inv_ids[0]
            action['res_id'] = model_id
            action['view_mode'] = 'form'
            action['views'] = [
                (self.env.ref('mobile_service.mobile_brand_model_form_view').id, 'form')]
        else:
            action['view_mode'] = 'tree,form'
            action['domain'] = [('id', 'in', inv_ids)]
        return action
