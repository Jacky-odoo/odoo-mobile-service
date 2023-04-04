from odoo import models, fields, _

class MobileServiceSmsServer(models.Model):
    _name = 'mobile_sms.server'
    _description = 'Sms Server'
    _rec_name = 'name'

    name = fields.Char(
        string="Mobile Server",
        translate=True,
        trim=True,
        required=True)
    server_type = fields.Selection(
        selection=[('asanak', 'Asanak'),
                   ('smsir', 'Sms.ir')],
        string='Server Type',
        default='asanak',
        tracking=True)
    image = fields.Image(
        string="Image",
        max_height=800,
        max_width=800,
        verify_resolution=True,
        help="This image used in wizard")
    internal_ref = fields.Char(
        size=16,
        trim=True,
        translate=False,
        help="Used in url and internal usages",
        string="Internal Refrence",
        index=True,
        group_operator="count",
        required=True)
    url = fields.Char(
        string="Url for access",
        trim=True)
    user_name = fields.Char(
        string="User Name",
        trim=True)
    password = fields.Char(
        string="Password",
        trim=True)
    security_code = fields.Char(
        string="Security Code",
        trim=True)
    api_key = fields.Char(
        string="Api Key",
        trim=True)
    source_tel = fields.Char(
        string="Phone Source",
        trim=True,
        required=True)
    server_special = fields.Boolean(string="Special Server")
