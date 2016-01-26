'''
Created on 14 gen. 2016

@author: albert
'''
import requests

#import webview
import PyQt5
import webview
import webbrowser
webbrowser.open('http://www.google.com')
class TViso(object):
    '''
    classdocs
    '''


    def __init__(self, id_api="3452", secret="t33eHYzzay9np3nugyzv"):
        '''
        Constructor
        '''
        
        #aconseguim el token d'autoritzacio 
        self.id_api = id_api
        self.secret = secret
        getauthurl= 'https://api.tviso.com/auth_token?id_api=' + id_api + '&secret=' + secret
        print(getauthurl)
        getAuthToken = requests.get('https://api.tviso.com/auth_token?id_api=' + id_api + '&secret=' + secret)
        print('auth_token: ',getAuthToken.json()['auth_token'],'\texpires: ',getAuthToken.json()['auth_expires_date'])
        self.auth_token = getAuthToken.json()['auth_token']
        self.auth_expires_date = getAuthToken.json()['auth_expires_date']

        #aconseguim el user token
#        webbrowser.open('https://api.tviso.com/user/user_token?auth_token='+self.auth_token+'&redirect_url=me')
        webbrowser.open('https://api.tviso.com/user/user_login?auth_token='+self.auth_token+'&username=ihipi&password=1234567')
        user = requests.post()


        #getLogin =  webview.create_window("It works, Jim!", 'https://api.tviso.com/user/user_token?auth_token='+self.auth_token)
        
Tv = TViso()        