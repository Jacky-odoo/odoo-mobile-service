import werkzeug
from odoo.http import Controller, route, request


class MobileService(Controller):

    @route('/mobile-service',
           type='http',
           auth="public",
           website=True,
           sitemap=True,
           methods=['GET'])
    def brand_select(self):
        Brand = request.env['mobile_service.brand']
        brands = Brand.search([(1, "=", 1)])

        values = {
            'brands': brands
        }
        return request.render("website_mobile_service.brand_select_wizard", values)

    @route('/mobile-service/<string:ref>',
           type='http',
           auth="public",
           website=True,
           sitemap=True,
           methods=['GET'])
    def brand_model_select(self, ref):
        brand = self._get_brand(ref)
        return request.render("website_mobile_service.brand_model_select_wizard", {
            'brand': brand,
            'models': brand.model_ids
        })

    @route('/mobile-service/<string:brand_ref>/<string:model_ref>',
           type='http',
           auth="public",
           website=True,
           sitemap=True,
           methods=['GET'])
    def complaint_select(self, brand_ref, model_ref):
        Complaint = request.env['mobile_service.complaint']
        return request.render("website_mobile_service.complaint_select_wizard", {
            'brand': self._get_brand(brand_ref),
            'model': self._get_brand_model(model_ref),
            'complaints': Complaint.search([])
        })

    @route('/mobile-service/<string:brand_ref>/<string:model_ref>/<string:complaint_ref>',
           type='http',
           auth="public",
           website=True,
           sitemap=True,
           methods=['GET'])
    def complaint_description_select(self, brand_ref, model_ref, complaint_ref):
        complaint = self._get_complaint(complaint_ref)
        return request.render("website_mobile_service.complaint_description_select_wizard", {
            'brand': self._get_brand(brand_ref),
            'model': self._get_brand_model(model_ref),
            'complaint': complaint,
            'complaint_descriptions': complaint.complaint_description_ids
        })

    @route('/mobile-service/<string:brand_ref>/<string:model_ref>/<string:complaint_ref>/<string:complaint_description_ref>',
           type='http',
           auth="public",
           website=True,
           sitemap=True,
           methods=['GET'])
    def register_issue_form(self, brand_ref, model_ref, complaint_ref, complaint_description_ref):
        return request.render("website_mobile_service.request_submit_wizard", {
            'brand': self._get_brand(brand_ref),
            'model': self._get_brand_model(model_ref),
            'complaint': self._get_complaint(complaint_ref),
            'complaint_description': self._get_complaint_description(complaint_description_ref)
        })

    @route('/mobile-service/submit_service_request',
           type='http',
           auth="public",
           website=True,
           sitemap=False,
           methods=['POST'])
    def register_issue(self, **kw):
        # maso, submet as CRM or repair service

        brand = self._get_brand(kw['brand_ref'] if 'brand_ref' in kw else '')
        mode = self._get_brand_model(
            kw['model_ref'] if 'model_ref' in kw else '')
        complaint = self._get_complaint(
            kw['complaint_ref'] if 'complaint_ref' in kw else '')
        complaint_description = self._get_complaint_description(
            kw['complaint_description_ref'] if 'complaint_description_ref' in kw else '')

        gen_name = kw['contact_name'] + \
            '( '+brand.name+':'+mode.name+':' + \
            complaint.name+':'+complaint_description.name+')'

        Model = request.env['crm.lead']
        Model.sudo().create({
            'name': gen_name,
            'street': kw['street'],
            'phone': kw['phone'],
            'email_from': kw['email_from'],
            'description': kw['description'],
            'from_net' : '1',
        })
        return werkzeug.utils.redirect("/mobile-service-thanks")

    def _get_brand(self, ref):
        return self._get_model_by_ref('mobile_service.brand', ref)

    def _get_brand_model(self, ref):
        return self._get_model_by_ref('mobile_service.brand.model', ref)

    def _get_complaint(self, ref):
        return self._get_model_by_ref('mobile_service.complaint', ref)

    def _get_complaint_description(self, ref):
        return self._get_model_by_ref('mobile_service.complaint.description', ref)

    def _get_model_by_ref(self, model_name, ref):
        Model = request.env[model_name]
        items = Model.search([("internal_ref", "=", ref)])
        if len(items) != 1:
            raise werkzeug.exceptions.NotFound()
        return items[0]
