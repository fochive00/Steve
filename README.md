# Getting start

 - Clone repository
 - Install dependencies
 - Setup OBS-Studio
 - Launch Minecraft
 - Run Script
***
### Clone repository
```sh
$ git clone https://github.com/fochive00/Steve
```
***

### Install dependencies
In Linux:
```sh
$ pip install libevdev opencv-python
```
***

### Setup OBS-Studio
Firtst, 
OBS-Studio -> Settings -> Output -> Recording:

 - set **File path or URL** to *udp://localhost:2000*

 - set **Container Format** to *mpegts*

![demo1](https://github.com/fochive00/Steve/raw/main/imgs/obs-studio-recording-setting.png)
***

### Launch Minecraft
Start a new world and pause(press ESC). Wait until the script runing, then back to game.

### Run script
In project directory:
```sh
$ python main.py
```

After doing this, you have about 5 seconds to switch to the game window.

***

### TODO
 - Add more comments
 - Perfect the Documentation
 - Play



