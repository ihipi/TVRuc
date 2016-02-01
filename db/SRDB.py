'''
Created on 16 gen. 2016

@author: albert
'''
import sqlite3,datetime, time, urllib,json,os, threading, queue
from buscadors.infosearch import Info
from math import floor
from datetime import datetime
from tools import tools
from buscadors.tviso import TViso
from tools.constants import TVISOURL, IMG
from pprint import pprint
 



class SickRucDB():
    '''
    classdocs
    '''


    def __init__(self, lloc=''):
        '''
        Constructor
        '''
        self.root = lloc
        self.dbname = 'sicruc.db'
        self.db = sqlite3.connect(lloc +self.dbname)
        self.c = self.db.cursor()
        
        self.c.execute('CREATE TABLE IF NOT EXISTS series (imdb INTEGER PRIMARY KEY not NULL,tvmazeID INTEGER, name TEXT, image TEXT, rating TEXT, sinopsis TEXT)')
        self.c.execute('CREATE TABLE IF NOT EXISTS mycollection (imdb INTEGER PRIMARY KEY not NULL,tviso_id INTEGER, media INTEGER, name TEXT, estat TEXT, imatge TEXT )')
        self.c.execute('create table if not exists capitols (idm INTEGER PRIMARY KEY not NULL, tviso_id INTEGER, season INTEGER, capitol INTEGER, titol TEXT, sinopsis TEXT,estat INTEGER , date TEXT)')
        self.lastId = self.getLastID()
        self.format = '%Y-%M-%d'
        ###
        ### COMPROVAR ULTIMA ACTUALITZACIó 
        ###
        self.lastUpdate = self.gettime()
        deltaTime = datetime.strptime(time.strftime(self.format),self.format)-datetime.strptime(self.lastUpdate , self.format)
        print(self.lastUpdate)
        if deltaTime.days>=tools.getconfig()['actualitzacio_freq']:
            print(deltaTime.days)            
            self.updateUserMedia()
        else:
            print('-'*50,'\nBase de dades actualitzada a dia: {}\n'.format(self.lastUpdate),'-'*50)
    def gettime(self):
        print(tools.getconfig()['lastUpdate'])
        return tools.getconfig()['lastUpdate']    
    
    def settime(self):
#         f = open(self.root+'conf', mode='w')
        last = {'lastUpdate':time.strftime(self.format)}
#         j = json.dump(last, f )
#         f.close()
        tools.setconfig(lastUpdate = time.strftime(self.format))
        return tools.getconfig()
    
    def dbstart(self):
        self.db = sqlite3.connect(self.dbname)
        self.c = self.db.cursor()
    def dbstop(self):
        self.db.close()

        
        
    def getLastID(self):
        
        self.c.execute('select * from series')
        lastId = 0
        for row in self.c:
            if row[0]>lastId:
                lastId = row[0]
        print('Last TVMaze id: ',lastId)
        return lastId
    def wgetImage(self, serie,tipus):    
        '''
        aconsegueix les imatges del "media seleccionat
        @params media_json: json de TVISO amb la informacio del media 
        '''
        tviso =  TViso()
        print(serie, tipus)
        res = tviso.getFullInfo( serie, tipus).json()

        if isinstance(res['images'], dict):
            posterFile = self.root+'imatges/'+res['imdb']+"_poster.jpg"
            backdropFile = self.root+'imatges/'+res['imdb']+"_back.jpg"
            posterurl = 'https://img.tviso.com'+'/{}{}{}'.format(res['images']['country'], IMG['fonsL'],res['images']['poster'])
            backurl = 'https://img.tviso.com'+'/{}{}{}'.format(res['images']['country'], IMG['posterL'],res['images']['backdrop'])
            print(posterurl, posterFile )
            print(backurl, backdropFile )
            #descarreguem la imatge amb un WGET de consola normal i corrent
            os.system("wget -O {0} {1}".format(posterFile, posterurl))
            os.system("wget -O {0} {1}".format(backdropFile, backurl))
            
            return True
        else:
            print('sense imatge')        
            return False
        
    def addSerie(self, idm, media_type):
        
        tviso =  TViso()
        res = tviso.getFullInfo( idm, media_type).json()
        try:
            #provem de guardar la foto
            
#             if isinstance(res['images'], dict):
#                 posterFile = self.root+'imatges/'+res['imdb']+"_poster.jpg"
#                 backdropFile = self.root+'imatges/'+res['imdb']+"_back.jpg"
#                 posterurl = 'https://img.tviso.com'+'/{}{}{}'.format(res['images']['country'], IMG['fonsL'],res['images']['poster'])
#                 backurl = 'https://img.tviso.com'+'/{}{}{}'.format(res['images']['country'], IMG['posterL'],res['images']['backdrop'])
#                 print(posterurl, posterFile )
#                 print(backurl, backdropFile )
#                 #descarreguem la imatge amb un WGET de consola normal i corrent
#                 os.system("wget -O {0} {1}".format(posterFile, posterurl))
#                 os.system("wget -O {0} {1}".format(backdropFile, backurl))
#                 
#             else:
#                 print('sense imatge')
            imageFile = self.root+'imatges/'+res['imdb']+"_poster.jpg"
            values = (int(res['imdb'][2:]),int(res['idm']), int(res['mediaType']), str(res['name']), str(res['status']), imageFile)
            self.c.execute("""insert into mycollection values (?,?,?,?,?,?)""",values)


        except sqlite3.IntegrityError:
            print("couldn't add serie  twice")
            
        except Exception as e:   
            
            print('error:\t'+str(e)+'...  \no no existeix...\n')

            
        #afegim els episodis a la taula capitols
            
        
        if res['mediaType'] == 1:
            for season in res['seasons'].keys():
                for e in res['seasons'][str(season)]:
                    estat =1
                    values = (int(e['idm']),int(e['media']['idm']), int(e['season']), int(e['num']),str(e['name']),str(e['plot']),estat, '')
                
                    print('-'*60)
                    ordre = """insert into capitols values (?,?,?,?,?,?,?,?)"""
                    try:
                        self.c.execute(ordre,values)
                    except sqlite3.IntegrityError:
                        print("couldn't add episode twice")
                    except Exception as e :    
                        print("epic fail: {}  ".format(e),ordre)
                    self.db.commit()
    def updateUserMedia(self):
        tviso = TViso()
        res = tviso.getUserSumary().json()
        pprint(res)
        threads = list()
        que = queue.Queue(4)
        for media in res['collection']['medias'].keys():
            print(media)
