from flask import Flask, request, jsonify
import urllib
import base64
import json
import requests
from pprint import pprint
import os
import urllib
import re
import random 
#importing the libraries
from urllib import urlopen
from bs4 import BeautifulSoup
import lxml
import ebaysdk 
import datetime
from ebaysdk.exception import ConnectionError 
from ebaysdk.finding import Connection 
# from amazonproduct import API  
# from amazon.api import AmazonAPI 
# from pyaws import ecs 
# api = API(locale='us')
app = Flask(__name__)
default_port = 8000

GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyDVnGCR7OrzoJfL5lkmi8MiYS67Zv_p9ZU'


'''
Link Ranking system process:
    Once we have database ready, check if link returned is from an advertisers website
    If so, rank higher. 

    If from Amazon, we add our referer link
    Rank these higher.

    def rank_links(websites):
'''

cat_labels = []
with open("categories.csv", "r+") as f:
    lines = f.readlines()
    for line in lines: 
        cat_labels.append(line) 

def get_meta(websites):
    ''  'given list of websites, get meta data about those sites'''

    final_dict = {}

    # loop through the website
    for link in websites:
        webpage = urlopen(link).read()
        soup = BeautifulSoup(webpage, "lxml")
        title = soup.find("meta",  property="og:title")
        image = soup.find("meta", property="og:image")
        description = soup.findAll(attrs={"name":"description"})

        # print(description)
        title = title["content"] if title else "No meta title given"
        image = image["content"] if image else "No meta url given"

        desc = description
        final_dict[link] = [desc, title , image]

    pprint(final_dict)

def get_prices(websites):
    '''given a list of links(website), the function returns a dictionary of website : price on the website'''

    # loop through the website
    for link in websites:
        # get rawhtml content
        rawHTML = str(urllib.urlopen(link).read())

        # REGEX look for price(CHECKME)
        # prices = re.findall(r"\$[^\]]+", rawHTML)
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

@app.errorhandler(500)
def internal_error(error):
    return "page not found. please try again" 

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
        fuck = searchParses(descriptions)
	print(fuck)
	return fuck
def searchParses(descriptions):
    query = ""
    global cat_labels 
    query = random.choice(cat_labels) 
    ebay_query = ""
    for i in range(3):
            query += (descriptions['descriptions'][i] + ' ')
   	    ebay_query += (descriptions['descriptions'][i] + ' ') 
    subscription_key = "08adc37931234833b440dc054123937c"
    assert subscription_key
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params = {"q": query, "textDecorations":True, "textFormat":"HTML"}
    response = requests.get(search_url, headers = headers, params = params)
    response.raise_for_status()
    search_results = response.json()


    webSites = [None] * 5
    # for i in range(3):
    #     # pprint(search_results['webPages']['value'])
    #     webSites[i] = {'url' : search_results['images']['value'][i]['hostPageUrl'], 'image': search_results['images']['value'][i]['contentUrl']}
    # amazon = AmazonAPI('AKIAIG4LJX65WJ6FRXNQ', 'eGHnM8AgGG5YfX6Tjl8dt6OxXb3xTkVvb/gn1MCy', 'teamdiversity-20')
    # products = amazon.search_n(1, Keywords='kindle', SearchIndex='All')
    # len(products)
    # ecs.setLicenseKey('AKIAIG4LJX65WJ6FRXNQ')
    # books = ecs.ItemSearch('python', SearchIndex='Books')
    # print(books[0].Title)
    # for apparel in api.item_search('Apparel', Keywords='Shirt'):
    #     print '%s: ' % (apparel.ASIN)
            # amazon_key = 'kK4vFL6Iwq2MHBt99mps166OG5K4yn693QvTNh76' 
    # amazon_id = 'ijuxp5i7cd'
    # amazon_url = 'http://webservices.amazon.com/onca/xml?Service=AWSECommerceService&AWSAccessKeyId=AKIAIG4LJX65WJ6FRXNQ&AssociateTag=teamdiversity-20&Operation=ItemSearch&Keywords=Nike&SearchIndex=Apparel&Sort=price'
    # response = requests.get(amazon_url)
    # response.raise_for_status()
    # search_results = response.json()
    # print(search_results)
    # api = finding(siteid='EBAY-US', appid='teamdive-redcarpe-PRD-e786e1828-f21c094c')

    # api.execute('findItemsAdvanced', {
    #     'keywords': 'laptop',
    #     'categoryId' : ['177', '111422'],
    #     'itemFilter': [
    #         {'name': 'Condition', 'value': 'Used'},
    #         {'name': 'MinPrice', 'value': '200', 'paramName': 'Currency', 'paramValue': 'GBP'},
    #         {'name': 'MaxPrice', 'value': '400', 'paramName': 'Currency', 'paramValue': 'GBP'}
    #     ],
    #     'paginationInput': {
    #         'entriesPerPage': '25',
    #         'pageNumber': '1'    
    #     },
    #     'sortOrder': 'CurrentPriceHighest'
    # })

    # dictstr = api.response_dict()

    # for item in dictstr['searchResult']['item']:
    #     print "ItemID: %s" % item['itemId'].value
    #     print "Title: %s" % item['title'].value
    #     print "CategoryID: %s" % item['primaryCategory']['categoryId'].value
    try:
        api = Connection(appid='teamdive-redcarpe-PRD-e786e1828-f21c094c', config_file=None)
        response = api.execute('findItemsAdvanced', {'keywords': ebay_query, 'sortOrder': 'CurrentPriceLowest'})
        items = response.reply.searchResult.item
	print(items)
	for i in range(2): 
            webSites[i] = {'url': items[i].viewItemURL, 'image': items[i].galleryURL, 'price': items[i].sellingStatus.currentPrice.value}
        for i in range(2,5):
            webSites[i] = {'url' : search_results['images']['value'][i]['hostPageUrl'], 'image': search_results['images']['value'][i]['contentUrl'], 'price': '0.00'}
    
    except Exception, e:
	for i in range(5):
	     webSites[i] = {'url' : search_results['images']['value'][i]['hostPageUrl'], 'image': search_results['images']['value'][i]['contentUrl'], 'price': '0.00'}
    webSites = {'webSites' : webSites}
    pprint(webSites)
    return jsonify(webSites)

if __name__ == '__main__':                                 
	app.run(host='0.0.0.0', port=default_port)


