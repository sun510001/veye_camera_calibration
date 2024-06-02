
###
 # @Author: sun510001 sqf121@gmail.com
 # @Date: 2024-05-31 23:04:45
 # @LastEditors: sun510001 sqf121@gmail.com
 # @LastEditTime: 2024-06-02 16:56:54
 # @FilePath: /camera/codes/video_preview.sh
 # @Description: record video by 1080p 30 fps
### 

# enter the right device
device=/dev/video0
####

current_time=$(date +"%Y-%m-%d_%H-%M-%S")
output_filename=../data/video_$current_time.mp4
gst_command="gst-launch-1.0 -e v4l2src io-mode=dmabuf device=$device ! \"video/x-raw,format=(string)UYVY, width=(int)1920, height=(int)1080,framerate=(fraction)30/1\" ! videoconvert ! x264enc bitrate=6200 speed-preset=veryfast tune=zerolatency ! 'video/x-h264, profile=high' ! h264parse ! mp4mux ! filesink location=$output_filename"

echo $"Press q to stop recording ..."
echo $"Command:"
echo $"$gst_command"
echo " "

eval "$gst_command" &

while true; do
    read -t 1 -n 1 -s key
    if [[ $key == "q" ]]; then
        echo $" "
        echo $"Terminating recording..."
        killall -SIGINT gst-launch-1.0
        break
    fi
done

wait $gst_pid
echo "Recording finished."