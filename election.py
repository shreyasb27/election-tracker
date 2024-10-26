import requests
import json
import time

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
election_data_url = "https://interactives.apelections.org/election-results/data-live/2024-11-05/results/national/metadata.json"

last_status = {}

def get_election_data():
    response = requests.get(election_data_url)
    if response.status_code != 200:
        exit(0)
    data = json.loads(response.content)
    for state in states:
        key = f"20241105{state}0"
        race_call_status = data[key]["raceCallStatus"]
        if key not in last_status:
            last_status[key] = race_call_status
        elif last_status[key] != race_call_status:
            print(state, "changed status!")
            print(race_call_status, state)
            last_status[key] = race_call_status

while True:
    get_election_data()
    time.sleep(5 * 60)