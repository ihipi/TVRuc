'''
Created on 24 gen. 2016

@author: albert
'''
import elitetorrent, divixtotal





'''
Constructor
'''
buscadors = {'divixtotal':divixtotal.DivixTotal(),
                  'elitetorrent':elitetorrent.Eliterorrent(),
                  'kickass':''}

def busca(motor, paraula, divixserie = False):
    print('torrentsearch:',motor,paraula, divixserie)
    motorB = buscadors[motor]

    if motor == 'divixtotal':
        return motorB.busca(paraula,divixserie)        
    elif motor == 'elitetorrent':
        return motorB.busca(paraula)        
    elif motor == 'kickass':
        pass
    
    
    
