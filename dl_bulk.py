"""
script for bulk download of modis land cover data

Written by Ulas Qazi
Date: June 9th 2021

"""
import os 
import re 
import configparser
from lxml import html 
import requests
from requests.auth import HTTPBasicAuth 
import urllib.request

#First we'll link to our text file containing data sources 
with open(r'C:\Users\cfcni\Desktop\oscar\data\links2020.txt') as tx_s:
    for line in tx_s:
        urls = re.findall('https?:.*?.hdf', line)
        #print(urls)

print(urls[0])
print(len(urls))

#############################################################################
# overriding requests.Session.rebuild_auth to mantain headers when redirected
 
class SessionWithHeaderRedirection(requests.Session): 
    AUTH_HOST = 'urs.earthdata.nasa.gov' 
    def __init__(self, username, password): 
        super().__init__() 
        self.auth = (username, password)
  
   # Overrides from the library to keep headers when redirected to or from 
   # the NASA auth host.
    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers 
        url = prepared_request.url 
        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url) 
            redirect_parsed = requests.utils.urlparse(url)
            if (original_parsed.hostname != redirect_parsed.hostname) and redirect_parsed.hostname != self.AUTH_HOST and original_parsed.hostname != self.AUTH_HOST: 
                    del headers['Authorization']
 
        return

# create session with the user credentials that will be used to authenticate access to the data
username = "###" 
password= "###" 
session = SessionWithHeaderRedirection(username, password)

print(*urls, sep = '\n')

for filename in urls:
    try:
        # submit the request using the session
        response = session.get(filename, stream=True)
        print(response.status_code)

        #define names for files 
        namefile = filename[filename.rfind('/')+1:]

        # raise an excpetion in case of http errors 
        response.raise_for_status()

        # save the file 
        #with open(filename, 'wb') as fd:
        with open(namefile, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=1024*1024):
                fd.write(chunk)

    except requests.exceptions.HTTPError as e:
        print(e)
    # except requests.exceptions.Timeout:
    #     print ("Timeout occurred")


