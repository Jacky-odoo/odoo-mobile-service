from odoo import models, fields, api, _
from odoo.addons.iap.tools import iap_tools
import requests


class MobileSms(models.AbstractModel):
    _inherit = "sms.api"
    
    @api.model
    def _send_sms(self, numbers, message):
        """ Send a single message to several numbers

        :param numbers: list of E164 formatted phone numbers
        :param message: content to send

        :raises ? TDE FIXME
        """
        serv = self.env['mobile_sms.server'].search([('id', '=', '1')])
        if serv:
            url = serv.url
            payload = {
                "username": serv.user_name,
                "password": serv.password,
                "Source": serv.source_tel,
                "Message": message,
                "destination": ','.join(numbers)
            }
            response = requests.request("POST", url, data=payload, timeout=5)
            return response
        else:
             params = {
            'numbers': numbers,
            'message': message,
        }
        return self._contact_iap('/iap/message_send', params)
        

        # params = {
        #    'numbers': numbers,
        #    'message': message,
        # }
        # return self._contact_iap('/iap/message_send', params)

    @api.model
    def _send_sms_batch(self, messages):
        """ Send SMS using IAP in batch mode

        :param messages: list of SMS to send, structured as dict [{
            'res_id':  integer: ID of sms.sms,
            'number':  string: E164 formatted phone number,
            'content': string: content to send
        }]

        :return: return of /iap/sms/1/send controller which is a list of dict [{
            'res_id': integer: ID of sms.sms,
            'state':  string: 'insufficient_credit' or 'wrong_number_format' or 'success',
            'credit': integer: number of credits spent to send this SMS,
        }]

        :raises: normally none
        """
        for message in messages:
            self._send_sms([message['number']], message['content'])

        params = {
            'messages': messages
        }
        return self._contact_iap('/iap/sms/2/send', params)
