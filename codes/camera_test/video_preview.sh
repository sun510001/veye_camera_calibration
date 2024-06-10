
###
 # @Author: sun510001 sqf121@gmail.com
 # @Date: 2024-05-31 23:04:45
 # @LastEditors: sun510001 sqf121@gmail.com
 # @LastEditTime: 2024-06-09 15:02:21
 # @FilePath: /camera/codes/camera_test/video_preview.sh
 # @Description: 
### 
gst-launch-1.0 v4l2src device=/dev/video0 ! "video/x-raw,format=(string)UYVY, width=(int)1920, height=(int)1080,framerate=(fraction)30/1" ! videoconvert ! autovideosink sync=false -v
# gst-launch-1.0 v4l2src device=/dev/video8 ! "video/x-raw,format=(string)UYVY, width=(int)1920, height=(int)1080,framerate=(fraction)30/1" ! videoconvert ! autovideosink sync=false -v