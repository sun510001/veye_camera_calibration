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
./veye_mipi_i2c.sh -r -f mirrormode -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f denoise -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f agc -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f lowlight -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f daynightmode -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f ircutdir -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f irtrigger -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f mshutter -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f cameramode -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f nodf -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f capture -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f csienable -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f brightness -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f aespeed -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f contrast -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f saturation -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f sharppen -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f wdrsharppen -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f wdrtargetbr -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f boardmodel -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f wdrtargetbr -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f i2cwen -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f i2cauxenable -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f awbgain -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f wbmode -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f mwbgain -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f yuvseq -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f new_expmode -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f new_mshutter -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f new_mgain -b 4 && \
sleep .2 && \
./veye_mipi_i2c.sh -r -f auto_shutter_max -b 4
