'''
Created on 9 gen. 2016

@author: albert
'''
from KickassAPI import Search, Latest, User, CATEGORY, ORDER

#Print the basic info about first 25 results of "Game of thrones" search
search = Search("sense8").pages(1, 10)
print([s for s in search])
# for t in search:
#     if 'SPANiSH' or 'ESPAñOL' in t[0]:
#         print(t[0],"\n\t",t[-3])
        
print("ended")