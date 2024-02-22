#! /usr/bin/python3

# importing libraries
import argparse
import subprocess
import time
import os

# ANSI escape codes for text formatting
class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# current time
def currentTime():
    local_time = time.localtime()
    date_time = time.strftime("%m/%d/%Y,%H:%M:%S", local_time)
    current_time = date_time.split(',')[1]
    return current_time

# Loading animated dots
def loadingAnimatedDots(number_of_dots, delay):
    for _ in range(number_of_dots):
        print(Color.BOLD + "·" + Color.ENDC, end="", flush=True)
        time.sleep(delay)

# shutdown our system
def shutdown():
    print(Color.BOLD + Color.WARNING + "System has shutdown now {}".format(currentTime()) + Color.ENDC)
    print(Color.BOLD + Color.WARNING + "Shutdowning " + Color.ENDC, end="")
    loadingAnimatedDots(4, 0.5)
    subprocess.run(["shutdown", "now"])

# lock the screen
def lock():
    print(Color.BOLD + Color.OKBLUE + "System has lock now {}".format(currentTime()) + Color.ENDC)
    print(Color.BOLD + Color.OKBLUE + "Locking " + Color.ENDC, end="")
    loadingAnimatedDots(4, 0.5)
    subprocess.run(["gnome-screensaver-command", "--lock"])

# reboot our system
def reboot():
    print(Color.BOLD + Color.OKGREEN + "System has reboot now {}".format(currentTime()) + Color.ENDC)
    print(Color.BOLD + Color.OKGREEN + "Rebooting " + Color.ENDC, end="")
    loadingAnimatedDots(4, 0.5)
    subprocess.run(["sudo", "reboot"])

# logout our system
def logout():
    print(Color.BOLD + Color.WARNING + "System has logout now {}".format(currentTime()) + Color.ENDC)
    print(Color.BOLD + Color.WARNING + "Loading " + Color.ENDC, end="")
    loadingAnimatedDots(4, 0.5)
    subprocess.run(["gnome-session-quit", "--logout", "--force"])

# suspend is similar to lock the screen
def suspend():
    print(Color.BOLD + "System has suspend now {}".format(currentTime()) + Color.ENDC)
    print(Color.BOLD + "Suspending " + Color.ENDC, end="")
    loadingAnimatedDots(4, 0.5)
    subprocess.run(["systemctl", "suspend"])

# wifi on
def wifiOn():
    print(Color.BOLD + Color.OKGREEN + "System WIFI has turn on now {}".format(currentTime()) + Color.ENDC)
    print(Color.BOLD + Color.OKGREEN + "Loading " + Color.ENDC, end="")
    loadingAnimatedDots(4, 0.5)
    subprocess.run(["nmcli", "radio", "wifi", "on"])

# wifi off
def wifiOff():
    print(Color.BOLD + Color.FAIL + "System wifi turn off {}".format(currentTime()) + Color.ENDC)
    print(Color.BOLD + Color.FAIL + "Loading " + Color.ENDC, end="")
    loadingAnimatedDots(4, 0.5)
    subprocess.run(["nmcli", "radio", "wifi", "off"])

# bluetooth on
def bluetoothOn():
    print(Color.BOLD + Color.OKBLUE + "System bluetooth turn on {}".format(currentTime()) + Color.ENDC)
    print(Color.BOLD + Color.FAIL + "Loading " + Color.ENDC, end="")
    loadingAnimatedDots(4, 0.5)
    subprocess.run(["sudo", "rfkill", "unblock", "bluetooth"])

# bluetooth off
def bluetoothOff():
    print(Color.BOLD + Color.FAIL + "System bluetooth has turned off {}".format(currentTime()) + Color.ENDC)
    print(Color.BOLD + Color.FAIL + "Loading " + Color.ENDC, end="")
    loadingAnimatedDots(4, 0.5)
    subprocess.run(["sudo", "rfkill", "block", "bluetooth"])

# turn on airplane mode
def airplaneModeOn():
    print(Color.BOLD + Color.WARNING + "System airplane mode has turned on {}".format(currentTime()) + Color.ENDC)
    print(Color.BOLD + Color.WARNING + "Loading " + Color.ENDC, end="")
    loadingAnimatedDots(6, 0.6)
    subprocess.run(["sudo", "rfkill", "block", "all"])

# turn off airplane mode
def airplaneModeOff():
    print(Color.BOLD + Color.OKGREEN + "System airplane mode has turned off {}".format(currentTime()) + Color.ENDC)
    print(Color.BOLD + Color.OKGREEN + "Loading " + Color.ENDC, end="")
    loadingAnimatedDots(6, 0.6)
    subprocess.run(["sudo", "rfkill", "unblock", "all"])

# main function
def main():
    parser = argparse.ArgumentParser(description="Control system actions")
    parser.add_argument("--type", "-t", required=True, choices=["shutdown", "lock", "reboot", "logout", "suspend", "wifiOn", "wifiOff", "bluetoothOn", "bluetoothOff", "airplaneModeOn", "airplaneModeOff"], help="")
    
    args = parser.parse_args()

    action = args.type

    if action == 'shutdown':
        shutdown()
    elif action == 'lock':
        lock()
    elif action == 'reboot':
        reboot()
    elif action == 'logout':
        logout()
    elif action == 'suspend':
        suspend()   
    elif action == 'wifiOn':
        wifiOn()
    elif action == 'wifiOff':
        wifiOff()
    elif action == 'bluetoothOn':
        bluetoothOn()
    elif action == 'bluetoothOff':
        bluetoothOff()
    elif action == 'airplaneModeOn':
        airplaneModeOn()
    elif action == 'airplaneModeOff':
        airplaneModeOff()
    else:
        pass
        # help()

if __name__ == "__main__":
    main()
