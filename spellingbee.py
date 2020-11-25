# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 11:25:24 2020

@author: Max
"""

import json, requests
from bs4 import BeautifulSoup
headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44",
        "X-Amzn-Trace-Id": "Root=1-5f592eba-58fbe130d46d9e0ebd201bdc"
    }

def getHTML(url):
    request = requests.get(url, headers=headers)
    return request.text

def loadList():
    words = open("words.txt","r").readlines()
    for i in range(len(words)):
        words[i] = words[i].rstrip()
    return words

def getValidWords(letters, middle):
    valid = []
    words =loadList()
    for w in words:
        if middle in w and all([letter in letters for letter in w]):
            valid.append(w)
    return valid

#this really ugly one-liner just loads the data from the NYtimes website
data = json.loads(BeautifulSoup(getHTML("https://www.nytimes.com/puzzles/spelling-bee"), features='lxml').find('script',{'type':'text/javascript'}).contents[0].split("window.gameData = ")[1])['today']

letters = data['validLetters']
middle = data['centerLetter']
officialwords = data['answers']

validwords = getValidWords(letters, middle)

unincluded = [word for word in validwords if not word in officialwords]

invalid = [word for word in officialwords if not word in validwords]
