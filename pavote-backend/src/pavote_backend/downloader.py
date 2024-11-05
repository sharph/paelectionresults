#!/usr/bin/env python

import requests
import json
import time
import os
import shutil

from processor import process_election, publish_election

TS_URL = 'https://electionreturns.pa.gov/api/ElectionReturn/GetUpdatedTimeStamp?methodName=LastUpdatedTimeStamp'

ELECTION_URLS = {
    '2024_pa_presidential':
    'https://electionreturns.pa.gov/api/ElectionReturn/GetCountyBreak?officeId=1&districtId=1&methodName=GetCountyBreak&electionid=undefined&electiontype=undefined&isactive=undefined',
#    'Attorney General':
#    'https://electionreturns.pa.gov/api/ElectionReturn/GetCountyBreak?officeId=5&districtId=1&methodName=GetCountyBreak&electionid=undefined&electiontype=undefined&isactive=undefined',
#    'Auditor General':
#    'https://electionreturns.pa.gov/api/ElectionReturn/GetCountyBreak?officeId=6&districtId=1&methodName=GetCountyBreak&electionid=undefined&electiontype=undefined&isactive=undefined',
#    'State Treasurer':
#    'https://electionreturns.pa.gov/api/ElectionReturn/GetCountyBreak?officeId=7&districtId=1&methodName=GetCountyBreak&electionid=undefined&electiontype=undefined&isactive=undefined'
}

MODE = os.getenv('MODE', 'test')
SYNTHETIC = os.getenv('SYNTHETIC', 'True').lower() == 'true'
SLEEP_TIME = int(os.getenv('SLEEP_TIME', 60))


def main():
    with open("2020.json", "r") as f:
        data_2020 = json.load(f)
        processed = process_election(data_2020['Election']['Statewide'][0])
        publish_election(processed, '2020_pa_presidential')



    last_time = None
    last_data = None
    while True:
        ts = requests.get(TS_URL).json()
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
                processed = process_election(data['Election']['Statewide'][0], test=SYNTHETIC)
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
