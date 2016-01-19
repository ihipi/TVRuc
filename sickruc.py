'''
Created on 11 gen. 2016

@author: albert
'''
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem, QRadioButton
from PyQt5 import uic
#from divixtotal import DivixTotal
from db import SRDB
from db.SRDB import SickRucDB


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
        self.tabs = []
        self.index =0
        self.buto_busqueda.clicked.connect(self.buscaEvent)
        
        self.radioLocal.clicked.connect(self.getItems)
        self.radioGlobal.clicked.connect(self.getItems)
        

#     def closeEvent(self, event):
#         resultat = QMessageBox.question(self,"sortir...","Vols sortir de l'aplicacio?",QMessageBox.Yes | QMessageBox.No)
#         if resultat == QMessageBox.Yes: event.accept()
#         else: event.ignore()
    

    
    def buscaEvent(self):
        busqueda = DivixTotal().busca(str(self.text_busqueda.text()),self.check_series.isChecked())
        print(self.text_busqueda.text())
        #busqueda = DivixTotal().busca('fargo',True)
        self.list_resultat.clear()
        for k in busqueda.keys():
            item = QListWidgetItem(k)
            self.list_resultat.addItem(item)
        
    def getItems(self, ):
        '''
        Selecciona un item de la llista
        '''
        self.listShows.clear()
        table = None
        if self.radioLocal.isChecked():
            table = 'myseries'
        if self.radioGlobal.isChecked():
            table ='series'
        for name in self.db.getSeriesList(table):
            item = QListWidgetItem(name)
            self.listShows.addItem(name)
        print(self.db.getSeriesList(table))
        
if __name__ == '__main__':
    #Instancia para iniciar una aplicación
    app = QApplication(sys.argv)
    #Crear un objeto de la clase
    _ventana = Ventana()
    #Mostra la ventana
    _ventana.show()
    #Ejecutar la aplicación
    app.exec_()