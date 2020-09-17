import csv


# Uses CSV File
def devices_by_submaps(submaps):
    device_list = list()

    with open('Devices.csv') as file:
            reader = csv.reader(file)
            for line in reader:
                if line[5] != '':
                    if line[5] in submaps:

                        device = dict()
                        device['ip'] = line[2]
                        device['ip'] = device['ip'].split(',')[0]

                        device['name'] = line[1]

                        device['map'] = line[5]

                        device['MAC'] = line[3]

                        device['type'] = line[4]
                        device_list.append(device)


    found_devices = list()
    filtered_devices = list()
    final_devices = list()

    with open('foreign_devices.txt') as file:
        reader = csv.reader(file)
        for line in reader:
            for device in device_list:
                if line[0] in device['MAC']:
                    found_devices.append(device['name'])

    for device in device_list:
        if device['name'] not in found_devices:
            filtered_devices.append(device)

    for device in filtered_devices:
        if 'UBNT' not in device['type']:
            final_devices.append(device)

    return final_devices


def mac_lookup(mac_address):



def mikrotik_filer(devices):

    found_devices = list()
    filtered_devices = list()
    final_devices = list()

    with open('foreign_devices.txt') as file:
        reader = csv.reader(file)
        for line in reader:
            for device in devices:
                if line[0] in device['MAC']:
                    found_devices.append(device['name'])

    for device in devices:
        if device['name'] not in found_devices:
            filtered_devices.append(device)

    for device in filtered_devices:
        if device not in filtered_devices:
            if 'UBNT' not in device['type']:
                final_devices.append(device)

    return final_devices
