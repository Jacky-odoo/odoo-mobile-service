{
    'name': 'Mobile Service Management',
    'version': '16.0.1.0.0',
    'summary': 'Module for managing mobile service shop daily activities.',
    'category': 'Industries',
    'author': 'ViraWeb123',
    'company': 'ViraWeb123',
    'website': 'https://viraweb123.ir',
    'depends': [
        'base', 
        'stock_account', 
        'mail', 
        'product', 
        'account'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/mobile_service_views.xml',
        'views/mobile_warranty_views.xml',
        'views/product_template.xml',
        'views/terms_and_condition.xml',
        'views/complaint_template.xml',
        'views/complaint_type.xml',
        'views/brand_models.xml',
        'views/brand.xml',
        'views/res_partner_views.xml',
        'wizard/mobile_create_invoice_views.xml',
        'reports/mobile_service_ticket.xml',
        'reports/service_ticket_template.xml',
        'data/accounting.xml',
        'data/mobile_service_data.xml',
        'data/mobile_service_email_template.xml'
    ],
    'images': [
        'static/description/banner.png'
    ],
    'assets': {
        'web.assets_backend': [
            'mobile_service/static/src/css/mobile_service.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}