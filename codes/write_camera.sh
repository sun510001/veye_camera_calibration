dmesg | grep veye && \
echo "" && \
/home/sun/Desktop/camera/raspberrypi_v4l2/rpi5_scripts/find_entity.sh && \
echo "" && \
/home/sun/Desktop/camera/raspberrypi_v4l2/rpi5_scripts/media_setting_rpi5.sh veyecam2m -fmt UYVY -w 1920 -h 1080 && \
echo "" && \
cd /home/sun/Desktop/camera/raspberrypi_v4l2/i2c_cmd && \
sleep .2 && \
./veye_mipi_i2c.sh -w -f new_expmode -p1 1 -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -w -f new_mshutter -p1 9000 -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -w -f new_mgain -p1 9.0 -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -w -f paramsave -b 4