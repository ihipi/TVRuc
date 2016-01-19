'''
Created on 16 gen. 2016

@author: albert
'''
import sqlite3
from infosearch import Info
from math import floor


class SickRucDB():
    '''
    classdocs
    '''


    def __init__(self, lloc=''):
        '''
        Constructor
        '''
        self.dbname = 'sicruc.db'
        self.db = sqlite3.connect(lloc +self.dbname)
        self.c = self.db.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS series (tvmazeID INTEGER PRIMARY KEY not NULL,thetvdb INTEGER, name TEXT, image TEXT)')
        self.c.execute('CREATE TABLE IF NOT EXISTS myseries (tvmazeID INTEGER PRIMARY KEY not NULL,thetvdb INTEGER, name TEXT, image TEXT)')
        self.c.execute('create table if not exists capitols (id TEXT PRIMARY KEY not NULL, tvmazeID INTEGER, season INTEGER, capitol INTEGER, titol TEXT,emisio text )')
        
    
    def dbstart(self):
        self.db = sqlite3.connect(self.dbname)
        self.c = self.db.cursor()
    def dbstop(self):
        self.db.close()

    def lastID(self):
        
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
        resposta = self.c.fetchone()
        var = (resposta[0],resposta[1],resposta[2],resposta[3])
        try:
            self.c.execute("""insert into myseries values (?,?,?,?)""",var)
        except sqlite3.IntegrityError:
            print("couldn't add "+resposta[2]+" twice")
            
        except:   
            print('La serie ja esta afegida o no existeix')
        r = infoShow.tvShowInfo(tvmazeId, True)
        if r == []:
            print("El codi 'tvmazeId' no existeix")
        else:
            
            for l in r:
                idCapitol = ''+ str(tvmazeId) + '-' + str(l['season']).zfill(2)+'-'+str(l['number']).zfill(2)
                sinopsi = l['summary']
                print('-'*60)
                cap = (idCapitol,tvmazeId,l['season'],l['number'],l['name'],l['airdate'])
                ordre = """insert into capitols values (?,?,?,?,?,?)"""
                try:
                    self.c.execute(ordre,cap)
                except sqlite3.IntegrityError:
                    print("couldn't add "+resposta[2]+'-'+idCapitol[len(idCapitol)-5:]+" twice")
                except :    
                    print("epic fail:   ",ordre)
                self.db.commit()

    def updatedb(self):
        i = floor(self.lastID()/250)
        print('Pagina:',i)
        info = Info()
        while True:
            e =0
            r = info.tvShowList(e)
            if r ==[]:
                break
            e = e +1
            if e >2:
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
                    row =( int(idtvmaze), str(thetvdb), str(nom), str(imatge),str(rating))
                    ordre = """insert into series values ({},{},'{}','{}')""".format(row[0],row[1],row[2],row[3])
                    
                    print(ordre)
                    try:
                        self.c.execute(ordre)
                    except :    
                        print(ordre)
                    self.db.commit()
    
    def getSeriesList(self,table):
        extra = 'order by rating asc'
        ordre = "SELECT * FROM " + table
        self.c.execute(ordre)
        return [row[2] for row in self.c]

            
#db = SickRucDB()
#db.getSeriesList('myseries')
#db.updatedb()
#db.c.execute('insert into series values (756,4455,"jhon nieve","imatge")')
#db.db.commit()
#db.addSerie(81)
#db.c.execute("SELECT * FROM capitols")
#print(db.c.fetchone())

