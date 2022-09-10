import subprocess
import json


def get_enr_record():
    all_json_file = open('all_9_9.json', 'r')
    enr_ip_addresses_file = open('enr_ip_addresses.csv', 'a')
    all_json_contents = all_json_file.read()
    all_json = json.loads(all_json_contents)
    for node in all_json:
        enr_record = all_json[node]['record']
        ip_address = enr_decode(enr_record)
        enr_ip_addresses_file.write(node + ', ' + ip_address + '\n')


def enr_decode(enr_record):
    try:
        output = subprocess.check_output(['enr-cli', 'read', enr_record])
    except subprocess.CalledProcessError as err:
        print(err)
        return

    output = str(output)
    try:
        ip_address = output[output.index(r'\nIP:') + 5: output.index(r'\nTCP')]
    except ValueError:
        ip_address = output[output.index(r'\nIP:') + 5: output.index(r'\nUDP')]
    except Exception as err:
        print(err)
        return

    # return the IP address
    return ip_address


get_enr_record()
