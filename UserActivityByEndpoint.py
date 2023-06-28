import requests
import configparser
import json
import time
from datetime import datetime, timedelta, timezone


def get_api_token():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config.get('API', 'token')


def get_current_time():
    current_time = datetime.now(timezone.utc)
    current_time_iso = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    return current_time_iso


def get_time_minutes_ago(minutes):
    delta = timedelta(minutes=-minutes)
    past_time = datetime.now(timezone.utc) + delta
    past_time_iso = past_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    return past_time_iso


def get_search_results():
    token = get_api_token()
    current_time_iso = get_current_time()
    timeframes = [30 * i for i in range(1, 49)]
    results = []

    for minutes in timeframes:
        start_time_iso = get_time_minutes_ago(minutes)
        end_time_iso = get_time_minutes_ago(minutes-30)
        url_base = 'https://api.xdr.trendmicro.com'
        url_path = '/v3.0/search/endpointActivities'
        query_params = {'startDateTime': start_time_iso, 'endDateTime': end_time_iso, 'top': '5000'}
        additional_text = ' and endpointHostName:*'
        headers = {'Authorization': 'Bearer ' + token, 'TMV1-Query': 'logonUser:' + user_input + additional_text}
        try:
            response = requests.get(url_base + url_path, params=query_params, headers=headers)
            if response.ok:
                results.append(response)
                time.sleep(3)
            else:
                print(f'Error {response.status_code}: {response.text}')
        except Exception as e:
            print(e)
    
    return results


user_input = input("Username: ")


def filter_response(responses):
    for response in responses:
        print(response.status_code)
        unique_hosts = []
        duplicate_hosts = []

        if response.ok:
            if 'application/json' in response.headers.get('Content-Type', '') and len((json_response := response.json())['items']):
                with open('output.txt', 'a') as file:
                    for item in json_response['items']:
                        hostname = item['endpointHostName']
                        event_time = item['eventTimeDT']
                        if hostname not in unique_hosts and hostname not in duplicate_hosts:
                            file.write(f'Hostname: {hostname}, Event Time: {event_time}\n')
                            unique_hosts.append(hostname)
                        elif hostname in unique_hosts:
                            unique_hosts.remove(hostname)
                            duplicate_hosts.append(hostname)

                print('Data written to file: output.txt')
            else:
                print('No relevant data found')
        else:
            print(f'Error {response.status_code}: {response.text}')


responses = get_search_results()
filter_response(responses)
