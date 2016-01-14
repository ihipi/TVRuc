'''
Created on 10 gen. 2016
game of thrones

@author: albert
'''


import requests
from bs4 import BeautifulSoup
class Eliterorrent():
    def __init__(self):
        
        self.url = "http://www.elitetorrent.net"
        
        self.CATEGORIA = {'series':''+self.url+'/categoria/4/series',
                     'pelicules':''+self.url+'/categoria/2/peliculas',
                     'seriesVOSE':''+self.url+'/categoria/16/series-vose',
                     'peliculesVOSE':''+self.url+'/categoria/14/peliculas-vose',
                     'peliculesHDRIP':''+self.url+ '/categoria/13/peliculas-hdrip'}

    def busca(self):
        resp = requests.get(''+url+'/busqueda/'+input('Què estas buscant?'))
        
        text = resp.text
        
        soup = BeautifulSoup(text, 'html.parser')
        lis = soup.find_all('li')
        for li in lis:
            print(li.div.a.get('title'))
            print('\t',''+url+li.a.get('href'))
        print('ended')

# print(soup.prettify())