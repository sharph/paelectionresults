#!/usr/bin/env python

import pytz
import requests
import json
import time
import os
import shutil
import datetime

from processor import process_philly, publish_election

ELECTION_URLS = {
    '2024_philly_presidential':
    'https://phillyresws.azurewebsites.us/ResultsAjax.svc/GetMapData?type=FED&category=PREC&raceID=2&osn=2&county=04&party=0&LanguageID=1',
}

MODE = 'test'
SYNTHETIC = True
SLEEP_TIME = int(os.getenv('SLEEP_TIME', 60))


def main():
    with open("2020_philly.json", "r") as f:
        data_2020 = json.load(f)
        processed = process_philly(data_2020)
        publish_election(processed, '2020_philly_presidential')

    last_time = None
    last_data = None
    while True:
        ts = datetime.datetime.now(pytz.timezone('US/Eastern')).isoformat()
        print('ts:', ts)
        if last_time != ts:
            last_time = ts
        else:
            continue
        out = {
            'elections': {},
            'mode': MODE
        }
        for name, url in ELECTION_URLS.items():
            print(name)
            out['elections'][name] = json.loads(requests.get(url).json()) if not SYNTHETIC else data_2020
            print('  ok')

        if last_data != out or SYNTHETIC:
            last_data = out
            for name, data in out['elections'].items():
                processed = process_philly(data)
                publish_election({
                    'data': processed,
                    'mode': MODE,
                    'time': ts
                }, name)
        else:
            print('data is the same')
            time.sleep(SLEEP_TIME)
            continue

        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
