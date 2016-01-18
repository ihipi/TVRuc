'''
Created on 14 gen. 2016

@author: albert
'''
import requests

#import webview
import PyQt5
import webview

class TViso(object):
    '''
    classdocs
    '''


    def __init__(self, id_api="3452", secret="335PHWtYS2YDThRe5eV5"):
        '''
        Constructor
        '''
        
        #aconseguim el token d'autoritzacio 
        self.id_api = id_api
        self.secret = secret
        getAuthToken = requests.get('https://api.tviso.com/auth_token?id_api=' + id_api + '&secret=' + secret)

        self.auth_token = getAuthToken.json()['auth_token']
        self.auth_expires_date = getAuthToken.json()['auth_expires_date']
       
        #aconseguim el user token
        getLogin =  webview.create_window("It works, Jim!", 'https://api.tviso.com/user/user_token?auth_token='+self.auth_token)
        
Tv = TViso()        