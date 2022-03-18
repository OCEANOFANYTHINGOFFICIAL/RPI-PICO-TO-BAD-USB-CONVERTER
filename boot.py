from board import *
import digitalio
import storage
# Naming The Usb Drive
#storage.remount("/", readonly=False)
#m = storage.getmount("/")
#m.label = "USB Rubber Ducky"
#storage.remount("/", readonly=True)
#storage.enable_usb_drive()
noStorageStatus = False
noStoragePin = digitalio.DigitalInOut(GP15)
noStoragePin.switch_to_input(pull=digitalio.Pull.UP)
noStorageStatus = not noStoragePin.value
if(noStorageStatus == True):
    # don't show USB drive to host PC
    storage.disable_usb_drive()
    print("Disabling USB Drive")
else:
    # normal boot
    print("USB Drive Enabled")