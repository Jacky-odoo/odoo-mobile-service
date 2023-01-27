from odoo.http import Controller, route, request




class MobileService(Controller):

    @route('/mobile-service', type='http', auth="public", website=True, sitemap=True)
    def index(self):
        Brand = request.env['blog.blog']



        values = {}


        return request.render("website_mobile_service.brand_select_wizard", values)

