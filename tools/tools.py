'''
Created on 24 gen. 2016

@author: albert
'''
import json
import os
import requests
from bs4 import BeautifulSoup

confFile =os.path.abspath('./db/conf')


def getBS(url):
    res = requests.get(url)
    return BeautifulSoup(res.text,'html.parser')


def getconfig():
    f = open(confFile, mode='r')
    conf = json.load(f)
    return conf   


def setconfig(**kargs):
    conf = getconfig()
    print(kargs)
    for k in kargs.keys():
        if k in conf.keys():
        
            conf[k] = kargs[k]
        else:
            conf[k] ={ kargs[k]}
            print("La clau '{}' s'ha afegit a la configuració amb valor '{}'".format(k,kargs[k]))
            
        
    f = open(confFile, mode='w')
    json.dump(conf, f )
    f.close()
    print(conf)
    return True

#setconfig(actualitzacio_freq=1)