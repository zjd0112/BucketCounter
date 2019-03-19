import cv2
import numpy as np

lower_blue = np.array([165, 100, 100])
higher_blue = np.array([175, 255, 255])
maxPlateRatio = 1.45
minPlateRatio = 0.55
count = 0;

def findPlateNumberRegion(img):
    region = []
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # print("contours lenth is :%s" % (len(contours)))
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        print(area)

        if area < 18000 or area > 32000:
            continue

        rect = cv2.minAreaRect(cnt)
        # print("rect is:%s" % {rect})

        box = np.int32(cv2.boxPoints(rect))

        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])
        ratio = float(width) / float(height)
        print(ratio)
        if ratio > maxPlateRatio or ratio < minPlateRatio:
            continue
        region.append(box)
    return region

if __name__ == '__main__':
    img = cv2.imread("temp/image.jpg")
    height = img.shape[0]
    width = img.shape[1]
    img = img[int(height/3):height, 0:width]

    # conevrt RGB to HSV
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # find all eligible pixels
    in_range_array = cv2.inRange(hsv_img, lower_blue, higher_blue)

    cv2.imwrite("temp/temp1.jpg", in_range_array)

    # close operation
    element_close = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 50))
    closed = cv2.morphologyEx(in_range_array, cv2.MORPH_CLOSE, element_close)
    cv2.imwrite("temp/temp2.jpg", closed)

    # open operation
    element_open = cv2.getStructuringElement(cv2.MORPH_RECT, (60, 3))
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, element_open)
    cv2.imwrite("temp/temp3.jpg", opened);

    # close operation
    element_close2 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 100))
    closed2 = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, element_close2)
    cv2.imwrite("temp/temp4.jpg", closed2);


    region = findPlateNumberRegion(closed2)

    if len(region) != 0:
        for i in range(len(region)):
            box = region[i]
            cv2.drawContours(img, [box], 0, (0, 255, 0), 3)

    cv2.imwrite("temp/result.jpg", img)
    print(len(region))
