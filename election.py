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
    for key in data:
        state = data[key]["statePostal"]
        officeId = data[key]["officeID"]
        officeName = data[key]["officeName"]
        if "seatName" in data[key]:
            seatName = data[key]["seatName"]
        if officeId == "I":
            tabulationStatus = data[key]["tabulationStatus"]
            if key not in last_status:
                last_status[key] = tabulationStatus
            elif last_status[key] != tabulationStatus:
                description = data[key]["description"]
                print(f"{state} - {officeName} - {seatName}")
                print(tabulationStatus)
                print(description)
                last_status[key] = tabulationStatus
        else:
            raceCallStatus = data[key]["raceCallStatus"]
            if key not in last_status:
                last_status[key] = raceCallStatus
            elif last_status[key] != raceCallStatus:
                if officeId == 'P' or officeId == 'G':
                    print(f"{state} - {officeName}")
                    print(raceCallStatus)
                else:
                    print(f"{state} - {officeName} - {seatName}")
                    print(raceCallStatus)
                last_status[key] = raceCallStatus

while True:
    get_election_data()
    time.sleep(5 * 60)