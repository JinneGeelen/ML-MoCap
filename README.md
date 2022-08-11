# ML-MoCap
Markerless Motion Capture Software required to build the low-cost, modular and multi-camera ML-MoCap system.

## Disclaimer

This project is work-in-progress. With the lessons learned from the first version of the ML-MoCap we decided to add a few improvements to make it more stable in use. In this list we keep track of the transition from version 0.1 to the first official release 1.0.

- [x] Transform from custom services to pre-build Docker applications
- [x] Management by Kubernetes
- [x] Transition from mountdrive to NFS and SMB
- [x] Customized Raspberry Pi OS Image files
- [ ] New UI Design

## Getting started

### Installation
#### Hardware
Depending on the application or goal the required hardware list will change. Here we list the hardware components used to build the first version of the ML-MoCap system for motion capture of hand movements as an example.

- 1x Raspberry Pi Board (Controller)
- 6x Raspberry Pi Board (Camera Module)
- 6x Raspberry Pi HQ Camera
- 6x PoE_Board Power Over Ethernet (POE) for Raspberry Pi
- 8x Ethernet cables (length depending on the distance between cameras)
- 1x Network Switch (PoE enabled)

#### Software

The operating system for the Raspberry Pi's will be installed with the Imager tool. Instead of the general Raspberry Pi OS we provide custum images including Docker installation of the required packages. Please follow the instruction documents for a set-by-step guided installation process.

1. [Installation Controller](Installation_Controller.md)
2. [Installation Camera Modules](Installation_CameraModules.md)
3. [Using the Application](Manual_WebApplication.md)

## Code contributors:
ML-MoCap code was originally developed by Tommy Maintz & Jinne Geelen. 

## References:
If you use this code we kindly ask you to cite us following [CITATION.cff](https://github.com/JinneGeelen/ML-MoCap/blob/main/CITATION.cff).

## License
Content is BSD-3-Clause licensed, as found in the [LICENSE.md](https://github.com/JinneGeelen/ML-MoCap/blob/feature/v2/LICENSE) file. Note that the software is provided "as is", without warranty of any kind, express or implied. If you use the code, please cite us.
