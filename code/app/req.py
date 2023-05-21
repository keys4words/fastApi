import requests, os
from datetime import datetime, timedelta
import json


token_url = input('Enter token request url...')
client_id = input('Enter client id...')
client_secret = input('Enter client secret...')

form_data = {'user': 'value'}
token_res = requests.post(TOKEN_URL, data=form_data)
print(token_res.status_code, token_res.access_code)
os.environ['mytoken'] = token_res.access_code

base_api_url = input('Enter base api url...')
resource_url = input('Enter resource url...')
data_res = requests.get(
        os.path.join(base_api_url, resource_url),
        params = {
            'key': 'value'
            },
        headers = {
            'X-WSO2-Authorization': os.environ['mytoken']
            }
        )
print(data_res.status_code, data_res.text)
json_payload = json.loads(data_res.text)
