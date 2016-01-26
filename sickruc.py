'''
Created on 11 gen. 2016

@author: albert
'''
import sys, urllib, requests, infosearch
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QSizeGrip, QHeaderView, QListWidgetItem, QRadioButton, QTreeWidgetItem , QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from divixtotal import DivixTotal
from db import SRDB
from db.SRDB import SickRucDB
from _io import StringIO
import torrentSearch


#Clase heredada de QMainWindow (Constructor de ventanas)
class Ventana(QMainWindow):
    #Método constructor de la clase
    def __init__(self, bd='db/'):
        #Iniciar el objeto QMainWindow
        QMainWindow.__init__(self)
        #Cargar la configuración del archivo .ui en el objeto
        uic.loadUi("SickRuc3.ui", self)
        #self.setWindowTitle("Cambiando el título de la ventana")
        self.db = SickRucDB(bd)
        self.inf = infosearch.Info()
        self.tabs = []
        for motor in torrentSearch.buscadors.keys():
            self.comboMotors.addItem(motor)
        self.index =0
        ###
        ###Configuracio de l'arbre episodis
        ###
        self.treeEpisodis.setHeaderHidden(False)


#         self.db.addSerie(32)
        
        
        
        ###########################################################
        ###                    ACCIONS                        #####
        ###                                                   #####
        ###                                                   #####
        ###########################################################

        
        ###########################################################
        ###            PESTANYA TORRENTS                      #####
        ###########################################################
        self.buto_busqueda.clicked.connect(self.buscaEvent)

        
        ###########################################################
        ###            PESTANYA SERIES                        #####
        ###########################################################
        
          
        #global\Local
        self.radioLocal.toggled.connect(self.getItems)
        self.radioGlobal.toggled.connect(self.getItems)
        #afegir borrar series de la llista 
        #   add        lambda: self.db.addSerie(self.listShows.currentItem().text(0))
        #   delete     lambda: self.db.deleteSerie(self.listShows.currentItem().text(0))
        self.btnAddShow.clicked.connect(self.addShow)
        self.btnDeleteShow.clicked.connect(self.deleteShow)
        
        #filtra resultats
        self.lineFiltra.textChanged.connect(lambda: self.getItems(self.lineFiltra.text()))
        #mostra informacio
        self.listShows.clicked.connect(lambda: self.setShowInfo(self.listShows.currentItem()))
        #mostra info capitol
        self.treeEpisodis.clicked.connect(lambda: self.setEpisodiInfo(self.treeEpisodis.currentItem()))
        #al seleccionar un capitol
        self.treeEpisodis.itemChanged.connect (self.seleccioCapitol)

        
        
        
        
        self.radioLocal.setChecked(True)

#     def closeEvent(self, event):
#         resultat = QMessageBox.question(self,"sortir...","Vols sortir de l'aplicacio?",QMessageBox.Yes | QMessageBox.No)
#         if resultat == QMessageBox.Yes: 
#             self.db.dbstop()
#             event.accept()
#         else: event.ignore()
#   
        ###########################################################
        ###                  TORRENTS                         #####
        ###########################################################

    def buscaEvent(self):
#         busqueda = DivixTotal().busca(str(self.text_busqueda.text()),self.check_series.isChecked())

        busqueda = torrentSearch.busca(motor = self.comboMotors.currentText(), paraula=str(self.text_busqueda.text()),divixserie=self.check_series.isChecked())
        print(self.comboMotors.currentText(),self.text_busqueda.text(),self.check_series.isChecked())
        #busqueda = DivixTotal().busca('fargo',True)
        self.treeResultat.clear()
        for k in busqueda.keys():
            row = [k,busqueda[k]]
            print(row)
            self.treeResultat.insertTopLevelItems(0,[QTreeWidgetItem(self.treeResultat, row)])

#             item = QListWidgetItem(k)
#             self.list_resultat.addItem(item)      
    
    def setTorrentInfo(self):
        motor = self.comoMotors
        if motor == 'divixtotal':
            
            pass
        elif motor == 'elitetorrent':
            pass
        elif motor == 'kickass':
            pass
 
        ###########################################################
        ###                    SERIES                        #####
        ###########################################################
    def deleteShow(self):
        '''
        crida la bd per BORRAR una serie de myseries
        '''
        num = self.listShows.currentItem().text(0)
        self.db.deleteSerie(num)
        self.getItems()
        print(num)
        
    def addShow(self):   
        '''
        crida la bd per AFEGIR una serie de myseries
        '''

        num = int(self.listShows.currentItem().text(0))
 
        self.db.addSerie(num)
        print(num)
        
    
             
    def getItems(self, filtra='' ):
        '''
        Busca i mostra series a la llista lateral
        @param filtra: Text de filtratge pe a la busqueda
        '''
        self.listShows.clear()
        if isinstance(filtra,   bool):
            filtra =''
        table = None
        #comprovem quina llista esta seleccionada Local/Global
        if self.radioLocal.isChecked():
            table = 'myseries'
        if self.radioGlobal.isChecked():
            table ='series'
            
           
            
        # Iterem per poblar||
        #--------- crida base dades --- (GLOB/LOC,TEXT)    
        for row in self.db.getSeriesList(table,filtra):
            
            #afegim item 
            #Seleccio deltreeWidget afegir a dalt(columna,[objecte])
            self.listShows.insertTopLevelItems(0,[QTreeWidgetItem(self.listShows, row)])
  
