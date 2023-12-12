from itertools import product
from GUI import GUI
from HAL import HAL
import urllib.request
import numpy as np
import tempfile
import time
import cv2
import os



# Download the haars XML for face detection 
def download_and_load_cascade():
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    with urllib.request.urlopen(url) as resp, tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(resp.read())
        temp.close()
        cascade = cv2.CascadeClassifier(temp.name)
        os.unlink(temp.name)
    return cascade
    

# We are rotating the image, not the drone 
def get_image_rotated(img, rotation):
    height, width = img.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), rotation, 1)
    return cv2.warpAffine(img, rotation_matrix, (width, height))


# We are detecting faces rotating the dron images
def detect_faces(img, detector):
    face_detected = False
    rotated_angles= [180.0, -135.0, 135.0, -90.0, 90.0, -60.0, 60.0, -45.0, 45.0, -20.0, 20.0, 0]
    
    frame_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    frame_gray = cv2.equalizeHist(frame_gray)
    
    for i in rotated_angles:
        img_rotated = get_image_rotated(img, i)
        faces = detector.detectMultiScale(img_rotated)
        for (x,y,w,h) in faces:
            center = (x + w/2, y + h/2)
            face_detected = True
            break
        if face_detected:
            break
    return face_detected
    


# Returning to initial point base
def return_to_base(boat_position):
    HAL.set_cmd_pos(boat_position[0], boat_position[1], boat_position[2], 0.0)
    time.sleep(15)
    HAL.land()


# Show the images of the drone when a survivor was found
def show_survivors_found_faces():
    for face in survidors_faces_found:
      GUI.showLeftImage(face)
      time.sleep(5)


# Return the grid for searching the survivors in the survivors location
def generate_grid(start_point, step, f_num_step_x, f_num_step_y):
    x_step, y_step = step
    x_start, y_start = start_point
    x_values = [x_start + x_step * i for i in range(f_num_step_x)]
    y_values = [y_start + y_step * j for j in range(f_num_step_y)]
    grid = list(product(x_values, y_values))
    return grid


# Display ventral and frontal images
def display_cameras():
    GUI.showImage(HAL.get_frontal_image())
    GUI.showLeftImage(HAL.get_ventral_image())
  

survivors_found = set()
survidors_faces_found = []
survivors_zone = (43, -28)
searching_height = 1
moving_height = 5 
grid = generate_grid(survivors_zone, (-3, -3), 7, 6)
finish = False


print("Starting...")
face_detector = download_and_load_cascade()
boat_position = HAL.get_position()
init_yaw = HAL.get_yaw()

print("Taking off...")
HAL.takeoff(moving_height)


print("Going to survivors zone...")
HAL.set_cmd_pos(survivors_zone[0], survivors_zone[1], searching_height, init_yaw)
time.sleep(10)


while True:
    
    display_cameras()
    
    if len(survivors_found) >= 6 and not finish:
        print("Returning to boat...")
        return_to_base([boat_position[0], boat_position[1], moving_height])
        show_survivors_found_faces()
        finish = True

    elif len(survivors_found) >= 6:
        print("End")
    
    else:
        for point in grid:
            display_cameras()
            ventral_img = HAL.get_ventral_image()
            HAL.set_cmd_pos(point[0], point[1], searching_height, init_yaw)
            time.sleep(2.0)
            if detect_faces(ventral_img, face_detector):
                survivor_position = (point[0], point[1])
                if survivor_position not in survivors_found:
                    survivors_found.add(survivor_position)
                    survidors_faces_found.append(ventral_img)
                    print("New survivor found at:", survivor_position)
                else:
                    print("Survivor already found at:", survivor_position)


