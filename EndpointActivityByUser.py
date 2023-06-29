import requests
import configparser
import json
import time
import sys
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
        end_time_iso = get_time_minutes_ago(minutes - 30)
        url_base = 'https://api.xdr.trendmicro.com'
        url_path = '/v3.0/search/endpointActivities'
        query_params = {'startDateTime': start_time_iso, 'endDateTime': end_time_iso, 'top': '5000'}
        additional_text = ' and logonUser:*'
        headers = {'Authorization': 'Bearer ' + token, 'TMV1-Query': 'endpointHostName:' + user_input + additional_text}
        try:
            response = requests.get(url_base + url_path, params=query_params, headers=headers)
            if response.ok:
                results.append(response)
                time.sleep(3)
            else:
                print(f'Error {response.status_code}: {response.text}')
        except Exception as e:
            print(e)

        print_progress(len(results), len(timeframes))

    print()
    return results


user_input = input("Hostname: ")


def filter_response(responses):
    for response in responses:
        print(response.status_code)
        unique_users = []
        duplicate_users = []

        if response.ok:
            if 'application/json' in response.headers.get('Content-Type', '') and len(
                    (json_response := response.json())['items']):
                with open('output.txt', 'a') as file:
                    for item in json_response['items']:
                        username = item['logonUser']
                        event_time = item['eventTimeDT']
                        if username not in unique_users and username not in duplicate_users:
                            file.write(f'User: {username}, Event Time: {event_time}\n')
                            unique_users.append(username)
                        elif username in unique_users:
                            unique_users.remove(username)
                            duplicate_users.append(username)

                print('Data written to file: output.txt')
            else:
                print('No relevant data found')
        else:
            print(f'Error {response.status_code}: {response.text}')


def print_progress(iteration, total):
    percent = int(100 * iteration / total)
    sys.stdout.write('\r')
    sys.stdout.write(f'Progress: [{percent:>{3}}%] {"=" * percent}{" " * (100 - percent)}')
    sys.stdout.flush()


responses = get_search_results()

total_iterations = len(responses)
for i, response in enumerate(responses, start=1):
    print_progress(i, total_iterations)

print()

filter_response(responses)
