
###
 # @Author: sun510001 sqf121@gmail.com
 # @Date: 2024-05-31 23:04:45
 # @LastEditors: sun510001 sqf121@gmail.com
 # @LastEditTime: 2024-06-01 10:21:40
 # @FilePath: /camera/codes/video_preview.sh
 # @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
### 
# gst-launch-1.0 v4l2src device=/dev/video0 ! "video/x-raw,format=(string)UYVY, width=(int)1280, height=(int)720,framerate=(fraction)30/1" ! videoconvert ! autovideosink sync=false -v
gst-launch-1.0 v4l2src device=/dev/video0 ! "video/x-raw,format=(string)UYVY, width=(int)1920, height=(int)1080,framerate=(fraction)30/1" ! videoconvert ! autovideosink sync=false -v