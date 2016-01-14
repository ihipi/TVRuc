'''
Created on 5 gen. 2016

@author: albert
'''
from imdbpie import Imdb

class Imdb():
    '''
    busquedes de informaci'o a imdb
    '''
    def __init__(self):
        
        self.imdb = Imdb()
        self.imdb = Imdb(anonymize=True) # to proxy requests
        
        # Creating an instance with caching enabled
        # Note that the cached responses expire every 2 hours or so.
        # The API response itself dictates the expiry time)
        
        self.imdb = Imdb(cache=True)
    def busca(self,busqueda):
        resultat={}
        busca = self.imdb.search_for_title(busqueda))
        
        for s in shows:
            resultat[s['imdb_id']]=[s['title'],s['year'],show['image']['url']]
            print(s['imdb_id'],'\t',s['year'],'\t',s['title'])
        
        return resultat


# for show in shows:
#     print('--------------------',show['title'],'----------------------')
#     print('imatge', show['image']['url'],'\n')
