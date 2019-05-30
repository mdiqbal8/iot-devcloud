
'''
* Copyright (c) 2018 Intel Corporation.
*
* Permission is hereby granted, free of charge, to any person obtaining
* a copy of this software and associated documentation files (the
* "Software"), to deal in the Software without restriction, including
* without limitation the rights to use, copy, modify, merge, publish,
* distribute, sublicense, and/or sell copies of the Software, and to
* permit persons to whom the Software is furnished to do so, subject to
* the following conditions:
*
* The above copyright notice and this permission notice shall be
* included in all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
* EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
* MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
* NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
* LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
* OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
* WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*
'''

import cv2
import argparse
import socket
import math
import os

from argparse import ArgumentParser

import numpy as np
from math import atan2

from math import atan2

OBJECT_AREA_MIN = 9000
OBJECT_AREA_MAX = 50000
LOWER_COLOR_RANGE = (0, 0, 0)
UPPER_COLOR_RANGE = (174, 73, 255)
COUNT_OBJECT = 0
HEIGHT_OF_OBJ = 0
WIDTH_OF_OBJ = 0
OBJECT_COUNT = "Object Number : {}".format(COUNT_OBJECT)

# Lower and upper value of color Range of the object for color thresholding to detect the object

def dimensions(box):
    """
    Return the length and width of the object.

    :param box: consists of top left, right and bottom left, right co-ordinates
    :return: Length and width of the object
    """
    (tl, tr, br, bl) = box
    x = int(math.sqrt(math.pow((bl[0] - tl[0]), 2) + math.pow((bl[1] - tl[1]), 2)))
    y = int(math.sqrt(math.pow((tl[0] - tr[0]), 2) + math.pow((tl[1] - tr[1]), 2)))

    if x > y:
        return x, y
    else:
        return y, x

'''
*********************************************** Orientation Defect detection ******************************************
 Step 1: Convert 3D matrix of contours to 2D 
 Step 2: Apply PCA algorithm to find angle of the data points.
 Step 3: If angle is greater than 0.5, return_flag is made to True else false. 
 Step 4: Save the image in "Orientation" folder if it has a orientation defect.
***********************************************************************************************************************
'''


def get_orientation(contours):
    """
    Gives the angle of the orientation of the object in radians
    :param contours: contour of the object from the frame
    :return: angle of orientation of the object in radians
    """
    size_points = len(contours)
    # data_pts stores contour values in 2D
    data_pts = np.empty((size_points, 2), dtype=np.float64)
    for i in range(data_pts.shape[0]):
        data_pts[i, 0] = contours[i, 0, 0]
        data_pts[i, 1] = contours[i, 0, 1]
    # Use PCA algorithm to find angle of the data points
    mean, eigenvector = cv2.PCACompute(data_pts, mean=None)
    angle = atan2(eigenvector[0, 1], eigenvector[0, 0])
    return angle


