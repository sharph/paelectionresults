import json
import pprint
import redis
import random
import os

def normalize_name(name):
    return name[0] + name[1:].lower()

def process_election(data, test=False):
    counties = {}
    for name, county in data.items():
        name = normalize_name(name)
        counties[name] = {}
        zero = random.random() > 0.5
        for party in ['dem', 'rep', 'lib', 'grn']:
            counties[name][party.lower()] = int(sum(
                map(
                    lambda x: int(x['Votes']),
                    filter(lambda x: x['PartyName'] == party.upper(), county)
                )
            ) * ((random.random() + 0.5 if not zero else 0) if test else 1))
    return counties

def process_philly(data, test=False):
    divisions = {}
    for result in data:
        division = result['PrecinctName'][:5]
        if division not in divisions:
            divisions[division] = {
                'dem': 0, 'rep': 0, 'lib': 0, 'grn': 0
            }
        zero = int(result['PrecinctNumber']) % 10 < 5
        divisions[division][result['PartyCode'].lower()] = int(result['calcCandidateVotes'] * (
            (random.random() + 0.5 if not zero else 0) if test else 1
        ))
    return divisions

def publish_election(msg, topic):
    client = redis.Redis(os.getenv('REDIS_HOST', 'localhost'), 6379)
    message = json.dumps({
        "topic": topic,
        "message": msg,
    })
    client.set(f"pubsub_{topic}", message)
    client.publish("pubsub", message)


if __name__ == '__main__':
    with open('2020.json', 'r') as f:
        pprint.pprint(
            process_election(json.load(f)['Election']['Statewide'][0])
        )
