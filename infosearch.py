'''
Created on 5 gen. 2016

@author: albert
'''
from imdbpie import Imdb
import requests
from math import floor

class Info():
    '''
    Buscador d'informacio a imdb i a tvmaze
    '''
    def __init__(self):
        
    
        self.imdb = Imdb()
        self.imdb = Imdb(anonymize=True) # to proxy requests
        # Creating an instance with caching enabled
        # Note that the cached responses expire every 2 hours or so.
        # The API response itself dictates the expiry time)
        self.imdb = Imdb(cache=True)
        self.tvmazeUrl = 'http://api.tvmaze.com'
        
       
    def tvmazeRequest(self,ordre):
        '''
        funcio basica de demanda a tvmaze
        @return: Diccionari amb la resposta de tvmaze
        
        '''
        r = requests.get('' + self.tvmazeUrl + ordre)
        return r.json()

        
    def tvBusca(self,paraula):
        '''
        Busca i retorna un resultat de la busqueda
        '''
        
        r = self.tvmazeRequest('/search/shows?q=' + paraula)
        for i in r:
            print(i['show'], '\t',i['show']['id'])
        return r
    
    
    def tvBuscaUn(self,paraula, episodis=False):
        '''
        Es un "Voy a tener suerte" i retorna el millor resultat, si "episodis"esta activar retorna els episodis
        '''
        r= None
        if episodis:
            r = self.tvmazeRequest('/singlesearch/shows?q='+ paraula + '&embed=episodes')
            
        else:    
            r = self.tvmazeRequest('/singlesearch/shows?q='+ paraula)
        return r
        
    def tvBuscaId(self,id,tvrage=False, thetvdb=True):
        r = None
        if tvrage:
            r = self.tvmazeRequest('/lookup/shows?tvrage='+id)
        elif thetvdb:
            r= self.tvmazeRequest('/lookup/shows?thetvdb='+id)
        return r
    def tvShowInfo(self, tvmazeId, episode=False, specials = False):
        
        r=None
        if episode and specials:
            r= self.tvmazeRequest('/shows/' + str(tvmazeId) + '/episodes?specials=1')
        elif episode and not specials:
            r= self.tvmazeRequest('/shows/' + str(tvmazeId) + '/episodes')
        else:
            r= self.tvmazeRequest('/shows/' + str(tvmazeId) )
            
        return r
    def tvShowList(self, page=1):
        
        
        r = self.tvmazeRequest('/shows?page='+str(page))
        return r
            
        
# Buscador = Info()
# r = Buscador.tvBusca('thrones')

# 
# for l in r:
#     print('-'*60)
#     for k in l:
# 
#         print(k, ':\t', l[k])
# for i in r:
#     for k in i.keys():
#         if isinstance(i[k], dict):
#             for subk in i[k].keys() :
#                 print('subkey')
#                 print(subk,':\t',i[k][subk])
#         else:
#             print(k, ':\t',i[k])

#        print(k,':\t',i[k]['externals']['thetvdb'], '  -  ',i[k]['name'])

            
       
       
       
       
       
        
#     shows = imdb.search_for_title(input('Que estas buscant?'))
# 
# print(shows)
# 
# for s in shows:
#     print(s['imdb_id'],'\t',s['year'],'\t',s['title'])



# for show in shows:
#     print('--------------------',show['title'],'----------------------')
#     print('imatge', show['image']['url'],'\n')
