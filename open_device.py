# -*- coding: utf-8 -*-
# @File    : open_device.py
# @Author  : lukasvondev
# @Date    : 2021/4/17
# @Env     : PyCharm
"""
    - This python script aims to open Azure Kinect DK device
    - and show image via OpenCV API.
"""
import cv2 as cv
import k4a


# detect azure kinect device is standby or not
def detect_device():
    deviceCount = k4a.Device.get_device_count()
    if deviceCount == 0:
        print("no azure kinect detected.")
        return 0
    else:
        print(f"{deviceCount} azure kinect detected.")
        return deviceCount


if __name__ == '__main__':

    count = detect_device()
    if count:
        device = k4a.Device.open(0)
        print(device.serial_number)
        print(device.hardware_version)
        print(device.color_ctrl_cap)

        # camera configuration
        device_config = k4a.DeviceConfiguration(color_format=k4a.EImageFormat.COLOR_BGRA32,
                                                color_resolution=k4a.EColorResolution.RES_1080P,
                                                depth_mode=k4a.EDepthMode.WFOV_2X2BINNED,
                                                camera_fps=k4a.EFramesPerSecond.FPS_15,
                                                synchronized_images_only=True,
                                                depth_delay_off_color_usec=0,
                                                wired_sync_mode=k4a.EWiredSyncMode.STANDALONE,
                                                subordinate_delay_off_master_usec=0,
                                                disable_streaming_indicator=False)

        status = device.start_cameras(device_config)
        if status != k4a.EStatus.SUCCEEDED:
            exit(-1)

        cv.namedWindow("Color Image")
        cv.resizeWindow("Color Image", 640, 360)
        cv.namedWindow("Depth Image")

        while True:
            capture = device.get_capture(-1)
            color_image = capture.color
            color_image_data = color_image.data
            depth_image = capture.depth
            depth_image_data = depth_image.data  # depth image format: uint16

            color_image_data = cv.cvtColor(color_image_data, cv.COLOR_RGBA2RGB)

            depth_color_image = cv.convertScaleAbs(depth_image_data, alpha=0.08)
            depth_color_image = cv.applyColorMap(depth_color_image, cv.COLORMAP_JET)

            color_image_data = cv.resize(color_image_data, (640, 360))

            cv.imshow("Color Image", color_image_data)
            cv.imshow("Depth Image", depth_color_image)

            key = cv.waitKey(3)

            # press ESC exit
            if key == 27:
                color_image.__del__()
                depth_image.__del__()
                device.close()
                cv.destroyAllWindows()
                break


