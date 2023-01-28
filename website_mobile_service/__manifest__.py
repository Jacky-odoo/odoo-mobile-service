{
    'name': 'Mobile Service Management Website Integeration',
    'version': '16.0.1.0.0',
    'summary': 'Module for connecting website into mobile service.',
    'category': 'Website',
    'author': 'ViraWeb123',
    'company': 'ViraWeb123',
    'website': 'https://viraweb123.ir',
    'depends': [
        'website',
        'mobile_service',
    ],
    'data': [
        # Data
        # Security
        # Templates
        'templates/website_brand_model.xml',
        'templates/website_brand.xml',
        'templates/website_complaint_description.xml',
        'templates/website_complaint.xml',
        'templates/website_submit.xml',
        # Views
        # Wizards
    ],
    'images': [],
    'assets': {},
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_frontend': [
            '/website_mobile_service/static/src/scss/breadcrumb.scss',
        ]
    },
}
