import math
import time
from moviepy.editor import VideoFileClip

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

%matplotlib inline


def read_img(str_path):
    image = cv.imread(str_path)
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return image


def show_img(ima):
    cv.imshow('image', ima)
    cv.waitKey()
    return 0


def blured_img(gry_img):
    blr_img = cv.GaussianBlur(gry_img, (5, 5), 0)
    return blr_img


def edge_detection(blr_img):
    edges = cv.Canny(blr_img, 100, 200)
    return edges


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255  # This line altered for grayscale.

    cv.fillPoly(mask, vertices, 255)
    masked_image = cv.bitwise_and(img, mask)
    return masked_image


def draw_line(img, lineP, color=(0, 255, 75), thickness=5):
    line_img = np.zeros(
        (
            img.shape[0],
            img.shape[1],
            3
        ),
        dtype="uint8"
    )

    img = np.copy(img)
    if lineP is not None:
        for l in lineP:

            cv.line(line_img, (int(l[0]), int(l[1])),
                    (int(l[2]), int(l[3])), color, thickness)

        img = cv.addWeighted(img, 0.6, line_img, 1.0, 0.0)
        return img


def region_of_interest_vertices(source_image):
    height, width = source_image.shape


    vertices = [
        (width / 1.7, height / 1.5),
        (width / 2, height / 1.5),
        (width / 6, height / 1.2),
        (0, height),
        (width, height),
        (width / 1.1, height / 1.2),
    ]

    return vertices

def draw_straight_line(source_image, edge):
    linesP = cv.HoughLinesP(
        edge,
        rho=6,
        theta=np.pi / 180,
        threshold=70,
        lines=np.array([]),
        minLineLength=20,
        maxLineGap=10
    )
    left_lanes_lines = []
    right_lanes_lines = []

    ##The average is easier to compute in slope intercept form.
    ## The average of slopes and average of intercepts of all lines is
    ## a good representation of the line.
    for line in linesP:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)
            # intercept = y1 - slope*x1

            if slope < -0.4 and slope > -0.9:
                left_lanes_lines.append((x1, y1, x2, y2))
            if (slope > 0.4 and slope < .9):
                right_lanes_lines.append((x1, y1, x2, y2))

    left_lane_detection = [sum(y) / len(y) for y in zip(*left_lanes_lines)]
    right_lane_detection = [sum(y) / len(y) for y in zip(*right_lanes_lines)]

    line_img = np.zeros(
        (
            source_image.shape[0],
            source_image.shape[1],
            3
        ),
        dtype="uint8"
    )

    if left_lane_detection is not None and len(left_lane_detection) > 0:
        slope = (left_lane_detection[3] - left_lane_detection[1]) / (left_lane_detection[2] - left_lane_detection[0])
        intercept = left_lane_detection[1] - slope * left_lane_detection[0]

        y1 = source_image.shape[0]  # bottom of the image
        y2 = int(y1 * 0.58)  # top of line, similar to mask height
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)

        img = np.copy(source_image)
        if linesP is not None:
            for l in linesP:
                cv.line(line_img, (x1, y1), (x2, y2), (0,0,255), 5)

            source_image = cv.addWeighted(source_image, 0.6, line_img, 1.0, 0.0)



    if right_lane_detection is not None and len(right_lane_detection) > 0:
        slope = (right_lane_detection[3] - right_lane_detection[1]) / (
                    right_lane_detection[2] - right_lane_detection[0])
        intercept = right_lane_detection[1] - slope * right_lane_detection[0]

        y1 = source_image.shape[0]  # bottom of the image
        y2 = int(y1 * 0.58)
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        if linesP is not None:
            for l in linesP:
                cv.line(line_img, (x1, y1), (x2, y2), (0, 0, 255), 5)

            source_image = cv.addWeighted(source_image, 0.6, line_img, 1.0, 0.0)

    return source_image




def processing(frame):
    gry_frame = cv.cvtColor(np.float32(frame), cv.COLOR_RGB2GRAY)
    gry = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blr_img = blured_img(gry)
    edges = edge_detection(blr_img)
    vertices = region_of_interest_vertices(gry_frame)
    mask = region_of_interest(edges, np.array([vertices], np.int32))
    drw = draw_straight_line(frame, mask)
    return drw




from moviepy.editor import VideoFileClip
from IPython.display import HTML
white_output = 'data/out.mp4'
clip1 = VideoFileClip("data/solidYellowLeft.mp4")
white_clip = clip1.fl_image(processing)
white_clip.write_videofile(white_output, audio=False)


