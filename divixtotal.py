'''
Created on 10 gen. 2016

@author: albert
'''
import requests
from bs4 import BeautifulSoup


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
        
    def peticio(self, url):
        '''
        Fa la petició a una pàgina 
        @return: html en format text
        '''
        resp = requests.get(url)
    
        return resp.text
        
    def bs(self, text):
        '''
        crea un objecte Beautiful soup
        @param text: Un text que contingui html
        @return: l'objecte Beautifulsoup 
        '''
        
        soup = BeautifulSoup(text, 'html.parser')
        return soup
  
    
    def busca(self,busqueda, serie = False):
        '''
        Busca llistat de torrents
        @param busqueda: torrent que busques
        @param serie: si estas buscant una serie
          
        '''
        
        busca = self.peticio(self.cat['busca'] + busqueda)
#         print(busca)
        soup = self.bs(busca)
#         print(soup.prettify())
        #recull els resultats de la busqueda i els itera
        torrents = {}
        for p in soup.find_all('p', attrs={'class':'seccontnom'}):
            
            if serie: # si esta activat serie
                if 'Series' in p.next_sibling.next_sibling.a.get(('title')):
                    #comprova que estigui catalogat com a serie i retorna la pagina de la serie
                    seriebs = self.bs(self.peticio(''+self.url+p.a.get('href')))
                   
                    
                    for capitol in seriebs.find_all('td', attrs={"class":'capitulonombre'}):
                        torrents[str(capitol.a.text)] = '' + self.url+capitol.a.get('href')
                        #print(capitol.a.text, '\t'+ self.url+capitol.a.get('href'))
                break   
            else:
                torrents[str(p.a.text)] = ''+self.url+p.a.get('href')    
            #print(p.a.get('title'),'\t\t',''+self.url+p.a.get('href'))
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
            
# dvx = DivixTotal()
# #dvx.llistaSeries('B')
# dvx.busca(input('Quin torrent busques?'))    
# print('ended')