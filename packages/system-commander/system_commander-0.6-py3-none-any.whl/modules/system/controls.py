import subprocess
import time

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

class system_operation:
    # current time
    def currentTime(self):
        local_time = time.localtime()
        date_time = time.strftime("%m/%d/%Y,%H:%M:%S", local_time)
        current_time = date_time.split(',')[1]
        return current_time

    # Loading animated dots
    def loadingAnimatedDots(self,number_of_dots, delay):
        for _ in range(number_of_dots):
            print(Color.BOLD + Color.FAIL + "·" + Color.ENDC, end="", flush=True)
            time.sleep(delay)

    # shutdown our system
    def shutdown(self):
        print(Color.BOLD + Color.WARNING + "System has shutdown now {}".format( self.currentTime()) + Color.ENDC)
        print(Color.BOLD + Color.WARNING + "Shutdowning" + Color.ENDC, end="")
        self.loadingAnimatedDots(8, 0.5)
        subprocess.run(["shutdown", "now"])

    # lock the screen
    def lock(self):
        print(Color.BOLD + Color.OKBLUE + "System has lock now {}".format(self.currentTime()) + Color.ENDC)
        print(Color.BOLD + Color.OKBLUE + "Locking" + Color.ENDC, end="")
        self.loadingAnimatedDots(8, 0.5)
        subprocess.run(["gnome-screensaver-command", "--lock"])

    # reboot our system
    def reboot(self):
        print(Color.BOLD + Color.OKGREEN + "System has reboot now {}".format(self.currentTime()) + Color.ENDC)
        print(Color.BOLD + Color.OKGREEN + "Rebooting" + Color.ENDC, end="")
        self.loadingAnimatedDots(8, 0.5)
        subprocess.run(["sudo", "reboot"])

    # logout our system
    def logout(self):
        print(Color.BOLD + Color.WARNING + "System has logout now {}".format(self.currentTime()) + Color.ENDC)
        print(Color.BOLD + Color.WARNING + "Loading" + Color.ENDC, end="")
        loadingAnimatedDots(8, 0.5)
        subprocess.run(["gnome-session-quit", "--logout", "--force"])

    # suspend is similar to lock the screen
    def suspend(self):
        print(Color.BOLD + "System has suspend now {}".format(self.currentTime()) + Color.ENDC)
        print(Color.BOLD + "Suspending" + Color.ENDC, end="")
        self.loadingAnimatedDots(8, 0.5)
        subprocess.run(["systemctl", "suspend"])

    # wifi on
    def wifiOn(self):
        print(Color.BOLD + Color.OKGREEN + "System WIFI has turn on now {}".format(self.currentTime()) + Color.ENDC)
        print(Color.BOLD + Color.OKGREEN + "Loading" + Color.ENDC, end="")
        self.loadingAnimatedDots(8, 0.5)
        subprocess.run(["nmcli", "radio", "wifi", "on"])

    # wifi off
    def wifiOff(self):
        print(Color.BOLD + Color.FAIL + "System wifi turn off {}".format(self.currentTime()) + Color.ENDC)
        print(Color.BOLD + Color.FAIL + "Loading" + Color.ENDC, end="")
        self.loadingAnimatedDots(8, 0.5)
        subprocess.run(["nmcli", "radio", "wifi", "off"])

    # bluetooth on
    def bluetoothOn(self):
        print(Color.BOLD + Color.OKBLUE + "System bluetooth turn on {}".format(self.currentTime()) + Color.ENDC)
        print(Color.BOLD + Color.FAIL + "Loading" + Color.ENDC, end="")
        self.loadingAnimatedDots(8, 0.5)
        subprocess.run(["sudo", "rfkill", "unblock", "bluetooth"])

    # bluetooth off
    def bluetoothOff(self):
        print(Color.BOLD + Color.FAIL + "System bluetooth has turned off {}".format(self.currentTime()) + Color.ENDC)
        print(Color.BOLD + Color.FAIL + "Loading" + Color.ENDC, end="")
        self.loadingAnimatedDots(8, 0.5)
        subprocess.run(["sudo", "rfkill", "block", "bluetooth"])

    # turn on airplane mode
    def airplaneModeOn(self):
        print(Color.BOLD + Color.WARNING + "System airplane mode has turned on {}".format(self.currentTime()) + Color.ENDC)
        print(Color.BOLD + Color.WARNING + "Loading" + Color.ENDC, end="")
        self.loadingAnimatedDots(8, 0.8)
        subprocess.run(["sudo", "rfkill", "block", "all"])

    # turn off airplane mode
    def airplaneModeOff(self):
        print(Color.BOLD + Color.OKGREEN + "System airplane mode has turned off {}".format(self.currentTime()) + Color.ENDC)
        print(Color.BOLD + Color.OKGREEN + "Loading" + Color.ENDC, end="")
        self.loadingAnimatedDots(8, 0.8)
        subprocess.run(["sudo", "rfkill", "unblock", "all"])