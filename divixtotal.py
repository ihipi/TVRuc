'''
Created on 10 gen. 2016

@author: albert
'''
import requests
from bs4 import BeautifulSoup
from tools import tools


class DivixTotal(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.url = "http://www.divxtotal.com/"
        
        self.cat = {'busca' : '' + self.url + 'buscar.php?busqueda=',
                          'series':''+self.url+'series/',
                          'pelicules':''+self.url+'peliculas/'}
        

    
    def busca(self,busqueda, serie = False):
        '''
        Busca llistat de torrents
        @param busqueda: torrent que busques
        @param serie: si estas buscant una serie
          
        '''
        

        soup = tools.getBS(self.cat['busca'] + busqueda)
#         print(soup.prettify())
        #recull els resultats de la busqueda i els itera
        torrents = {}
        print('divixtotal:', serie)
        for p in soup.find_all('p', attrs={'class':'seccontnom'}):
            
            if serie: # si esta activat serie
                if 'Series' in p.next_sibling.next_sibling.a.get(('title')):
                    #comprova que estigui catalogat com a serie i retorna la pagina de la serie
                    seriebs = tools.getBS(self.url+p.a.get('href'))
                   
                    
                    for capitol in seriebs.find_all('td', attrs={"class":'capitulonombre'}):
                        torrents[str(capitol.a.text)] = self.url+capitol.a.get('href')
                        print(capitol.a.text, '\t'+ self.url+capitol.a.get('href'))
                return torrents   
            else:
                torrents[str(p.a.text)] = ''+self.url+p.a.get('href')    
            #print(p.a.get('title'),'\t\t',''+self.url+p.a.get('href'))
        print(torrents)
        return torrents
        

   
    def llistaSeries(self, inicial=None):
        '''
        Busca el llistat sencer de series de divixtotal
        
        '''
        soup = self.bs(self.peticio(self.cat['series']))
        lis = soup.find('li', {'class':'li_listadoseries'})
    
        for li in lis:
            lletra = None
            if li.font:   
                lletra= li.font.text           
                print(lletra)
            for a in li.find_all('a'):
                if inicial:
                    if lletra in inicial:
                        print(a.get('title'),'\t\t\t',''+self.url+a.get( 'href'))

                else:        
                    print(a.get('title'),'\t\t\t',''+self.url+a.get( 'href'))
            
#dvx = DivixTotal()
# #dvx.llistaSeries('B')
#dvx.busca('fargo')    
# print('ended')