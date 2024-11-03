import requests
import json
import time
from escpos.printer import Usb
from datetime import datetime

election_data_url = "https://interactives.apelections.org/election-results/data-live/2024-11-05/results/national/metadata.json"

last_status = {}

p = Usb(0x0fe6,0x811e, 0, 0x81, 1)

def printRaceInfo(state, officeName, seatName, status, description):
    p.set_with_default(align = 'center', double_width=True, double_height=True)
    if seatName == None:
        p.textln(f"{state} - {officeName}")
    else:
        p.textln(f"{state} - {officeName} - {seatName}")
    
    p.set_with_default(align = 'center')
    p.textln(status)
    if description != None:
        p.textln(description)
    
    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    p.textln(f"Date and time: {date_time}")
    p.cut()


def get_election_data():
    response = requests.get(election_data_url)
    if response.status_code != 200:
        exit(0)
    data = json.loads(response.content)
    for key in data:
        state = data[key]["statePostal"]
        officeId = data[key]["officeID"]
        officeName = data[key]["officeName"]
        seatName = None
        if "seatName" in data[key]:
            seatName = data[key]["seatName"]
        if officeId == "I":
            tabulationStatus = data[key]["tabulationStatus"]
            if key not in last_status:
                last_status[key] = tabulationStatus
            elif last_status[key] != tabulationStatus:
                description = data[key]["description"]
                printRaceInfo(state, officeName, seatName, tabulationStatus, description)
                last_status[key] = tabulationStatus
        else:
            raceCallStatus = data[key]["raceCallStatus"]
            if key not in last_status:
                last_status[key] = raceCallStatus
            elif last_status[key] != raceCallStatus:
                printRaceInfo(state, officeName, seatName, raceCallStatus, None)
                last_status[key] = raceCallStatus

while True:
    get_election_data()
    time.sleep(1 * 60)
