import requests
import base64
import json
import cv2

URL_BASE = 'https://beerscan-image-wkgvoiogvq-ew.a.run.app'
URL_BOXES = URL_BASE + '/predict_boxes'


def rectangle(image, request_results):
    color = (0, 255, 0)
    for elem in request_results.values():
        cv2.rectangle(image, (elem['startX'], elem['startY']),
                      (elem['endX'], elem['endY']), color, 2)
    return image


<<<<<<< HEAD
def boxes_request(im_bytes):

    """Request to api coordinates of the rectangles boxes surrounding beer bottles

    """
=======
def boxes_request(image_file):

    with open(image_file, "rb") as f:
        im_bytes = f.read()
>>>>>>> cc7b28bda21eb0dc61fde693804c85ebf3ee4f6e

    img_b64 = base64.b64encode(im_bytes).decode("utf8")

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    payload = json.dumps({"image": img_b64})
    response = requests.post(URL_BOXES, data=payload, headers=headers)

    try:
        data = response.json()
        print(data)
    except requests.exceptions.RequestException:
        print(response.text)

    return data['boxes']
