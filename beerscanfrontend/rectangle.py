import cv2

def rectangle(image, request_results):
    color = (0, 255, 0)
    for elem in request_results["boxes"].values():
        cv2.rectangle(image, (elem['startX'], elem['startY']),
                      (elem['endX'], elem['endY']), color, 2)
    return image
