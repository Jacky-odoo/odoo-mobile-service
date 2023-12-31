{
    'name': 'SMS Server Management',
    'version': '16.0.1.0.0',
    'summary': 'Module for managing SMS Server.',
    'category': 'Industries',
    'author': 'ViraWeb123',
    'company': 'ViraWeb123',
    'website': 'https://viraweb123.ir',
    'depends': [
        'base', 
        'mail',  
        'account',
        'sms'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/mobile_sms_server.xml',
        'wizards/res_config_settings_views.xml',
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