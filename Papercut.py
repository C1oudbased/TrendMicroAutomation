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
    delta = timedelta(hours=48)
    yesterday_time = datetime.now(timezone.utc) - delta
    yesterday_time_iso = yesterday_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    return yesterday_time_iso

def get_search_results():
    token = get_api_token()
    current_time_iso = get_current_time()
    yesterday_time_iso = get_yesterdays_time()
    url_base = 'https://api.xdr.trendmicro.com'
    url_path = '/v3.0/search/endpointActivities'
    query_params = {'startDateTime': yesterday_time_iso,'endDateTime': current_time_iso}
    additional_text = ' and logonUser:*'
    headers = {'Authorization': 'Bearer ' + token, 'TMV1-Query': 'endpointHostName:' + user_input + additional_text}
    try:
        return requests.get(url_base + url_path, params=query_params, headers=headers)
    except Exception as e:
        print(e)

user_input = input("Hostname: ")

response = get_search_results()
if response == None:
    exit()

def filter_response(response):
    print(response.status_code)
    parsed_json = []
    if response.ok:
        if 'application/json' in response.headers.get('Content-Type', '') and len((json_response := response.json())['items']):
            with open('output.txt', 'w') as file:
                for item in json_response['items']:
                    username = item['logonUser']
                    event_time = item['eventTimeDT']
                    file.write(f'User: {username}, Event Time: {event_time}\n')
                    parsed_json.append(username)
            print('Data written to file: output.txt')
        else:
            print('No relevant data found')
    else:
        print(f'Error {response.status_code}: {response.text}')
    return parsed_json

filter_response(response)