#             print(row)
    
    def setImage(self, url): 
        '''
        donada una url assigna la imatge de la serie
        '''
        data=None
        pixmap = QPixmap()
        print(url[:5])
        
        if url == None:
            print('Not image url ')
            return false
            
        #accedim a la imatge de la url
        
        elif url[:4] == 'http':
            #en cas de ser una url
            #    recollim la url de la imatge . la llegim
            data = urllib.request.urlopen(url).read()
            #config pixmap amb load from data
            pixmap.loadFromData(data)

        else:
            # en cas de ser de la coleccio local
            #nomes cal dfer servir Load
            pixmap.load(url)
        
        try:
            #creem i assignem la 
            # Objecte label ---------- imatge - escalem (tamany definit de Label), Mante l'aspecte, ???)
        
            self.labelImatge.setPixmap(pixmap.scaled(self.labelImatge.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))    
            return True
        except:
            self.labelImatge.setText('Sense imatge')
            return False

    def setShowInfo(self, item):
        '''
        Emplena el quadre de Informacio
        @param item: linia de la llista lateral
        '''
        local = self.radioLocal.isChecked()
        info = None
        if local:
            print(item.text(0))
            
            tvmaID = item.text(0)
            #info =self.db.getShowId(tvmaID)[0]
            self.db.c.execute('SELECT * FROM myseries WHERE tvmazeID=?',[item.text(0),])
            info =[row for  row in self.db.c][0]
            print('local:\n',info)
#             self.labelTitol.setText(info[0][2])
#             self.labelRating.setText(info[0][4])
#             self.setImage(info[0][3])
#             self.setSinopsy(info[0][5])
#             self.addEpisodis(tvmaID)
        else:
            tvmaID = item.text(0)
            info =self.db.getShowId(tvmaID)[0]
            self.db.c.execute('SELECT * FROM myseries WHERE tvmazeID=?',[item.text(0),])
            #info =[row for  row in self.db.c]
            print('Global:\n',info)
            
        self.labelTitol.setText(info[2])
        self.labelRating.setText(info[4])
        self.setImage(info[3])
        self.setSinopsy(info[5])
        self.addEpisodis(tvmaID)
        
    def setEpisodiInfo(self, item):
        try:
#         print([item.text(0),item.text(1),item.text(2)])
            self.db.c.execute('SELECT sinopsis FROM capitols WHERE titol=?',(item.text(2),))
            self.setSinopsy(self.db.c.fetchone()[0])
        except:
            print('Episodi info no actualitzat')
        
    def setSinopsy(self,text= 'Sinopsis....'):   
        self.labelSinopsi.setText(text) 
        
    def addEpisodis(self,tvmaID):
        self.treeEpisodis.clear()
        parent =self.treeEpisodis.invisibleRootItem()
        col =0
        seasons = {}
        for row in self.inf.tvShowInfo(tvmaID, True):
            if row['season']  not in seasons.keys():
                seasons[row['season']] = [[str(row['number']),row['name']]]
            else:
                seasons[row['season']].append([str(row['number']),row['name']])
        for k in seasons.keys():

            s = QTreeWidgetItem(parent, ['Season '+ str(k)])
            s.setData(col, Qt.UserRole,'Temporada')
            for e in seasons[k]:

                row = QTreeWidgetItem(s,['',e[0],e[1]])
                row.setData(1,Qt.UserRole,'Episodi')
                row.setCheckState (0,Qt.Unchecked)

                             
#             linia = [str(row['season']),str(row['number']),row['name']]
#             self.treeEpisodis.insertTopLevelItems(0,[QTreeWidgetItem(self.treeEpisodis,linia)])
        print("Arbre d'episodis acyualitzat")
    def seleccioCapitol(self,item,column):    
        print(item.text(column),column)
        try:
            if item.checkState(column) == Qt.Checked:
                self.db.c.execute('UPDATE capitols SET estat=? WHERE titol=?',(1,item.text(2)))    
                self.db.db.commit()
                self.db.c.execute('SELECT estat FROM capitols WHERE titol=?',(item.text(2),))   
                print('ESTAT:',self.db.c.fetchone())
                
                print("checked", item, item.text(2))
            if item.checkState(column) == Qt.Unchecked:
                
                self.db.c.execute('UPDATE capitols SET estat=? WHERE titol=?',(0,item.text(2)))    
                self.db.db.commit()
                self.db.c.execute('SELECT estat FROM capitols WHERE titol=?',(item.text(2),))                  
                print('ESTAT:',self.db.c.fetchone()[-1])
                print("unchecked", item, item.text(2))
        except:
            print('seleccio capitol fallada')
        
        
if __name__ == '__main__':
    #Instancia para iniciar una aplicación
    app = QApplication(sys.argv)
    #Crear un objeto de la clase
    _ventana = Ventana()
    #Mostra la ventana
    _ventana.show()
    #Ejecutar la aplicación
    app.exec_()