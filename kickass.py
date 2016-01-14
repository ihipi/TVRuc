'''
Created on 9 gen. 2016

@author: albert
'''
from KickassAPI import Search, Latest, User, CATEGORY, ORDER

#Print the basic info about first 25 results of "Game of thrones" search
serch = Search("sense8").pages(1, 10)
print(serch)
for t in serch:
    if 'SPANiSH' or 'ESPAñOL' in t[0]:
        print(t[0],"\n\t",t[-3])
        
print("ended")