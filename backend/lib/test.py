#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import hakosim
import time
import math
import numpy
import pprint

import threading
import numpy as np
import cv2

import threading


def image_display_thread(client, fps=15):
    interval = 1.0 / fps
    while True:
        start_time = time.time()

        try:
            response = client.simGetImage("0", hakosim.ImageType.Scene)
            if response:
                img_np = np.frombuffer(response, dtype=np.uint8)
                img_rgb = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

                if img_rgb is None or img_rgb.size == 0:
                    print("Error: Failed to decode image")
                else:
                    cv2.imshow("Camera View", img_rgb)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            else:
                print("Error: No image received from client")

        except Exception as e:
            print(f"Error: {e}")

        elapsed_time = time.time() - start_time
        wait_time = max(0, interval - elapsed_time)
        time.sleep(wait_time)

    cv2.destroyAllWindows()

def transport(client, baggage_pos, transfer_pos):
    client.moveToPosition(baggage_pos['x'], baggage_pos['y'], 3, 5, -90)
    client.moveToPosition(baggage_pos['x'], baggage_pos['y'], 3, 5)
    client.moveToPosition(baggage_pos['x'], baggage_pos['y'], 3, 5, 0)
    client.moveToPosition(baggage_pos['x'], baggage_pos['y'], 0.7, 5, 0)
    client.grab_baggage(True)
    client.moveToPosition(baggage_pos['x'], baggage_pos['y'], 3, 5)
    client.moveToPosition(transfer_pos['x'], transfer_pos['y'], 3, 5)
    client.moveToPosition(transfer_pos['x'], transfer_pos['y'], transfer_pos['z'], 5)
    client.grab_baggage(False)
    client.moveToPosition(transfer_pos['x'], transfer_pos['y'], 3, 5)

def debug_pos(client):
    pose = client.simGetVehiclePose()
    print(f"POS  : {pose.position.x_val} {pose.position.y_val} {pose.position.z_val}")
    roll, pitch, yaw = hakosim.hakosim_types.Quaternionr.quaternion_to_euler(pose.orientation)
    print(f"ANGLE: {math.degrees(roll)} {math.degrees(pitch)} {math.degrees(yaw)}")

def parse_lidarData(data):

    # reshape array of floats to array of [X,Y,Z]
    points = numpy.array(data.point_cloud, dtype=numpy.dtype('f4'))
    points = numpy.reshape(points, (int(points.shape[0]/3), 3))
    
    return points


def main():
    """
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <config_path>")
        return 1

    client = hakosim.MultirotorClient(sys.argv[1])
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)

    """

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <config_path>")
        return 1

    # connect to the HakoSim simulator
    client = hakosim.MultirotorClient(sys.argv[1])
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)

    
    #image_display_thread(client)

    # カメラ画像表示スレッドを開始
    image_thread = threading.Thread(target=image_display_thread, args=(client, 15))
    image_thread.daemon = True  # メインスレッド終了時に自動終了
    image_thread.start()

    lidarData = client.getLidarData()
    if (len(lidarData.point_cloud) < 3):
        print("\tNo points received from Lidar data")
    else:
        print(f"len: {len(lidarData.point_cloud)}")
        points = parse_lidarData(lidarData)
        print("\tReading: time_stamp: %d number_of_points: %d" % (lidarData.time_stamp, len(points)))
        print("\t\tlidar position: %s" % (pprint.pformat(lidarData.pose.position)))
        print("\t\tlidar orientation: %s" % (pprint.pformat(lidarData.pose.orientation)))
    
        #lidar_z = lidarData.pose.position.z_val
        condition = numpy.logical_and(points <= 2, points > 0)
        filtered_points = points[numpy.any(condition, axis=1)]

        print(filtered_points)
    
    

    client.takeoff(3)
    baggage_pos = { "x": 0, "y": 3 }
    transfer_pos = { "x": 0, "y": -1, "z": 0.7 }
    #transport(client, baggage_pos, transfer_pos)
    debug_pos(client)
    

    client.simSetCameraOrientation("0",15)

    baggage_pos = { "x": 0, "y": 4 }
    transfer_pos = { "x": 0, "y": -1, "z": 1.2 }
    #transport(client, baggage_pos, transfer_pos)
    debug_pos(client)

    
    client.moveToPosition(0, 0, 0, 0)
    debug_pos(client)
    time.sleep(3)
    
    string = input("文字列を入力してください:")
    if string == "green":
        for i in range(100):
            client.moveToPosition(20, -3, 0.3, 5)
            debug_pos(client)
            time.sleep(3)
            client.moveToPosition(40, -3, 0.3, 5)
            debug_pos(client)
            time.sleep(3)
            client.moveToPosition(40, -18, 0.3, 5)
            debug_pos(client)
            time.sleep(3)
            client.moveToPosition(20, -18, 0.3, 5)
            debug_pos(client)
            time.sleep(3)
    elif string == "pink":
        for i in range(100):
            client.moveToPosition(-11, -3, 0.3, 5)
            debug_pos(client)
            time.sleep(3)
            client.moveToPosition(-30, -3, 0.3, 5)
            debug_pos(client)
            time.sleep(3)
            client.moveToPosition(-30, -18, 0.3, 5)
            debug_pos(client)
            time.sleep(3)
            client.moveToPosition(-11, -18, 0.3, 5)
            debug_pos(client)
            time.sleep(3)
    

    lidarData = client.getLidarData()
    if (len(lidarData.point_cloud) < 3):
        print("\tNo points received from Lidar data")
    else:
        print(f"len: {len(lidarData.point_cloud)}")
        points = parse_lidarData(lidarData)
        print("\tReading: time_stamp: %d number_of_points: %d" % (lidarData.time_stamp, len(points)))
        print("\t\tlidar position: %s" % (pprint.pformat(lidarData.pose.position)))
        print("\t\tlidar orientation: %s" % (pprint.pformat(lidarData.pose.orientation)))
    
        #lidar_z = lidarData.pose.position.z_val
        condition = numpy.logical_and(points <= 2, points > 0)
        filtered_points = points[numpy.any(condition, axis=1)]

        print(filtered_points)


    png_image = client.simGetImage("0", hakosim.ImageType.Scene)
    if png_image:
        with open("scene.png", "wb") as f:
            f.write(png_image)

    client.simSetCameraOrientation("0",-90)

    client.land()
    debug_pos(client)

    
    


    return 0

if __name__ == "__main__":
    sys.exit(main())
