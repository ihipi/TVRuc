'''
Created on 24 gen. 2016

@author: albert
'''
import requests, json, os
from bs4 import BeautifulSoup

confFile =os.path.abspath('../SickRuc/db/conf')


def getBS(url):
    res = requests.get(url)
    return BeautifulSoup(res.text,'html.parser') 
def getconfig():
    f = open(confFile, mode='r')
    conf = json.load(f)
    return conf   
    
def setconfig(**kargs):
    conf = getconfig()
    
    for k in kargs.keys():
        if k in conf.keys():
        
            conf[k] = kargs[k]
        else:
            print("no existaix '"+k+"' a la configuració")
            
        
    f = open(confFile, mode='w')
    json.dump(conf, f )
    f.close()
    print(conf)
    return True

#setconfig(actualitzacio_freq=1)