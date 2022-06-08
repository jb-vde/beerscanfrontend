import requests
import base64
import json
import cv2

URL_BASE = 'https://safe---beerscan-image-wkgvoiogvq-ew.a.run.app'
URL_BEER_ID = URL_BASE + '/identify_beers'


def rectangle(image, beers):
    color = (0, 255, 0)
    for beer in beers.values():
        cv2.rectangle(image, (beer['startX'], beer['startY']),
                      (beer['endX'], beer['endY']), color, 2)
        cv2.putText(image, beer["beer_name"][0],
                    (beer["startX"], beer["startY"]-10),
                    cv2.FONT_HERSHEY_PLAIN, 1.0, (0,255,0), 2)
    return image


def api_request(im_bytes):
    """Api requests for the rectangles coordinates"""

    img_b64 = base64.b64encode(im_bytes).decode("utf8")

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    payload = json.dumps({"image": img_b64})
    response = requests.post(URL_BEER_ID, data=payload, headers=headers)

    try:
        data = response.json()
        print(data)
    except requests.exceptions.RequestException:
        print(response.text)
        data =  {}

    return data
