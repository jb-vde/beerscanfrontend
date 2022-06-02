import requests
import base64
import json
import cv2

URL_BASE = 'https://beerscan-image-wkgvoiogvq-ew.a.run.app'
URL_BOXES = URL_BASE + '/predict_boxes'
URL_SIZE = URL_BASE + '/size'


def rectangle(image, request_results):
    color = (0, 255, 0)
    for elem in request_results["boxes"].values():
        cv2.rectangle(image, (elem['startX'], elem['startY']),
                      (elem['endX'], elem['endY']), color, 2)
    return image


def test_boxes_endpoint(img_b64):

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    payload = json.dumps({"image": img_b64})
    response = requests.post(URL_BOXES, data=payload, headers=headers)

    try:
        data = response.json()
        print(data)
    except requests.exceptions.RequestException:
        print(response.text)

    return data


def boxes(image_file):

    with open(image_file, "rb") as f:
        im_bytes = f.read()
    img_b64 = base64.b64encode(im_bytes).decode("utf8")


    data = test_boxes_endpoint(img_b64)
    return data
