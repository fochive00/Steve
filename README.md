# Getting start

 - [Clone repository](#clone-repository)
 - [Install dependencies](#install-dependencies)
 - [Launch Minecraft](#launch-minecraft)
 - [Setup OBS Studio](#setup-obs-studio)
 - [Run Script](#run-script)
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

In Windows:
```cmd
$ pip install opencv-python
```
***

### Launch Minecraft
 - Launch Minecraft
 - Start a new world and pause(press ESC).
***

### Setup OBS Studio

[Get OBS-Studio](https://obsproject.com/)

#### Settings -> Output:

 - Set the **Output Mode** to *Advanced*

#### Settings -> Output -> Recording:

 - Set the **File path or URL** to *udp://localhost:2000*
 - Set the **Container Format** to *mpegts*
 - Reduce the  **Video Bitrate** to 500~1000Kbps for better performance.

![demo1](https://github.com/fochive00/Steve/blob/main/imgs/obs-studio-recording-setting.png)

#### Settings -> Video:

 - Set the **Integer FPS Value** to *20* or lower.
 - Set the **Output(Scaled) Resolution** to a quiet small one.

#### Apply settings and get back to main window:
 - Add a new **screen capture** sourse and select the Minecraft window.
 - Start Recording.
<font color=#eeee00>(Note that there is not 'Start Streaming')
</font>

***
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



