# Installation Camera Modules

1. Download the [custom camera image](SD_images/mlmocap_camera.img.gz) file to build the camera operating system on the SD card.
*Note!* The camera modules are installed one-by-one. Finish all steps for camera1 before you continue to install camera2, etc.
2. Add the custom image to one of the SD cards with [Raspberry Pi Imager](https://www.raspberrypi.com/software/), make sure to change the settings (gear icon) before choosing write, change [NR] for the current camera number that you want to install: 
    1. Change hostname into `mlmocap-camera[NR]`
    2. Select SSH enabled
    3. Choose prefererred username and password for your controller, defaults are: `pi` and `raspberry`
    4. Optional: Fill in the credentials of your WiFi network (controller will provide the network including WiFi settings.)
    5. Save settings and now press write to flash the card, this takes a while wait for the progress to finish.
3. Insert the SD card into the camera module Pi and connect it to the power supply (via PoE, just insert the ethernet cable).
4. Set a static and unique IP address:
    1. Connect to new camera module via ssh in your terminal type: `ssh pi@mlmocap-camera[NR].local`
    2. When prompted "Are you sure you want to continue", type: `yes`, enter
    3. Fill in password chosen in settings of Pi Imager, default: `raspberry`
    4. Open network settings by typing: `sudo nano /etc/dhcpcd.conf`
    5. Scroll down untill you see the internet settings, change [CAMERA NUMBER] to an increasing number above 10 and below 24, like camera1 = 11, camera2 = 12 etc. replace this row: `static ip_address=10.1.1.[CAMERA NUMBER]/24`
    6. To close and save the changes in this file:
    `Ctrl+x, then Y followed by Enter`
    7. Now reboot the camera module by typing: `sudo reboot`
    8. Reconnect to the camera with ssh, wait a few seconds for the module to finish restart: `ssh pi@mlmocap-camera[NR].local`
5. Add K3S to Camera module
    1. Open a second terminal, to connect to the controller: `ssh pi@mlmocap-controller.local`
    2. In this terminal (on the controller) get node-token, run following command: `sudo cat /var/lib/rancher/k3s/server/node-token`
    3. Copy the output
    4. Go to the terminal that is connected to the camera module. Add the copied token to the following command at [REPLACE WITH TOKEN]. Than paste the complete total to the current camera command line:
    `curl -sfL https://get.k3s.io | K3S_URL=https://10.1.1.1:6443 K3S_TOKEN=[REPLACE WITH TOKEN] sh -`
    5. Finally, we will change the node role, via controller. Go to the terminal connected to the controller and run this command after changing the current camera number: `kubectl label node mlmocap-camera[NR] kubernetes.io/role=camera`
    6. Connect to the webapp to see if the camera's appear, this might take a while, be patient :)






