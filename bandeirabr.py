import numpy as np
import cv2 as cv

height, width = 200, 400
background_color = (0, 151, 57)
yellowBgr = (0, 255, 255)

img = np.full((height, width, 3), background_color, dtype=np.uint8)

pts = np.array([[200,0], [400,100], [200,200], [0,100]], np.int32)

image = cv.fillPoly(img, [pts], yellowBgr)

cv.circle(image, center=(200, 100), radius=50, color=(255, 0, 0), thickness=-1)

cv.imshow('bandeira',image)
cv.waitKey(0)
cv.destroyAllWindows()
