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
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',

        # views
        'views/dashboard.xml',   #contains basic menuse and root struct
        'views/brand_model.xml',
        'views/brand.xml',
        'views/complaint.xml',
        'views/complaint_description.xml',
        'views/product.xml',
        'views/res_partner.xml',
        'views/service.xml',
        'views/term_condition.xml',
        'views/warranty.xml',

        # Templates

        # Wizards
        'wizard/mobile_create_invoice.xml',

        # Reports
        'reports/mobile_service_ticket.xml',
        'reports/service_ticket_template.xml',

        # Data
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