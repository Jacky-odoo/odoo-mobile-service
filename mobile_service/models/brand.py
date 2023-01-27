from datetime import datetime, date, timedelta
from odoo import models, fields, api, _

class MobileBrand(models.Model):
    _name = 'mobile.brand'
    _rec_name = 'brand_name'

    brand_name = fields.Char(string="Mobile Brand", 
                             required=True)
    model_ids = fields.One2many(comodel_name="brand.model",
                                inverse_name='mobile_brand_name', 
                                string="Models")

    model_count= fields.Integer(compute='_model_brand_count',
                                string='# Mobile Brand Count',
                                copy=False)

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
