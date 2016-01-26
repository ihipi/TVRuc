'''
Created on 16 gen. 2016

@author: albert
'''
import sqlite3, time, urllib,json,os
from infosearch import Info
from math import floor
from datetime import datetime
from tools import tools


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
        
        self.c.execute('CREATE TABLE IF NOT EXISTS series (tvmazeID INTEGER PRIMARY KEY not NULL,thetvdb INTEGER, name TEXT, image TEXT, rating TEXT, sinopsis TEXT)')
        self.c.execute('CREATE TABLE IF NOT EXISTS myseries (tvmazeID INTEGER PRIMARY KEY not NULL,thetvdb INTEGER, name TEXT, image TEXT, rating TEXT, sinopsis TEXT)')
        self.c.execute('create table if not exists capitols (id TEXT PRIMARY KEY not NULL, tvmazeID INTEGER, season INTEGER, capitol INTEGER, titol TEXT,emisio text, sinopsis TEXT,estat INTEGER )')
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
            self.updatedb()
        else:
            print('-'*50,'\nBase de dades actualitzada\n','-'*50)
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
    
    def addSerie(self, tvmazeId):
        
        infoShow =  Info()
        self.c.execute("""select * from series where tvmazeID=?""",(tvmazeId,))
        res = self.c.fetchone()
#        var = (res[0],res[1],res[2],res[3], res[4],res[5])
        var = [r for r in res]
        try:
            #provem de guardar la foto
            if res[3 ]!= 'None':
                imatgeFile = self.root+'imatges/'+str(res[0])+'_'+res[2]+".jpg"
                urllib.request.urlretrieve(res[3], imatgeFile )
                var[-3]= imatgeFile
            else:
                print('sense imatge')
            self.c.execute("""insert into myseries values (?,?,?,?,?,?)""",var)


        except sqlite3.IntegrityError:
            print("couldn't add "+res[2]+" twice")
            
        except:   
            
            print('error  o no existeix...\n',var)
            print([type(v) for v in var])
            
        #afegim els episodis a la taula capitols
            
        r = infoShow.tvShowInfo(tvmazeId, True)
        if r == []:
            print("El codi 'tvmazeId' no existeix")
        else:
            
            for l in r:
                idCapitol = ''+ str(tvmazeId) + '-' + str(l['season']).zfill(2)+'-'+str(l['number']).zfill(2)
                
                print('-'*60)
                cap = (idCapitol,tvmazeId,l['season'],l['number'],l['name'],l['airdate'],l['summary'],0)
                ordre = """insert into capitols values (?,?,?,?,?,?,?,?)"""
                try:
                    self.c.execute(ordre,cap)
                except sqlite3.IntegrityError:
                    print("couldn't add "+res[2]+'-'+idCapitol[len(idCapitol)-5:]+" twice")
                except :    
                    print("epic fail:   ",ordre)
                self.db.commit()

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
                        
                    thetvdb = show['externals']['thetvdb']
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
                    row =( int(idtvmaze), str(thetvdb), str(nom), str(imatge),str(rating),sino)
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


#db =SickRucDB()
#db.settime()
# print(db.getShowId(67))
#db.getSeriesList('myseries')
#db.updatedb()
#db.c.execute('insert into series values (756,4455,"jhon nieve","imatge")')
#db.db.commit()
# db.addSerie(86)
#db.addSerie(23)
#db.addSerie(643)

#db.c.execute("SELECT * FROM capitols")
#print(db.c.fetchone())

