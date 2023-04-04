from odoo import models, fields, api, _
from odoo.addons.iap.tools import iap_tools
from odoo.addons.sms.models.sms_api import SmsApi
import requests
import json


class MobileSms(models.AbstractModel):
    _inherit = "sms.api"


    @api.model
    def _send_sms_batch(self, messages):
        """
        :param messages: list of SMS to send, structured as dict [{
            'res_id':  integer: ID of sms.sms,
            'number':  string: E164 formatted phone number,
            'content': string: content to send
        }]
        """
        params = self.env['ir.config_parameter'].sudo()
        if params.get_param('mobile_sms.server_special'):
            server_config_id = params.get_param('mobile_sms.server_id')
            server_config = self.env['mobile_sms.server'].search(
                [('id', '=', server_config_id)])
        else:
            server_config = False

        if server_config and server_config.server_type == 'asanak':
            response = self._send_by_asanak(server_config, messages)
        elif server_config and server_config.server_type == 'smsir':
            response = self._send_by_smsir(server_config, messages)
        else:
            response = super()._send_sms_batch(messages)
        return response


    def _send_by_asanak(self, confg, messages):
        result = []
        for message in messages:
            payload = {
                "username": confg.user_name,
                "password": confg.password,
                "Source": confg.source_tel,
                "Message": message['content'],
                "destination": message['number']
            }
            response = requests.request(
                "POST",
                url='https://panel.asanak.com/webservice/v1rest/sendsms',
                data=payload,
                timeout=5)
            if response.status_code == 200:
                if (response.content != 'Source Number is not valid') and (response.content != 'Username or Password is not valid'):
                    result.append({
                        'res_id': message['res_id'],
                        'state': 'success',
                        'credit': 5,
                    })
            else:
                result.append({
                    'res_id': message['res_id'],
                    'state': 'Un-success',
                    'credit': 5,
                })
        return result

    def _send_by_smsir(self, config, messages):
        result = []
        
        for message in messages:
            api_key = self.get_token_from_smsir(
                UserApiKey=config.api_key,
                SecretKey=config.security_code
            )
            
            headers = {
                'Content-type': 'application/json',
                'x-sms-ir-secure-token': api_key,
            }
            body = {
                "Messages": [message['content']],
                "MobileNumbers": [message['number']],
                "LineNumber": config.source_tel,
                "SendDateTime": "",
                "CanContinueInCaseOfError": "false",
            }
            response = requests.post(
                'https://RestfulSms.com/api/MessageSend', 
                data=json.dumps(body),
                headers=headers
            )
            if response.status_code == 201:
                if response.json()['IsSuccessful'] == True:  
                    result.append({
                        'res_id': message['res_id'],
                        'state': 'success',
                        'credit': 5,
                    })
                else:
                    result.append({
                    'res_id': message['res_id'],
                    'state': 'Un-success',
                    'credit': 5,
                })
            else:
                result.append({
                    'res_id': message['res_id'],
                    'state': 'Un-success',
                    'credit': 5,
                })
        return result



    def get_token_from_smsir(self, UserApiKey='', SecretKey=''):
        url = 'http://RestfulSms.com/api/Token'
        headers = {
            "Content-Type": "application/json",
        }
        body = {
            "UserApiKey": UserApiKey,
            "SecretKey": SecretKey
        }
        response = requests.post(url, data=json.dumps(body), headers=headers)
        if response.status_code == 201:
            if response.json()['IsSuccessful'] == True:
                secure_token = response.json()['TokenKey']
                print(secure_token)
                print("This is Sucsess")
                return secure_token
            print(response.content)
        return None
