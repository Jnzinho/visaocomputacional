import cv2 as cv
import numpy as np


def process_cookie_images(image_paths: list[str]) -> None:
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    previous_equalized = None
    base_size = None  # (width, height)

    for index, image_path in enumerate(image_paths):
        original_gray = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
        if original_gray is None:
            print(f"Failed to load image: {image_path}")
            continue

        equalized = cv.equalizeHist(original_gray)

        if base_size is None:
            base_size = (equalized.shape[1], equalized.shape[0])
        else:
            if (equalized.shape[1], equalized.shape[0]) != base_size:
                equalized = cv.resize(equalized, base_size)
        print (index) # debug
        if previous_equalized is None:
            opened = cv.morphologyEx(equalized, cv.MORPH_OPEN, kernel)
            opened = cv.threshold(opened, 127, 255, cv.THRESH_BINARY)[1]
            opened = cv.dilate(opened, kernel, iterations=3)

            contours, _ = cv.findContours(opened, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

            contour_mask = np.zeros_like(opened)
            cv.drawContours(contour_mask, contours, -1, 255, 10)

            cv.imshow(f'Opening (first): {image_path}', opened)
            cv.imshow(f'Contours (first): {image_path}', contour_mask)
            print(f'Contours detected in {image_path}: {len(contours)}')
        else:
            change = cv.absdiff(equalized, previous_equalized)
            opened = cv.morphologyEx(change, cv.MORPH_OPEN, kernel)
            opened = cv.threshold(opened, 127, 255, cv.THRESH_BINARY)[1]
            opened = cv.dilate(opened, kernel, iterations=3)

            contours, _ = cv.findContours(opened, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

            contour_mask = np.zeros_like(opened)
            cv.drawContours(contour_mask, contours, -1, 255, 10)

            cv.imshow(f'Opening: {image_path}', opened)
            cv.imshow(f'Contours: {image_path}', contour_mask)
            print(f'Contours detected in {image_path}: {len(contours)}')

        previous_equalized = equalized


imgs = [
    'cookies/cookie3.png',
    'cookies/cookie.png',
    'cookies/cookie2.png',
]

process_cookie_images(imgs)

cv.waitKey(0)
cv.destroyAllWindows()