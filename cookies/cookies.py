import cv2 as cv
import numpy as np

def count_chocolate_drops(image_path: str, width: int = 1000, height: int = 1000) -> int:
    img = cv.imread(image_path)
    if img is None:
        print(f"Failed to load image: {image_path}")
        return 0

    img_resized = cv.resize(img, (width, height))

    cv.imshow(f'Cookie: {image_path}', img_resized)

    blackandwhiteimg = cv.cvtColor(img_resized, cv.COLOR_BGR2GRAY)
    blackandwhiteimg = cv.GaussianBlur(blackandwhiteimg, (5, 5), 0)
    blackandwhiteimg = cv.threshold(blackandwhiteimg, 50, 255, cv.THRESH_BINARY)[1]

    # BLOB
    params = cv.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 10
    params.filterByCircularity = True
    params.minCircularity = 0.3
    params.filterByConvexity = True
    params.minConvexity = 0.3
    blob = cv.SimpleBlobDetector_create(params)

    # DILATATION
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (10, 10))
    blackandwhiteimg = cv.dilate(blackandwhiteimg, kernel, iterations=1)

    # EROSAO
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (40, 40))
    blackandwhiteimg = cv.erode(blackandwhiteimg, kernel, iterations=1)

    contours, hierarchy = cv.findContours(blackandwhiteimg, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    # draw contours in blue
    img_with_contours = cv.drawContours(blackandwhiteimg, contours, -1, (60,0,255), 1)

    cv.imshow(f'Cookie: {image_path}', img_with_contours)

    print(f'Number of chocolate drops in {image_path}: {len(contours)}')
    
    return len(contours)

image_files = [
    'cookies/cookie3obgbreno.png',
    'cookies/cookie.png',
    'cookies/cookie2.png'
]

for image_file in image_files:
    count_chocolate_drops(image_file)

cv.waitKey(0)
cv.destroyAllWindows()