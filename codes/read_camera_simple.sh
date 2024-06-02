###
 # @Author: sun510001 sqf121@gmail.com
 # @Date: 2024-05-31 23:04:45
 # @LastEditors: sun510001 sqf121@gmail.com
 # @LastEditTime: 2024-06-01 17:36:12
 # @FilePath: /camera/codes/read_camera_simple.sh
 # @Description:
### 

dmesg | grep veye && \
echo "" && \
/home/sun/Desktop/camera/raspberrypi_v4l2/rpi5_scripts/find_entity.sh && \
echo "" && \
/home/sun/Desktop/camera/raspberrypi_v4l2/rpi5_scripts/media_setting_rpi5.sh veyecam2m -fmt UYVY -w 1920 -h 1080 && \
echo "" && \
cd /home/sun/Desktop/camera/raspberrypi_v4l2/i2c_cmd && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f devid -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f hdver -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f sensorid -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f wdrmode -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f videoformat -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f awbgain -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f daynightmode -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f mwbgain -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f new_expmode -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f new_mshutter -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f new_mgain -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f auto_shutter_max -b 4