# coding: utf-8
from flask import Flask, request, jsonify
import urllib
import base64
import json
import requests
import os

app = Flask(__name__)
default_port = 52892

GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyD6_ObTCpA5dB8Ep8CO_5Xj-ozgVdI0IU0'

def goog_cloud_vison (image_content):
    api_url = GOOGLE_CLOUD_VISION_API_URL
    req_body = json.dumps({
        'requests': [{
            'image': {
                'content': image_content
            },
            'features': [{
		'type': 'LABEL_DETECTION',
		'maxResults': 10,
	    }]
        }]
    })

    res = requests.post(api_url, data=req_body)
    return res.json()


@app.route('/', methods=['GET'])
def hello ():
    return 'Hello! This is palette_server.'


@app.route('/api/classify', methods=['POST'])
def classify ():
    #print(requests.files['file'])
    #print(jsonify(requests))	    
    #if ('jpg' in requests.files['file']):
	print("in the if")
        #image_base64_str = tfpp_json['jpg'].replace('data:image/jpeg;base64,', '')
        f = open("vie.jpg",'r+')
	img_jpg = f.read()
	print("what")
        image_content = base64.b64encode(img_jpg)
        res_json = goog_cloud_vison(image_content)
        res_json['description'] = 'Label Detection (Google Cloud Vision)'

        return jsonify(res_json)
	#return "jpg received"

app.run(host="159.65.33.47", port=default_port)
