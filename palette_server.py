from flask import Flask, request, jsonify
import urllib
import base64
import json
import requests
from pprint import pprint
import os
import urllib
import re
#importing the libraries
from urllib import urlopen
from bs4 import BeautifulSoup
import lxml
from urlparse import urlparse

app = Flask(__name__)
default_port = 8000

GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyDVnGCR7OrzoJfL5lkmi8MiYS67Zv_p9ZU'

'''
Link Ranking system process:
    Once we have database ready, check if link returned is from an advertisers website
    If so, rank higher. 

    If from Amazon, we add our referer link
    Rank these higher.

'''

def get_meta(websites):
    '''given list of websites, get meta data about those sites, used for link ranking'''
    final_dict = {}

    # loop through the website
    for link in websites:
        # get the domain
        parsed_uri = urlparse( link['url'] )
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        webpage = urlopen(domain).read()

        soup = BeautifulSoup(webpage, "lxml")
        metas = soup.find_all('meta')

        desc  = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
        final_dict[domain] = [desc]

    pprint(final_dict)
    return websites

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

    if request.form:
	 print('in response')
	 res_json = goog_cloud_vison(request.form['data'])
	 print(res_json)         
	 res_json['description'] = 'Label Detection (Google Cloud Vision)'
         descriptions = [None] * 10
         index = 0
         for i in res_json['responses'][0]['labelAnnotations']:
               descriptions[index] = i['description']
               index += 1
         descriptions = {'descriptions': descriptions}
         return searchParses(descriptions)
    else:
        print("in the if")
        f = open("vie.jpg",'r+')
        img_jpg = f.read()
        image_content = base64.b64encode(img_jpg)
        res_json = goog_cloud_vison(image_content)
        res_json['description'] = 'Label Detection (Google Cloud Vision)'
        descriptions = [None] * 10
        index = 0
        for i in res_json['responses'][0]['labelAnnotations']:
            descriptions [index] = i['description']
            index += 1
        descriptions = {'descriptions':descriptions}
        return searchParses(descriptions)


def searchParses(descriptions):
    query = ""
    for i in range(3):
            query += (descriptions['descriptions'][i] + ' ')
    subscription_key = "08adc37931234833b440dc054123937c"
    assert subscription_key
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params = {"q": query, "textDecorations":True, "textFormat":"HTML"}
    response = requests.get(search_url, headers = headers, params = params)
    response.raise_for_status()
    search_results = response.json()


    webSites = [None] * 10
    for i in range(10):
        webSites[i] = {'url' : search_results['images']['value'][i]['hostPageUrl'], 'image': search_results['images']['value'][i]['contentUrl']}
    
    webSites = get_meta(webSites)
    webSites = {'webSites' : webSites}
    pprint(webSites)
    return jsonify(webSites)

if __name__ == '__main__':                                 
	app.run(host='0.0.0.0', port=default_port)

