# -*- coding:utf-8-*-


import cv2
import numpy as np
import matplotlib.pyplot as plt

def measure_distance(src_img):

    # img = cv2.imread(src_img, 0)
    # unicode(src_img)
    print(src_img)
    # t = src_img.encode("utf-8")
    # print(t)
    img = cv2.imdecode(np.fromfile(src_img, dtype=np.uint8), 0)

    print(1)
    # img = cv2.medianBlur(img,5)
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edge = cv2.Canny(img, 0, 0)

    circles = cv2.HoughCircles(edge,cv2.HOUGH_GRADIENT,1,100,
                                param1=60,param2=30, minRadius=55,maxRadius=65)

    # circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20,
    #                            param1=60, param2=30, minRadius=55, maxRadius=65)

    # circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
    #
    #                            param1=50,param2=30, minRadius=55,maxRadius=65)
    method = eval('cv2.TM_SQDIFF')
    template = cv2.imread('img/temp_2.jpg', 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img, template, method)

    try:

        circles = np.uint16(np.around(circles))

        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(255,0,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(255,0,0),3)

    except:

        pass



    # 固定圆  Apply template Matching

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(cimg, top_left, bottom_right, (0,0,255), 2)
    # cv2.rectangle(cimg, top_left, bottom_right, (255,0,0), 3)

    return cimg, circles, top_left[0], top_left[0] + w

# cimg,circles = measure_distance("C:\\bianban\\2.jpg")
# # cv2.imshow('detected circles',cimg)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
# # cimg = measure_distance("3.jpg")
# plt.imshow(cimg)
# plt.show()