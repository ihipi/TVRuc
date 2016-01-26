'''
Created on 10 gen. 2016
game of thrones

@author: albert
'''


import requests
from bs4 import BeautifulSoup
from KickassAPI import Torrent
from tools import tools

class Eliterorrent():
    def __init__(self):
        
        self.url = "http://www.elitetorrent.net"
        
        self.CATEGORIA = {'series':''+self.url+'/categoria/4/series',
                     'pelicules':''+self.url+'/categoria/2/peliculas',
                     'seriesVOSE':''+self.url+'/categoria/16/series-vose',
                     'peliculesVOSE':''+self.url+'/categoria/14/peliculas-vose',
                     'peliculesHDRIP':''+self.url+ '/categoria/13/peliculas-hdrip',}

    def busca(self, busqueda = ''):
        torrents={}
        url =''+self.url+'/busqueda/'+ busqueda
        resp = requests.get(''+self.url+'/busqueda/'+ busqueda)
        
        text = resp.text
        
        soup = tools.getBS(url)
        lis = soup.find_all('li')
        for li in lis:
            torrents[li.div.a.get('title')]= self.url+li.a.get('href')
        print(torrents)
        return torrents
        print('ended')
    
    def getTorrent(self, url):
        soup = tools.getBS(url)
        links = soup.find('div', attrs={'class':'enlace_descarga'})
        descarga =[]
        print(links)
        for a in links.find_all('a'):
            print(a)
            if a.get('href')[:6] != 'magnet':
                descarga.append(self.url+a.get('href'))
            else:
                descarga.append(a.get('href'))
        print(descarga)        
        return descarga
        

# print(soup.prettify())
#elite = Eliterorrent()
#elite.getTorrent(elite.busca('sense8')['Sense8 - 1x09'])