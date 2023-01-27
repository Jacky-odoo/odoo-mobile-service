from odoo import models, fields, api, _

class Partner(models.Model):
    _inherit = 'res.partner'

    mobile_service_ids = fields.One2many(
        comodel_name='mobile.service',
        inverse_name='person_name',
        string="Mobile Services")

    mobile_service_count = fields.Integer(
        compute='_mobile_service_count',
        string='# Moblie Services',
        copy=False)

    def _mobile_service_count(self):
        self.ensure_one()
        self.mobile_service_count = self.env['mobile.service'].search(
            [('person_name', '=', self.id)], count=True)

    def action_view_mobile_services(self):
        self.ensure_one()
        ctx = dict(
            create=True,
        )
        action = {
            'name': _("Services"),
            'type': 'ir.actions.act_window',
            'res_model': 'mobile.service',
            'target': 'current',
            'context': ctx
        }
        service_ids = self.mobile_service_ids
        serv_ids = []
        for each in service_ids:
            serv_ids.append(each.id)
        if len(serv_ids) == 1:
            service_id = serv_ids and serv_ids[0]
            action['res_id'] = service_id
            action['view_mode'] = 'form'
            action['views'] = [
                (self.env.ref('mobile_service.mobile_service_request_form_view').id, 'form')]
        else:
            action['view_mode'] = 'tree,form'
            action['domain'] = [('id', 'in', serv_ids)]
        return action
