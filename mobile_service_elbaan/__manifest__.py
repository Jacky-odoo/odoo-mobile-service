{
    'name': 'Mobile Service Elbaan Management',
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
        'security/ir.model.access.csv',
        'views/mobile_service_elbaan.xml',
    ],
    'images': [
        
    ],
     'assets': {
        'web.assets_backend': [
            'mobile_service_elbaan/static/src/css/mobile_service_elbaan.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}