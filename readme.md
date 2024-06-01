<!--
 * @Author: sun510001 sqf121@gmail.com
 * @Date: 2024-05-31 23:04:45
 * @LastEditors: sun510001 sqf121@gmail.com
 * @LastEditTime: 2024-06-01 11:13:26
 * @FilePath: /camera/readme.md
 * @Description: 
-->
# test VEYE-IMX-462 camera
[Camera Data Sheet](https://wiki.veye.cc/index.php/VEYE-MIPI-IMX462_Data_Sheet)
## Installing enviroment
Install Opencv 4.9.0, Opencv_contrib 4.9.0 and GStreamer plugin.
URL: [树莓派5 安装opencv和gstreamer插件](https://www.sqf.icu/article/1d04a080-16d9-4aaa-b386-27009bbdd612)


## Setting camera
If you use VEYE-IMX-462 at the first time, use [VEYE WIKI V4L2_mode_for_Raspberry_Pi](https://wiki.veye.cc/index.php/V4L2_mode_for_Raspberry_Pi) to install camera sdk.\
Use `./write_camera.sh` to set camera parameters.(check `-b` [bus number](https://wiki.veye.cc/index.php/I2c_bus_number_and_video_node))

## Loading camera to get images
```shell
python get_camera_frames.py
```
