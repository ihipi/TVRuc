'''
Created on 14 gen. 2016

@author: albert
'''
import requests, time

#import webview
import PyQt5, requests
#Per llegir parameetres de una url
from urllib.parse import urlparse, parse_qs
from tools.constants import API_ID, SECRET, TVISOURL
from pprint import pprint
from tools import tools

class TViso(object):
    '''
    classdocs
    '''

    

    def __init__(self, id_api=None, secret=None):
        '''
        Constructor
        '''
        
        
        #aconseguim el token d'autoritzacio 
        self.id_api = id_api or API_ID
        self.secret = secret or SECRET
        self.actualTime = time.time()
        self.auth_token = tools.getconfig()['auth_token']
        self.auth_expires = tools.getconfig()['auth_expires_date']
        self.user_token = tools.getconfig()['user_token']

        print(self.actualTime , self.auth_expires)

        if self.actualTime > self.auth_expires :
            self.getAuthToken()
            self.getUserToken()
        

        #aconseguim el user token
#        webbrowser.open('https://api.tviso.com/user/user_token?auth_token='+self.auth_token+'&redirect_url=me')
#        webbrowser.open('https://api.tviso.com/user/user_login?auth_token='+self.auth_token+'&username=ihipi&password=1234567')
    def getAuthToken(self):
#        if self.actualTime > self.auth_expires_date:
        getauthurl= 'https://api.tviso.com/auth_token?id_api=' + self.id_api + '&secret=' + self.secret
        getAuthToken = requests.get(getauthurl)
        print('auth_token: ',getAuthToken.json()['auth_token'],'\expira: ',getAuthToken.json()['auth_expires_date'])
        tools.setconfig(auth_expires_date = getAuthToken.json()['auth_expires_date'], auth_token = getAuthToken.json()['auth_token'])
        return True
 #       else:
 #           print('No sha tocat auth_token({})'.format(self.auth_token))   
    def getUserToken(self):
        urluser = 'https://api.tviso.com/user/user_login?auth_token='+self.auth_token+'&username=albert.giro@gmail.com&password=1234567'
        response = requests.get(urluser)
        if response.history:
            print("Request was redirected")
            
            print(response.status_code, response.url)
            #creem un objecte url parse per trobar el usertoken
            resp = urlparse(response.url)
            query = parse_qs(resp.query)
            if query.get('user_token'):
                print(query.get('user_token')[0])
                tools.setconfig(user_token = query.get('user_token')[0])
                return True
            else:
                respj = response.json()
                print(respj)
                print("")
                return False

        #getLogin =  webview.create_window("It works, Jim!", 'https://api.tviso.com/user/user_token?auth_token='+self.auth_token)
    def searchTitle(self, title):
        print('comenca searchTitle', 'https://api.tviso.com/media/search?auth_token='+self.auth_token+"&q='"+title+"'")
        gets = {'auth_token': self.auth_token,
                'q':title,
                'country':'ES'}
        return requests.get('https://api.tviso.com/media/search?',params =gets)
    def getAllMediaList(self):
        gets = {'auth_token':self.auth_token}
        return requests.get(TVISOURL + '/media/list/all?',params = gets)
    def getFollowing(self):
        gets={'auth_token':self.auth_token,'user_token':self.user_token}
        print((TVISOURL+'/user/following?',gets))
        return requests.get(TVISOURL+'/user/following?', params = gets)
    def getUserCollection(self):
        gets={'auth_token':self.auth_token,'user_token':self.user_token}
        return requests.get(TVISOURL+'/user/media/collection?', params = gets)
    def getUserMedia(self,media = False):
        gets={'auth_token':self.auth_token,'user_token':self.user_token}

        return requests.get(TVISOURL + '/user/media?', params = gets)
    def getFullInfo(self, idm,mediaType = None):
        gets = {'auth_token': self.auth_token,'idm':idm }
        if mediaType:
            print('media: ',mediaType)
            gets['mediaType']=mediaType
        return requests.get(TVISOURL+'/media/full_info?', params = gets)
    def getUserPending(self):
        gets={'auth_token':self.auth_token,'user_token':self.user_token}
        return requests.get(TVISOURL+'/user/media/pending/:mediaType?', params = gets)
    def getUserSumary(self):
        gets={'auth_token':self.auth_token,'user_token':self.user_token}
        return requests.get(TVISOURL+'/user/media/collection_summary?', params = gets)    
        
# Tv = TViso()
#pprint(Tv.searchTitle('fargo').json())      
#pprint(Tv.getUserCollection().json(),depth = 5)
#pprint(Tv.getUserMedia().json(),depth = 5)
#pprint(Tv.getFullInfo(2078,1).json(),depth = 5)
# pprint(Tv.getUserSumary().json(),depth =4)