import werkzeug

from odoo.http import Controller, route, request



class MobileService(Controller):

    @route('/mobile-service', type='http', auth="public", website=True, sitemap=True)
    def brand_select(self):
        Brand = request.env['mobile.brand']
        brands = Brand.search([(1, "=", 1)])

        values = {
            'brands': brands
        }
        return request.render("website_mobile_service.brand_select_wizard", values)


    @route('/mobile-service/<string:ref>', type='http', auth="public", website=True, sitemap=True)
    def brand_model_select(self, ref):
        Brand = request.env['mobile.brand']
        brands = Brand.search([("internal_ref", "=", ref)])

        if len(brands) != 1:
            raise werkzeug.exceptions.NotFound()

        values = {
            'brand': brands[0],
            'models': brands[0].model_ids
        }
        return request.render("website_mobile_service.brand_model_select_wizard", values)