def detect_orientation(frame, contours, base_dir, count_object):
    """
    Identifies the Orientation of the object based on the detected angle
    :param frame: Input frame from video
    :param contours: contour of the object from the frame
    :return: defect_flag, object_defect
    """
    global OBJECT_COUNT
    defect = "Orientation"
    object_defect = "Defect : Orientation"
    # Find the orientation of each contour
    angle = get_orientation(contours)
    # If angle is less than 0.5 then we conclude that no orientation defect is present
    if angle < 0.5:
        defect_flag = False
    else:
        x, y, w, h = cv2.boundingRect(contours)
        print("Orientation defect detected in object {}".format(count_object))
        defect_flag = True
        cv2.imwrite("{}/orientation/Orientation_{}.jpg".format(base_dir, count_object), frame[y - 5: y + h + 10, x - 5: x + w + 10])
        cv2.putText(frame, OBJECT_COUNT, (5, 50), cv2.FONT_HERSHEY_SIMPLEX,0.75, (255, 255, 255), 2)
        cv2.putText(frame, "Defect: {}".format(defect), (5, 140),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
        cv2.putText(frame, "Length (mm): {}".format(HEIGHT_OF_OBJ), (5, 80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
        cv2.putText(frame, "Width (mm): {}".format(WIDTH_OF_OBJ), (5, 110),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
    return defect_flag, object_defect


'''
*********************************************** Color Defect detection ************************************************
 Step 1: Increase the brightness of the image
 Step 2: Convert the image to HSV Format. HSV color space gives more information about the colors of the image. 
         It helps to identify distinct colors in the image.
 Step 3: Threshold the image based on the color using "inRange" function. Range of the color, which is considered as 
         a defect for the object, is passed as one of the argument to inRange function to create a mask
 Step 4: Morphological opening and closing is done on the mask to remove noises and fill the gaps
 Step 5: Find the contours on the mask image. Contours are filtered based on the area to get the contours of defective
         area. Contour of the defective area is then drawn on the original image to visualize.
 Step 6: Save the image in "color" folder if it has a color defect.
***********************************************************************************************************************
'''


def detect_color(frame, cnt, base_dir, count_object):
    """
    Identifies the color defect W.R.T the set default color of the object
    :param frame: Input frame from the video
    :param cnt: Contours of the object
    :return: color_flag, object_defect
    """
    global OBJECT_COUNT
    defect = "Color"
    LOWER_COLOR_RANGE = (0, 0, 0)
    UPPER_COLOR_RANGE = (174, 73, 255)
    object_defect = "Defect : Color"
    color_flag = False
    # Increase the brightness of the image
    cv2.convertScaleAbs(frame, frame, 1, 20)
    # Convert the captured frame from BGR to HSV
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Threshold the image
    img_thresholded = cv2.inRange(img_hsv, LOWER_COLOR_RANGE, UPPER_COLOR_RANGE)
    # Morphological opening (remove small objects from the foreground)
    img_thresholded = cv2.erode(img_thresholded, kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    img_thresholded = cv2.dilate(img_thresholded, kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    contours, hierarchy = cv2.findContours(img_thresholded, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if 2000 < area < 10000:
            cv2.drawContours(frame, contours[i], -1, (0, 0, 255), 2)
            color_flag = True
    if color_flag == True:
        x,y,w,h =cv2.boundingRect(cnt)
        print("Color defect detected in object {}".format(count_object))
        print("{}/color/Color_{}.jpg".format(base_dir, count_object))
        cv2.imwrite("{}/color/Color_{}.jpg".format(base_dir, count_object), frame[y - 5: y + h + 10, x - 5: x + w + 10])
        cv2.putText(frame, OBJECT_COUNT, (5, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (255, 255, 255), 2)
        cv2.putText(frame, "Defect: {}".format(defect), (5, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
        cv2.putText(frame, "Length (mm): {}".format(HEIGHT_OF_OBJ), (5, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
        cv2.putText(frame, "Width (mm): {}".format(WIDTH_OF_OBJ), (5, 110),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
    return color_flag, object_defect


'''
**************************************************** Crack detection **************************************************
 Step 1: Convert the image to gray scale
 Step 2: Blur the gray image to remove the noises
 Step 3: Find the edges on the blurred image to get the contours of possible cracks
 Step 4: Filter the contours to get the contour of the crack
 Step 5: Draw the contour on the orignal image for visualization
 Step 6: Save the image in "crack" folder if it has crack defect
***********************************************************************************************************************
'''


def detect_crack(frame, cnt, base_dir, count_object):
    """
    Identifies the Crack defect on the object
    :param frame: Input frame from the video
    :param cnt: Contours of the object
    :return: defect_flag, object_defect, cnt
    """
    global OBJECT_COUNT
    defect = "Crack"
    object_defect = "Defect : Crack"
    defect_flag = False
    low_threshold = 130
    kernel_size = 3
    ratio = 3
    # Convert the captured frame from BGR to GRAY
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.blur(img, (7, 7))
    # Find the edges
    detected_edges = cv2.Canny(img, low_threshold, low_threshold * ratio, kernel_size)
    # Find the contours
    contours, hierarchy = cv2.findContours(detected_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = []
    if len(contours) != 0:
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            if area > 20 or area < 9:

                cv2.drawContours(frame, contours, i, (0, 255, 0), 2)
                defect_flag = True
                cnts.append(contours[i])

        if defect_flag == True:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.imwrite("{}/crack/Crack_{}.jpg".format(base_dir, count_object), frame[y - 5: y + h + 20, x - 5: x + w + 10])
            cv2.putText(frame, OBJECT_COUNT, (5, 50), cv2.FONT_HERSHEY_SIMPLEX,0.75, (255, 255, 255), 2)
            cv2.putText(frame, "Defect: {}".format(defect), (5, 140),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
            cv2.putText(frame, "Length (mm): {}".format(HEIGHT_OF_OBJ),(5, 80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
            cv2.putText(frame, "Width (mm): {}".format(WIDTH_OF_OBJ), (5, 110),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
            print("Crack defect detected in object {}".format(count_object))
    return defect_flag, object_defect, cnt


def runFlawDetector(vid_path= 0,distance= 0, fieldofview= 0, base_dir=None,  draw_callback=None):

    global HEIGHT_OF_OBJ
    global WIDTH_OF_OBJ
    global OBJECT_COUNT
    LOW_H = 0
    LOW_S = 0
    LOW_V = 47
    HIGH_H = 179
    HIGH_S = 255
    HIGH_V = 255
    count_object = 0
    if base_dir == None:
       base_dir = os.getcwd()
    dir_names = ["crack", "color", "orientation", "no_defect"]
    frame_count = 0
    num_of_dir = 4
    frame_number = 40
    defect = []
    if vid_path:
        if vid_path == 'CAM':
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("\nCamera not plugged in... Exiting...\n")
                sys.exit(0)
            fps = cap.get(cv2.CAP_PROP_FPS)
            delay = (int)(1000 / fps)
        else:
            cap = cv2.VideoCapture(vid_path)
            if not cap.isOpened():
                print("\nUnable to open video file... Exiting...\n")
                sys.exit(0)
            fps = cap.get(cv2.CAP_PROP_FPS)
            delay = (int)(1000 / fps)
    if distance and fieldofview:
        width_of_video = cap.get(3)
        height_of_video = cap.get(4)
        # Convert degrees to radians
        radians = (fieldofview / 2) * 0.0174533
        # Calculate the diagonal length of image in millimeters using
        # field of view of camera and distance between object and camera.
        diagonal_length_of_image_plane = abs(
            2 * (distance / 10) * math.tan(radians))
        # Calculate diagonal length of image in pixel
        diagonal_length_in_pixel = math.sqrt(
            math.pow(width_of_video, 2) + math.pow(height_of_video, 2))
        # Convert one pixel value in millimeters
        one_pixel_length = (diagonal_length_of_image_plane /
                            diagonal_length_in_pixel)
    # If distance between camera and object and field of view of camera
    # are not provided, then 96 pixels per inch is considered.
    # pixel_lengh = 2.54 cm (1 inch) / 96 pixels
    else:
            one_pixel_length = 0.0264583333
    # create folders with the given dir_names to save defective objects
    for i in range(len(dir_names)):
        if not os.path.exists(os.path.join(base_dir, dir_names[i])):
            os.makedirs(os.path.join(base_dir, dir_names[i]))
        else:
            file_list = os.listdir(os.path.join(base_dir, dir_names[i]))
            for f in file_list:
                os.remove(os.path.join(base_dir,dir_names[i],f))

    try:
        vw = None
        while True:
            # Read the frame from the stream
            _, frame = cap.read()

            if np.shape(frame) == ():
                break

            frame_count += 1
            OBJECT_COUNT = "Object Number : {}".format(count_object)

            # Check every given frame number (Number chosen based on the frequency of object on conveyor belt)
            if frame_count % frame_number == 0:
                defect = []
                HEIGHT_OF_OBJ = 0
                WIDTH_OF_OBJ = 0

                # Convert BGR image to HSV color space
                img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                # Thresholding of an Image in a color range
                img_thresholded = cv2.inRange(img_hsv, (LOW_H, LOW_S, LOW_V), (HIGH_H, HIGH_S, HIGH_V))

                # Morphological opening(remove small objects from the foreground)
                img_thresholded = cv2.erode(img_thresholded, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
                img_thresholded = cv2.dilate(img_thresholded, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

                # Morphological closing(fill small holes in the foreground)
                img_thresholded = cv2.dilate(img_thresholded, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
                img_thresholded = cv2.erode(img_thresholded, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

                # Find the contours on the image
                contours, hierarchy = cv2.findContours(img_thresholded, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

                for cnt in contours:
                    x, y, width, height = cv2.boundingRect(cnt)
                    if OBJECT_AREA_MAX > width * height > OBJECT_AREA_MIN:
                        box = cv2.minAreaRect(cnt)
                        box = cv2.boxPoints(box)
                        height, width = dimensions(np.array(box, dtype='int'))
                        HEIGHT_OF_OBJ = round(height * one_pixel_length * 10, 2)
                        WIDTH_OF_OBJ = round(width * one_pixel_length * 10, 2)
                        count_object += 1
                        frame_copy = frame.copy()
                        frame_orient = frame.copy()
                        frame_clr = frame.copy()
                        frame_crack = frame.copy()
                        frame_nodefect = frame.copy()
                        OBJECT_COUNT = "Object Number : {}".format(count_object)

                        # Check for the orientation of the object
                        orientation_flag, orientation_defect = detect_orientation(frame_orient, cnt, base_dir, count_object)
                        if orientation_flag == True:
                            defect.append(str(orientation_defect))

                        # Check for the color defect of the object
                        color_flag, color_defect = detect_color(frame_clr, cnt, base_dir, count_object)
                        if color_flag == True:
                            defect.append(str(color_defect))

                        # Check for the crack defect of the object
                        crack_flag, crack_defect, crack_contour = detect_crack(frame_crack, cnt, base_dir, count_object)
                        if crack_flag == True:
                            defect.append(str(crack_defect))

                        # Check if none of the defect is found
                        if not defect:
                            object_defect = "No Defect"
                            defect.append(str(object_defect))
                            print("No defect detected in object {}".format(count_object))
                            cv2.imwrite("{}/no_defect/Nodefect_{}.jpg".format(base_dir, count_object), frame[y - 5: y + height + 10, x - 5: x + width + 10])
                            cv2.putText(frame_nodefect, "Length (mm): {}".format(HEIGHT_OF_OBJ),(5, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255, 255, 255), 2)
                            cv2.putText(frame_nodefect, "Width (mm): {}".format(WIDTH_OF_OBJ),(5, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255, 255, 255), 2)
                        print("Length (mm) = {}, width (mm) = {}".format(HEIGHT_OF_OBJ, WIDTH_OF_OBJ))
                if not defect:
                    continue

            all_defects = " ".join(defect)
            cv2.putText(frame, all_defects, (5, 140), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 2)
            cv2.putText(frame, OBJECT_COUNT, (5, 50), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 2)
            cv2.putText(frame, "Length (mm): {}".format(HEIGHT_OF_OBJ), (5, 80),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
            cv2.putText(frame, "Width (mm): {}".format(WIDTH_OF_OBJ), (5, 110),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
            if draw_callback != None:
                draw_callback(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if vw == None:
                height = np.size(frame, 0)
                width = np.size(frame, 1)
                out_dir = os.path.join(base_dir, 'inference_output.mp4')
                vw = cv2.VideoWriter(out_dir, 0x00000021, 15.0, (width, height), True)
            vw.write(frame)
    finally:
        if vw != None:
            vw.release()


