#! /usr/bin/python3

# importing libraries
import argparse
from .system.controls import system_operation

# main function
def main():
    system_controls = system_operation()
    
    parser = argparse.ArgumentParser(description="Control system actions")
    parser.add_argument("--type", "-t", required=True, choices=["shutdown", "lock", "reboot", "logout", "suspend", "wifiOn", "wifiOff", "bluetoothOn", "bluetoothOff", "airplaneModeOn", "airplaneModeOff"], help="")
    
    args = parser.parse_args()

    action = args.type

    if action == 'shutdown':
        system_controls.shutdown()
    elif action == 'lock':
        system_controls.lock()
    elif action == 'reboot':
        system_controls.reboot()
    elif action == 'logout':
        system_controls.logout()
    elif action == 'suspend':
        system_controls.suspend()   
    elif action == 'wifiOn':
        system_controls.wifiOn()
    elif action == 'wifiOff':
        system_controls.wifiOff()
    elif action == 'bluetoothOn':
        system_controls.bluetoothOn()
    elif action == 'bluetoothOff':
        system_controls.bluetoothOff()
    elif action == 'airplaneModeOn':
        system_controls.airplaneModeOn()
    elif action == 'airplaneModeOff':
        system_controls.airplaneModeOff()
    else:
       return "{} : invalid type".format(action)

