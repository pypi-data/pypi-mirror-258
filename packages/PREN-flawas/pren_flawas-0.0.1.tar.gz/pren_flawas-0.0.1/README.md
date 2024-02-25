# PREN 2023/24

The task is to develop a device which, from a random, given pattern of (3D)
dice arrangements at a remote location (e.g. in another room / city etc.) to create an exact copy
of the colors and positions of the cubes as precisely and quickly as possible. The copy of the arrangement
should be created inside the device and be visually and physically accessible from the outside.

## Components

Required Hardware and software. Our product was built with the following hardware components:

[Raspberry Pi 2B](https://www.raspberrypi.com/products/raspberry-pi-2-model-b/) with LAN connection or
[Raspberry Pi 4B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) with LAN or WiFi connection

[200x200 1.54inch E-Ink Raw Schwarz / Weiss e-Paper Display](https://www.bastelgarage.ch/200x200-1-54inch-e-ink-raw-schwarz-weiss-e-paper-display?search=200x200%201.54inch%20e-ink%20raw%20schwarz%20%2F%20weiss%20e-paper%20displa)

[Universal Raw e-Paper Driver HAT Adapter](https://www.bastelgarage.ch/universal-raw-e-paper-driver-hat-adapter?search=Universal%20Raw%20e-Paper%20Driver%20HAT%20Adapter)

[Shelly Pro 1 PM](https://www.shelly.com/de-ch/products/product-overview/shelly-pro-1pm)


## Installation

```bash
sudo apt update
sudo apt upgrade
sudo apt-get install xrdp
sudo apt install git
sudo apt-get install python3
sudo apt -y install python3-pil
sudo pip3 install PyObjC
```

## Authors

- [@JuliaVonM](https://github.com/JuliaVonM)
- [@Mangosil](https://github.com/Mangosil)
- [@flawas](https://github.com/flawas)
