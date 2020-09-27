from pyicloud import PyiCloudService
import click
import sys
import time
import csv
import json
import os.path
from os import path
from datetime import datetime


def log():
    global api
    api = PyiCloudService('glaglasven@live.com', '')

    if api.requires_2sa:
        import click
        print("Two-step authentication required. Your trusted devices are:")

        devices = api.trusted_devices
        for i, device in enumerate(devices):
            print("  %s: %s" % (i, device.get('deviceName',
                "SMS to %s" % device.get('phoneNumber'))))

        device = devices[0]
        if not api.send_verification_code(device):
            print("Failed to send verification code")
            sys.exit(1)

        code = input("code: ")
        if not api.validate_verification_code(device, code):
            print("Failed to verify verification code")
            sys.exit(1)



def check_create_file(name):
    if path.exists('{}.csv'.format(name)) :
        return
    fields = 'Longitude', 'Latitude', 'person', 'time'
    with open('{}.csv'.format(name), 'w') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
        csvwriter.writeheader()
    return
    
def write_file(name, data):
    with open('{}.csv'.format(name), 'a+') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows([data])

def create_dic_friends_id():
    global ids
    ids = {}
    contacts = api.friends.contact_details
    for i in range(len(contacts)):
        ids[contacts[i]["id"]] = contacts[i]["firstName"]
    print(ids)
    
def get_name_from_id(id):
    global ids
    return ids[id]
    

log()
create_dic_friends_id()

while(True):
    log()
    locations = api.friends.locations

    nb_friends = len(locations)
    
    

    for i in range(nb_friends):
        location = locations[i]
        name='tracker'
        try:
            id = location["id"]
            check_create_file(name)
            lat = location["location"]["latitude"]
            lon = location["location"]["longitude"]
            timestamp = location["location"]["timestamp"]
            time_ = datetime.fromtimestamp(timestamp/1000)
            write_file(name, [lon, lat, get_name_from_id(id), time_])
        except:
            pass

    time.sleep(60)