#            self.addSerie(media.split('-')[1],media.split('-')[0])
#######prova amb threads

            show =threading.Thread(target=self.addSerie, name= media, args=(media.split('-')[1],media.split('-')[0]))  
#            args =(media.split('-')[1],media.split('-')[0])
            imatge =threading.Thread(target=self.wgetImage, name=media.split('-')[1], args=(media.split('-')[1],media.split('-')[0]))
            threads.append(show)
            threads.append(imatge)
            
            show.start()
            imatge.start()
           
#            self.wgetImage(media.split('-')[1],media.split('-')[0])
        for episodi in res['collection']['episodes'].keys():
            data = datetime.fromtimestamp(res['collection']['episodes'][episodi]).strftime('%Y-%m-%d')
            print(data, episodi)
            self.c.execute("""UPDATE capitols SET date=? WHERE idm=?""", (str(data), int(episodi)))
            self.db.commit()
        self.settime()    

        
    
    def deleteSerie(self,tvmazeID):
        self.c.execute('SELECT image FROM myseries WHERE tvmazeID=?',(tvmazeID,))
        os.remove(self.c.fetchone()[0])
        self.c.execute('DELETE FROM myseries WHERE tvmazeID=?',(tvmazeID,))
        self.db.commit()
        self.c.execute('DELETE FROM capitols WHERE tvmazeID=?',(tvmazeID,))
        self.db.commit()

        
        
    def updatedb(self):
        i = floor(self.lastId/250)
        print('Pagina:',i)
        info = Info()
        while True:
            r = info.tvShowList(i)
            if r ==[]:
                break
            

            i += 1
            if r:
                for show in r:

                    nom = str(show['name'])
                    idtvmaze = show['id']
                    
                    imatge = ''
                    try:
                        imatge = show['image']['original']
                        print(imatge)
                    except TypeError:
                        imatge = 'None'
                        print(show['image'])
                        
                    try:
                        sino = show['summary']
                    except:
                        sino =''
                        
                    imdb = show['externals']['imdb']
                    if thetvdb == None:
                        thetvdb =0
                    rating = show['rating']['average']
                    if rating ==None:
                        rating = 0
#                     titol = nom
#                     idKey = idtvmaze
#                     tvdb = thetvdb
#                     print('-'*60)
#                     print('Nom', '\t', nom)
#                     print('TVMazeId','\t',idtvmaze)
#                     print('imatge','\t',imatge)
#                     print('thetvdb','\t',thetvdb)
#                     print('Rate', '\t',rating)
                    row =( int(imdb[2:]), str(idtvmaze), str(nom), str(imatge),str(rating),sino)
                    ordre = """insert into series values (?,?,?,?,?,?)"""
                    
                    print(ordre)
                    try:
                        self.c.execute(ordre,row)
                        
                    except sqlite3.IntegrityError:
                        print('"could not add "'+row[2]+'" twice')
    
                    except :    
                        print('No ha funcionat',row)
                    self.db.commit()
                    
        for serie in self.getSeriesList('myseries'):
            self.addSerie(int(serie[0]))
        
        self.settime()    
    
    def getSeriesList(self,table,  filtre=None ):
        extra = ' ORDER BY name DESC'
        ordre = "SELECT name,rating, tvmazeID FROM " + table
        if isinstance(filtre, str) and filtre is not '':
                ordre = ordre + " WHERE instr(UPPER(name) , UPPER('{}'))>0".format(filtre)
            
#         ordre += extra
#         print(filtre)
        print(ordre)
        self.c.execute(ordre)
        return [[str(row[2]),row[0],row[1]] for  row in self.c]
    
    def getShowId(self,id):
        '''
        Aconsegueix la serie amb la id de tvmaze
        '''
        self.c.execute('SELECT * FROM series WHERE tvmazeID=?',(id,))
        
        return  [column for column in self.c]


db =SickRucDB()
#db.settime()
# print(db.getShowId(67))
#db.getSeriesList('myseries')
#db.updatedb()
#db.c.execute('insert into series values (756,4455,"jhon nieve","imatge")')
#db.db.commit()
#db.addSerie(613,1)
db.updateUserMedia()
#db.addSerie(23)
#db.addSerie(643)

#db.c.execute("SELECT * FROM capitols")
#print(db.c.fetchone())

