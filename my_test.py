import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('c:\\bianban\\2.jpg',0)
img2 = img.copy()
img3 = cv2.imread('c:\\bianban\\2.jpg', 3)
sp = img.shape

template = cv2.imread('c:\\bianban\\temp_2.jpg',0)
w, h = template.shape[::-1]

template2 = cv2.imread('c:\\bianban\\temp.jpg',0)
w2, h2 = template2.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']



# for meth in methods:
#     img = img2.copy()
#     method = eval(meth)
#
#     # Apply template Matching
#     res = cv2.matchTemplate(img,template,method)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#
#     # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
#     if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
#         top_left = min_loc
#     else:
#         top_left = max_loc
#     bottom_right = (top_left[0] + w, top_left[1] + h)
#
#     cv2.rectangle(img,top_left, bottom_right, (255,0,0), 2)
#
#     plt.subplot(121),plt.imshow(res,cmap = 'gray')
#     plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
#     plt.subplot(122),plt.imshow(img3)
#     plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
#     plt.suptitle(meth)
#
#     plt.show()



img = img2.copy()
method = eval('cv2.TM_SQDIFF')

# 固定圆  Apply template Matching
res = cv2.matchTemplate(img,template,method)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
top_left = min_loc
bottom_right = (top_left[0] + w, top_left[1] + h)
cv2.rectangle(img3, top_left, bottom_right, 255, -1)

cv2.imwrite("e:\\cat2.jpg", img3)

# 移动圆  Apply template Matching
# print(top_left, sp[0])
img4 = cv2.imread('e:\\cat2.jpg',0)

res1 = cv2.matchTemplate(img4, template2, method)
min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res1)
top_left1 = min_loc1
bottom_right1 = (top_left1[0] + w2, top_left1[1] + h2)
cv2.rectangle(img4, top_left1, bottom_right1, 255, 1)



# plt.subplot(131),plt.imshow(res)
# plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(img3)
# plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
plt.subplot(121),plt.imshow(img4)


plt.show()