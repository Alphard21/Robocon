#!/usr/bin/env python
from tutorials.srv import lidar, lidarRequest
import rospy

def lidar_scan():
    rospy.wait_for_service('scan')
    lidar_service = rospy.ServiceProxy('scan', lidar)
    coordinates = [(x,y)]
    for coord in coordinates:
        request = lidarRequest()
        request.centerX = coord[0]
        request.centerY = coord[1]
        response = lidar_service(request)
        lidar_readings = response.lidar_array
        for i in range(0, len(lidar_readings), 2):
            angle = lidar_readings[i]
            distance = lidar_readings[i + 1]
            print("Angle: {angle}, Distance: {distance}")

def reconstruct_map(lidar_data):
   map_data = [[0] * 361 for _ in range(100)]
    for reading in lidar_data:
        angle = reading.r
        distance = reading.i
        angle_rad = math.radians(angle)
        x = int(distance * math.cos(angle_rad))
        y = int(distance * math.sin(angle_rad))
        map_data[y][x] = 1

    return map_data

def lidar_client():
    rospy.init_node('lidar_client')
    lidar_scan()

if __name__ == "__main__":
    lidar_client()

