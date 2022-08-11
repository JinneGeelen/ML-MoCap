# Installation Controller

1. Download the [custom controller image](SD_images/mlmocap_controller.img.gz) file to build the controller operating system on the SD card.
2. Add the custom image to one of the SD cards with [Raspberry Pi Imager](https://www.raspberrypi.com/software/), make sure to change the settings (gear icon) before choosing write: 
    1. Change hostname into `mlmocap-controller`
    2. Select SSH enabled
    3. Choose prefererred username and password for your controller, defaults are: `pi` and `raspberry`
    4. Fill in the credentials of your WiFi network
    5. Save settings and now press write to flash the card, this takes a while wait for the progress to finish.
3. Insert the SD card into the controller Pi and connect the power supply

