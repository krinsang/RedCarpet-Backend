from flask import Flask, request, jsonify
import urllib
import base64
import json
import requests
from pprint import pprint
import os
import urllib
import re

app = Flask(__name__)
default_port = 8000

GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyDVnGCR7OrzoJfL5lkmi8MiYS67Zv_p9ZU'



def get_prices(websites):
    '''given a list of links(website), the function returns a dictionary of website : price on the website'''

    # loop through the website
    for link in websites:
        # get rawhtml content
        rawHTML = str(urllib.urlopen(link).read())

        # REGEX look for price(CHECKME)
        prices = re.findall(r"\$[^\]]+", rawHTML)
        # pprint(prices)


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
	    },{ 
		'type': 'LOGO_DETECTION',
		'maxResults': 10}]
        }]
    })

    res = requests.post(api_url, data=req_body)
    return res.json()


@app.route('/', methods=['GET'])
def hello():
    api_dict = {
		'classify route Get, Post' : '/api/classify/'
		}
    return jsonify(api_dict) , 200

@app.route('/api/classify/', methods=['GET', 'POST'])
def classify():

    # if request use already encoded image, else use sample bag image(vie.jpg)
    if request.form:
        image_content = goog_cloud_vison(request.form['data'])
    else:
        f = open("vie.jpg",'r+')
        img_jpg = f.read()
        image_content = base64.b64encode(img_jpg)

    res_json = goog_cloud_vison(image_content)
    res_json['description'] = 'Label Detection (Google Cloud Vision)'
    descriptions = [None] * 10
    index = 0
    for i in res_json['responses'][0]['labelAnnotations']:
        descriptions[index] = i['description']
        index += 1
    descriptions = {'descriptions': descriptions}
    return searchParses(descriptions)


def searchParses(descriptions):
    query = ""
    print("in searchParses")
    for i in range(3):
            query += (descriptions['descriptions'][i] + ' ')
    subscription_key = "e9dbf70ca16c4533932bd31b5bb204bb"
    assert subscription_key
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params = {"q": query, "textDecorations":True, "textFormat":"HTML"}
    response = requests.get(search_url, headers = headers, params = params)
    response.raise_for_status()
    search_results = response.json()
    webSites = [None] * 5
    for i in range(5):
		webSites[i] = (search_results['webPages']['value'][i]['url'])
    # get the prices
    get_prices(webSites)

    webSites = {'webSites' : webSites}
    pprint(webSites)
    return jsonify(webSites)

if __name__ == '__main__':                                 
	app.run(host='0.0.0.0', port=default_port)

