from odoo.http import Controller, route, request




class MobileService(Controller):

    @route('/mobile-service', type='http', auth="public", website=True, sitemap=True)
    def index(self):
        Brand = request.env['mobile.brand']
        brands = Brand.search([(1, "=", 1)])


        values = {
            'brands': brands
        }


        return request.render("website_mobile_service.brand_select_wizard", values)

