import http.client
import json
from artd_partner.models import Partner
from artd_infobip.models import InfobipCredential, InfobipSMS

class InfobipUtil:
    __partner = None
    __endpoint_url = None
    __api_key = None
    __infobip_credential = None
    __headers = None
    __connection = None
    __country_code = None

    def __init__(self, partner:Partner):
        self.__partner = partner
        city = self.__partner.city
        region = city.region
        country = region.country
        self.__country_code = country.phone_code
        self.__infobip_credential = InfobipCredential.objects.filter(partner=self.__partner, status=True).last()
        self.__endpoint_url = self.__infobip_credential.endpoint_url
        self.__api_key = self.__infobip_credential.api_key
        self.__connection = http.client.HTTPSConnection(self.__endpoint_url)
        self.__headers = {
            'Authorization': f'App {self.__api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def send_sms(self, to, message):
        payload = json.dumps({
            "messages": [
                {
                    "destinations": [{"to":f"{self.__country_code}{to}"}],
                    "from": "ServiceSMS",
                    "text": message
                }
            ]
        })
        self.__connection.request("POST", "/sms/2/text/advanced", payload, self.__headers)
        res = self.__connection.getresponse()
        data = res.read()
        response = json.loads(data.decode("utf-8"))
        InfobipSMS.objects.create(
            infobip_credential=self.__infobip_credential,
            message_id=response['messages'][0]['messageId'],
            to=to,
            message=message,
            response=response
        )
        print(response)


