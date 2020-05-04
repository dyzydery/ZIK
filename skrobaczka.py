# coding=utf-8
#! python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
def getPage(url):
	return str(urlopen(url).read())

def printPage(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	text_file = open("s.html", "w")
	text_file.write(soup.prettify())
	text_file.close()

def getPageClass(url,klasa):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup.find(class_=klasa)

def getPageClassAll(url,klasa):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup.find_all(class_=klasa)

def getPageId(url,idx):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup.find(id=idx)
