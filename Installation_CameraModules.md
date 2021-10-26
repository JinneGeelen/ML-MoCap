# Installation Camera Modules

1. Download the [custom camera image](4TU?) file to build the camera module operating system on the SD cart. 
Note! The camera modules are installed one-by-one. Finish all steps for camA before you continue to install camB.
2. Add the custom image to one of the SD carts with [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
3. Connect power supply and insert the SD cart into the Pi
4. Change the hostname from 'cameraX' to the preferred incremental name in order of installation.
5. Check/Choose/Fix the IP address of the module (TBD)
6. Choose prefererred username and password for your controller
    1. Enter `sudo raspi-config` in a terminal window
    2. Select `Change user password`
    The default user on Raspberry Pi OS is `pi` with the password `raspberry`. You can change that here.
    3. Set the visible name for this Pi on a network
4. Add Remote Access
    1. Enter `sudo raspi-config` in a terminal window
    2. Select Interfacing Options
    3. Navigate to and select SSH
    4. Choose `Yes`
    5. Select `Ok`
    6. Choose `Finish`
5. Enable/disable the CSI camera interface.
