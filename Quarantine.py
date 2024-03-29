import requests
import configparser
import json
import sys

def get_api_token():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config.get('API', 'token')

def quarantine_email(message_id):
    token = get_api_token()
    url_base = 'https://api.xdr.trendmicro.com'
    url_path = '/v3.0/response/emails/quarantine'
    query_params = {}
    headers = {'Authorization': 'Bearer ' + token,'Content-Type': 'application/json;charset=utf-8'}
    body = [{'messageId':  message_id}]
    r = requests.post(url_base + url_path, params=query_params, headers=headers, json=body)
    print(r.status_code)
    with open('response.log', 'a') as f:
        f.write(json.dumps(r.json()) + '\n')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: torgal.py <message_id>")
        sys.exit(1)
    message_id = sys.argv[1]
    quarantine_email(message_id)
