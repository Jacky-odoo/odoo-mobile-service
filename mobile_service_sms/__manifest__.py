{
    'name': 'Mobile SMS Management',
    'version': '16.0.1.0.0',
    'summary': 'Module for managing mobile SMS Server.',
    'category': 'Industries',
    'author': 'ViraWeb123',
    'company': 'ViraWeb123',
    'website': 'https://viraweb123.ir',
    'depends': [
        'base', 
        'stock_account', 
        'mail', 
        'product', 
        'account',
        'sms'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/mobile_service_composer.xml',
        'views/mobile_sms_server.xml',
    ],
    'images': [
        
    ],
     'assets': {
        'web.assets_backend': [
           
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}