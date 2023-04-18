import requests
import configparser
from datetime import datetime, timedelta, timezone


def get_api_token():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config.get('API', 'token')


def get_current_time():
    current_time = datetime.now(timezone.utc)
    current_time_iso = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    return current_time_iso


def get_yesterdays_time():
    delta = timedelta(hours=24)
    yesterday_time = datetime.now(timezone.utc) - delta
    yesterday_time_iso = yesterday_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    return yesterday_time_iso


def get_new_alerts():
    token = get_api_token()
    current_time_iso = get_current_time()
    yesterday_time_iso = get_yesterdays_time()
    url_base = 'https://api.xdr.trendmicro.com'
    url_path = '/v3.0/workbench/alerts'
    query_params = {'startDateTime': yesterday_time_iso,'endDateTime': current_time_iso}
    headers = {'Authorization': 'Bearer ' + token, 'TMV1-Filter': "investigationStatus eq 'New' and model eq 'Suspicious Email with Redirect Link Detected by Retro Scan'"}
    try:
        return requests.get(url_base + url_path, params=query_params, headers=headers)
    except Exception as e:
        print(e)


response = get_new_alerts()
if response == None:
    exit()


def filter_response(response):
    print(response.status_code)
    workbench_id = []
    if response.ok:
        if 'application/json' in response.headers.get('Content-Type', '') and len((json_response := response.json())['items']):
            for item in json_response['items']:
                id_value = item['id']
                print(f'ID: {id_value}')
                workbench_id.append(id_value)
        else:
            print('No alerts found')
    else:
        print(f'Error {response.status_code}: {response.text}')
    return workbench_id


def get_workbench_details(id_value):
    url_base = 'https://api.xdr.trendmicro.com'
    url_path = f'/v3.0/workbench/alerts/{id_value}'
    token = get_api_token()

    query_params = {}
    headers = {'Authorization': 'Bearer ' + token}

    response = requests.get(url_base + url_path, params=query_params, headers=headers)

    print(response.status_code)
    if 'application/json' in response.headers.get('Content-Type', '') and len((json_response := response.json())['indicators']):
        msg_id = json_response['indicators'][0]['value']
        print(f'msgID: {msg_id}')
    else:
        print(response.text)
    return msg_id


def quarantine_email(msg_id):
    url_base = 'https://api.xdr.trendmicro.com'
    url_path = '/v3.0/response/emails/quarantine'
    token = get_api_token()

    query_params = {}
    headers = {'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json;charset=utf-8'}
    email = {'messageId': msg_id}
    print(email)
    response = requests.post(url_base + url_path, params=query_params, headers=headers, json=[email])
    print(response.status_code)
    if 'application/json' in response.headers.get('Content-Type', '') and len(response.content):
        print(response.json())
    else:
        print(response.text)


ids = filter_response(response)
for id_value in ids:
    msg_id = get_workbench_details(id_value)
    print(msg_id)
    quarantine_email(msg_id)
