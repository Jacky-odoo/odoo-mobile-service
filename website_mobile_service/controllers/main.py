import werkzeug
from odoo.http import Controller, route, request


class MobileService(Controller):

    @route('/mobile-service', type='http', auth="public", website=True, sitemap=True)
    def brand_select(self):
        Brand = request.env['mobile_service.brand']
        brands = Brand.search([(1, "=", 1)])

        values = {
            'brands': brands
        }
        return request.render("website_mobile_service.brand_select_wizard", values)

    @route('/mobile-service/<string:ref>', type='http', auth="public", website=True, sitemap=True)
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
           sitemap=True)
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
           sitemap=True)
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
           sitemap=True)
    def register_issue(self, brand_ref, model_ref, complaint_ref, complaint_description_ref):
        return request.render("website_mobile_service.request_submit_wizard", {
            'brand': self._get_brand(brand_ref),
            'model': self._get_brand_model(model_ref),
            'complaint': self._get_complaint(complaint_ref),
            'complaint_description': self._get_complaint_description(complaint_description_ref)
        })

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
