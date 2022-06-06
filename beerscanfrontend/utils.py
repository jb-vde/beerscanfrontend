import requests
import base64
import json
import cv2

URL_BASE = 'https://beerscan-image-wkgvoiogvq-ew.a.run.app'
URL_BOXES = URL_BASE + '/predict_boxes'
URL_BEER_ID = URL_BASE + '/identify_beer'


def rectangle(image, request_results):
    color = (0, 255, 0)
    for elem in request_results.values():
        cv2.rectangle(image, (elem['startX'], elem['startY']),
                      (elem['endX'], elem['endY']), color, 2)
    return image


def boxes_request(im_bytes):
    """Api requests for the rectangles coordinates"""

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


def beer_identification_request(im_bytes):
    """Api requests for the beer identification"""

    return ["Duvel Triple Hop"]

    # img_b64 = base64.b64encode(im_bytes).decode("utf8")

    # headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    # payload = json.dumps({"image": img_b64})
    # response = requests.post(URL_BEER_ID, data=payload, headers=headers)

    # try:
    #     data = response.json()
    #     print(data)
    # except requests.exceptions.RequestException:
    #     print(response.text)

    # return data['boxes']
