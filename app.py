'''________________________________________________________________________
					
					Instituto Tecnologico de Costa Rica
					     Lenguajes de Programacion	
					     Tercera Tarea Programada 
					     App Web en Python-SML
					
					Realizado por: 
					        * Josue Espinoza Castro 
						* Mauricio Gamboa Cubero
						* Andres Pacheco Quesada

					Junio del 2014
__________________________________________________________________________'''

#Imports del framework para la aplicacion web: Flask
from flask import Flask, request, redirect, url_for, abort, session, render_template, flash
from werkzeug.utils import secure_filename
import os

#Configuracion de guardar archivos
UPLOAD_FOLDER = '/home/josue/TP3_sml'
ALLOWED_EXTENSIONS = set(['sml'])

#Nombre de la aplicacion: Bumbur
app = Flask("SML")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Para usar flash
#app.secret_key = 'josue'

#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------			FRONTEND	   ------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

#URL y funcion para home
@app.route('/')
def home():
	return render_template('home.html')


@app.route('/felicidades', methods=['GET', 'POST'])
def felicidades():
	##dinamico = [["x","999","Global"],["y","True","Let1"]]
	##estatico = [["x","int","Global"],["y","boolean","Let1"]]
	if request.method == 'POST':
		file = request.files['file']
		if file and archivoPermitido(file.filename):
			nombre = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre))
			#leersml(nombre) y generar las listas para las tablas
			#dinamico = leersml(nombre)[1] 
			#estatico = leersml(nombre)[2]
			#["x",3,"int","global","int"]
			print("Nombre del archivo: ",nombre)
			final = leersml(nombre)
			final.reverse()
			print("TERMINO DE HACER LEERSML")
			dinamico = []
			estatico = []
			for e in final: #cada val
				dinamico += [[e[0],e[1]]]
				estatico += [[e[0],e[2]]]
			print("Dinamico: ",dinamico)
			print("Estatico: ",estatico)
			borrarArchivo(nombre)
			global lista
			global lista2
			lista = []
			lista2 = []
			return render_template('felicidades.html',dinamico=dinamico,estatico=estatico)
		else:
			return redirect(url_for('error'))
	return render_template('felicidades.html')

@app.route('/error', methods=['GET', 'POST'])
def error():
	return render_template('error.html')


#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------			BACKEND		   --------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

#Funcion que evalua la extension sml del archivo
def archivoPermitido(nombre):
	boolean = '.' in nombre and nombre.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
	return boolean

#Funcion para borrar un archivo en uploads despues de ser evaluado
def borrarArchivo(nombre):
	os.remove("/home/josue/TP3_sml/"+nombre)

#Al comenzar, se borran los archivo en la carpeta Uploads
filelist = [ f for f in os.listdir("/home/josue/TP3_sml") if f.endswith(".sml") ]
for f in filelist:
	borrarArchivo(f)

####################################################################################################################
import re
global lista2
lista2=[]


def leersml(nombre):
    archi=open(nombre,'r+')
    linea=archi.readline()
    while linea!="":
        dividirNueva(linea)
        linea=archi.readline()        
    archi.close()
    print("Matriz Leida",lista2)
    agrupada = agrupar(lista2,1,[],[])
    print("Agrupada: ",agrupada)
    transformada = transformar(agrupada)
    print("Transformada: ",transformada)
    almacenar(transformada)
    print("Lista: ",lista)
    return lista
    
def dividirNueva(linea):
    temp=re.split(' |;|\n|(=)*',linea)  
    try:
        while True:
            temp.remove(None)
    except ValueError:
            pass
    try:
        while True:
            temp.remove("\n")
    except ValueError:
        pass
    contador=temp.count('')
    while contador !=0:
        temp.remove('')
        contador -=1
    lista2.append(temp)

##pasadoFueLet
##pasadoFueLet = False

def agrupar(matriz,ide,valActual,agrupada2):
##    print(matriz)
    while matriz!=[]:
        agrupada=[]

################################################################################################################################################
        if ide==1: #val
##            print(matriz)
            vector=matriz[0]
            if vector!=[] and (vector[0]=='val' or vector[0]=='(val'):
                valActual += ['val']
                vector=vector[1:]
                matriz[0]=matriz[0][1:]
##                print(valActual)

            while vector!=[] and vector[0] not in {'val','let','if','(val','(let','(if'}: ## vector[0]!='val' or vector[0]!='let' or vector[0]!='if': ##
                valActual += [vector[0]]                
                vector=vector[1:]
                matriz[0]=matriz[0][1:]
            #termino el val bien, sml bonito
            if vector == [] and len(matriz)>=2 and len(matriz[1])>= 1 and matriz[1][0] in {'val','let','if','(val','(let','(if'}:
                agrupada+=valActual
                if matriz[1][0]=='val' or matriz[1][0]=='(val':
                    matriz = matriz[1:]
                    return agrupar(matriz,1,[],agrupada2+[agrupada])
                elif matriz[1][0]=='let' or matriz[1][0]=='(let':
                    agrupada+=[[]]
                    matriz = matriz[1:]
                    return agrupar(matriz,2,[],agrupada2+[agrupada])
                elif matriz[1][0]=='if' or matriz[1][0]=='(if':
                    matriz = matriz[1:]
                    return agrupar(matriz,3,[],agrupada2+agrupada)
                    
            #No ha terminado el val, sigue en la siguiente linea (lista)     
            elif vector == [] and len(matriz)>=2 and len(matriz[1])>= 1 and matriz[1][0] not in {'val','let','if','(val','(let','(if'}:
                matriz=matriz[1:]
                return agrupar(matriz,1,valActual,agrupada2)

            #ya termino el val, sigue en la misma linea la siguiente expresion    
            elif vector != [] and vector[0] in {'val','let','if','(val','(let','(if'}:
                if vector[0]=='val' or vector[0]=='(val':
                    return agrupar(matriz,1,[],agrupada2+[agrupada]) 
                elif vector[0]=='let' or vector[0]=='(let':
##                    agrupada+=[valActual]                 
##                    agrupada=[agrupada]
                    return agrupar(matriz,2,valActual,agrupada2+agrupada)
                elif vector[0]=='if' or vector[0]=='(if':
                    agrupada+=[valActual]
                    return agrupar(matriz,3,[],agrupada2+agrupada)
            elif len(matriz)==1 and matriz[0]==[]:
                matriz=matriz[1:]
                agrupada2+=[valActual]
                return agrupada2

##        if ide==1: #val
##
##            vector=matriz[0]
##            if vector!=[] and (vector[0]=='val' or vector[0]=='(val'):
##                valActual += ['val']
##                vector=vector[1:]
##                matriz[0]=matriz[0][1:]
##
##            while vector!=[] and vector[0] not in {'val','let','if','(val','(let','(if'}: 
##                valActual += [vector[0]]                
##                vector=vector[1:]
##                matriz[0]=matriz[0][1:]
##                
##            #termino el val bien, sml bonito
##            if vector == [] and len(matriz)>=2 and len(matriz[1])>= 1 and matriz[1][0] in {'val','let','if','(val','(let','(if'}:
##                agrupada+=[valActual]
##                global pasadoFueLet
##                if pasadoFueLet:
##                    pasadoFueLet = False
##                    if matriz[1][0]=='val' or matriz[1][0]=='(val':
##                        matriz = matriz[1:]
##                        agrupada2[-1]+=agrupada
##                        return agrupar(matriz,1,[],agrupada2)
##                    elif matriz[1][0]=='let' or matriz[1][0]=='(let':
##                        matriz = matriz[1:]
##                        agrupada2[-1]+=agrupada
##                        return agrupar(matriz,2,[],agrupada2)
##                    elif matriz[1][0]=='if' or matriz[1][0]=='(if':
##                        matriz = matriz[1:]
##                        agrupada2[-1]+=agrupada
##                        return agrupar(matriz,3,[],agrupada2)
##                else:
##                    if matriz[1][0]=='val' or matriz[1][0]=='(val':
##                        matriz = matriz[1:]
##                        return agrupar(matriz,1,[],agrupada2+agrupada)
##                    elif matriz[1][0]=='let' or matriz[1][0]=='(let':
##                        matriz = matriz[1:]
##                        return agrupar(matriz,2,[],agrupada2+agrupada)
##                    elif matriz[1][0]=='if' or matriz[1][0]=='(if':
##                        matriz = matriz[1:]
##                        return agrupar(matriz,3,[],agrupada2+agrupada)
##                    else:
##                        matriz = [[]]+matriz
##                        
##            #No ha terminado el val, sigue en la siguiente linea (lista)     
##            elif vector == [] and len(matriz)>=2 and len(matriz[1])>= 1 and matriz[1][0] not in {'val','let','if','(val','(let','(if'}:
##                matriz=matriz[1:]
##                return agrupar(matriz,1,valActual,agrupada2+agrupada)
##
##            #ya termino el val, sigue en la misma linea la siguiente expresion    
##            elif vector != [] and vector[0] in {'val','let','if','(val','(let','(if'}: #and len(matriz)>1 and matriz[1] != []:
##                agrupada+=[valActual]
##                global pasadoFueLet
##                if pasadoFueLet:
##                    pasadoFueLet = False
##                    if vector[0]=='val' or vector[0]=='(val':
####                        matriz = matriz[1:]
##                        agrupada2[-1]+=agrupada
##                        return agrupar(matriz,1,[],agrupada2)
##                    elif vector[0]=='let' or vector[0]=='(let':
####                        matriz = matriz[1:]
##                        agrupada2[-1]+=agrupada
##                        return agrupar(matriz,2,[],agrupada2)
##                    elif vector[0]=='if' or vector[0]=='(if':
####                        matriz = matriz[1:]
##                        agrupada2[-1]+=agrupada
##                        return agrupar(matriz,3,[],agrupada2)
##                else:
##                    if vector[0]=='val' or vector[0]=='(val':
####                        matriz = matriz[1:]
##                        return agrupar(matriz,1,[],agrupada2+agrupada)
##                    elif vector[0]=='let' or vector[0]=='(let':
####                        matriz = matriz[1:]
##                        return agrupar(matriz,2,[],agrupada2+agrupada)
##                    elif vector[0]=='if' or vector[0]=='(if':
####                        matriz = matriz[1:]
##                        return agrupar(matriz,3,[],agrupada2+agrupada)
####                    else:
####                        matriz = [[]]+matriz
##                        
##            elif len(matriz)==1 and matriz[0]==[]:
##                matriz=matriz[1:]
##                if pasadoFueLet:
##                    agrupada2[-1]+=[valActual]
##                    apenasDespuesDelLet = False
##                else:
##                    agrupada2+=[valActual]
##                return agrupada2
##
##            elif vector != [] and vector[0] in {'val','let','if','(val','(let','(if'}:
##                agrupada+=[valActual]
##                global pasadoFueLet
##                if pasadoFueLet:
##                    pasadoFueLet = False
##                    if matriz[0][0]=='val' or matriz[0][0]=='(val':
##                        agrupada2[-1]+=agrupada
##                        return agrupar(matriz,1,[],agrupada2)
##                    elif matriz[0][0]=='let' or matriz[0][0]=='(let':
##                        agrupada2[-1]+=agrupada
##                        return agrupar(matriz,2,[],agrupada2)
##                    elif matriz[0][0]=='if' or matriz[0][0]=='(if':
##                        agrupada2[-1]+=agrupada
##                        return agrupar(matriz,3,[],agrupada2)
##                else:
##                    if matriz[0][0]=='val' or matriz[0][0]=='(val':
##                        return agrupar(matriz,1,[],agrupada2+agrupada)
##                    elif matriz[0][0]=='let' or matriz[0][0]=='(let':
##                        return agrupar(matriz,2,[],agrupada2+agrupada)
##                    elif matriz[0][0]=='if' or matriz[0][0]=='(if':
##                        return agrupar(matriz,3,[],agrupada2+agrupada)
####                    else:
####                        matriz = [[]]+matriz

################################################################################################################################################
                            
        elif ide==2: #let
            vector=matriz[0]
            if vector!=[] and (vector[0]=='let' or vector[0]=='(let'):
                valActual+=[[]]
                valActual[-1]+= ['let']
                valActual[-1]+=[[]]
##                print(valActual)
                vector=vector[1:]
                matriz[0]=matriz[0][1:]
                if vector[0]=='val' or vector[0]=='(val':
                    valActual[-1][-1]+=['val']
                    vector=vector[1:]
                    matriz[0]=matriz[0][1:]
##                    print("If que entra si el vector[0] es val",vector[0])
            while vector!=[] and vector[0] not in {'val','(val','let','(let','if','(if','in','end','end)'}: ##Mete todo lo que tenga el let hasta antes del in
                valActual[-1][-1]+=[vector[0]]
                vector=vector[1:]
                matriz[0]=matriz[0][1:]
                    

            if vector != [] and vector[0] in {'val','(val','let','(let','if','(if','end','end)'}:

                agrupada+=[valActual]
                if vector[0]=='val' or vector[0]=='(val':
                    agrupada2[-1]+=agrupada
                    return agrupar(matriz,1,[],agrupada2)
                elif vector[0]=='let' or vector[0]=='(let':
                    agrupada2[-1]+=agrupada
                    return agrupar(matriz,2,[],agrupada2)
                elif vector[0]=='if' or vector[0]=='(if':
                    agrupada2[-1]+=agrupada
                    return agrupar(matriz,3,[],agrupada2)
                    
                    
                    
                
            if vector!=[] and vector[0]=='in':
##                print('Si vector es distinto de vacio y vector[0] es in',vector[0])
                valActual+=['in']
                vector=vector[1:]
                matriz[0]=matriz[0][1:]
                while vector!=[] and vector[0] not in {'val','(val','let','(let','if','(if'}:
##                    print(vector[0])
                    valActual+=[vector[0]]
                    vector=vector[1:]                        
                    matriz[0]=matriz[0][1:]
                    
            if vector!=[] and (vector[0]=='end' or vector[0]=='end)'):
                valActual+=['end']
                vector=vector[1:]
                matriz[0]=matriz[0][1:]
                agrupada+=valActual
                return agrupar(matriz,2,valActual,agrupada2)

                    
            elif vector == [] and len(matriz)>=2 and len(matriz[1])>= 1: ## and matriz[1][0]=='in':                    
                matriz=matriz[1:]
##                valActual+=[vector[0]]
                return agrupar(matriz,2,valActual+[],agrupada2)

            elif vector == [] and len(matriz)>=2 and len(matriz[1])>= 1 and matriz[1][0] in {'val','(val','let','(let','if','(if'}:  
                matriz=matriz[1:]
                valActual+=[[]]
##                valActual+=[vector[0]]
##                    print('in',vector[0])
                return agrupar(matriz,2,valActual,agrupada2)


            elif vector == [] and len(matriz)>=2 and len(matriz[1])>= 1 and matriz[1][0] not in {'val','(val','let','(let','if','(if'}:
                matriz=matriz[1:]

##                valActual+=[vector[0]]
##                    print('in',vector[0])
                return agrupar(matriz,1,valActual,agrupada2)
            


            elif len(matriz)==1 and matriz[0]==[]:
                matriz=matriz[1:]
                agrupada2+=[valActual]
                return agrupada2
    
            
################################################################################################################################################

        elif ide==3: #if

            vector=matriz[0]
            if vector!=[] and (vector[0]=='if' or vector[0]=='(if'):
                valActual += ['if']
                vector=vector[1:]
                matriz[0]=matriz[0][1:]

            while vector!=[] and vector[0] not in {'val','(val','let','(let','if','(if'}: 
                valActual += [vector[0]]                
                vector=vector[1:]
                matriz[0]=matriz[0][1:]
            #termino el if bien, sml bonito
            if vector == [] and len(matriz)>=2 and len(matriz[1])>= 1 and matriz[1][0] in {'val','(val','let','(let','if','(if'}:
                agrupada+=[valActual]
                if matriz[1][0]=='val' or matriz[1][0]=='(val':
                    matriz = matriz[1:]
                    agrupada2[-1]+=agrupada
                    return agrupar(matriz,1,[],agrupada2)
                elif matriz[1][0]=='let' or matriz[1][0]=='(let':
                    matriz = matriz[1:]
                    agrupada2[-1]+=agrupada
                    return agrupar(matriz,2,[],agrupada2)
                elif matriz[1][0]=='if' or matriz[1][0]=='(if':
                    matriz = matriz[1:]
                    agrupada2[-1]+=agrupada
                    return agrupar(matriz,3,[],agrupada2)

            #No ha terminado el if, sigue en la siguiente linea (lista)     
            elif vector == [] and len(matriz)>=2 and len(matriz[1])>= 1 and matriz[1][0] not in {'val','(val','let','(let','if','(if'}:
                matriz=matriz[1:]
                return agrupar(matriz,3,valActual,agrupada2)

            #ya termino el if, sigue en la misma linea la siguiente expresion    
            elif vector != [] and vector[0] in {'val','(val','let','(let','if','(if'}:
                agrupada+=[valActual]
                if vector[0]=='val' or vector[0]=='(val':
                    agrupada2[-1]+=agrupada
                    return agrupar(matriz,1,[],agrupada2)
                elif vector[0]=='let' or vector[0]=='(let':
                    agrupada2[-1]+=agrupada
                    return agrupar(matriz,2,[],agrupada2)
                elif vector[0]=='if' or vector[0]=='(if':
                    agrupada2[-1]+=agrupada
                    return agrupar(matriz,3,[],agrupada2)
                
            elif len(matriz)==1 and matriz[0]==[]:
                matriz=matriz[1:]
                agrupada2[-1]+=[valActual]
                return agrupada2

    return agrupada2

##Otra implementacion de agrupar puede ser: if in {val,let etc} then return agrupar...(agrupada + agrupada(lo que viene)

##Funcion que cambia: ['x>','3'] en ['x','<','3']
def corregirLista(string):
    string = string.replace('+','!')
    string = string.replace('*','@')
    string = string.replace('))','EEE')
    string = string.replace('((','QQQ')
    string = string.replace('(','%')
    string = string.replace(')','&')
    string = string.replace('-','`')

    print(string)
    
    temp=re.split(',|(=)*(>)*(<)*(`)*(div)*(EEE)*(QQQ)*([)*(])*(mod)*(hd)*(tl)*(::)*(!)*(@)*(%)*(&)*',string)

    print(temp)
    
    try:
        while True:
            temp.remove(None)
    except ValueError:
            pass
    final = []
    for e in temp:
        e = e.replace('~','-')
        e = e.replace('`','-')
        e = e.replace('!','+')
        e = e.replace('@','*')
        e = e.replace('%','(')
        e = e.replace('&',')')
        if e == "EEE":
                final.append(')')
                final.append(')')
        elif e == "QQQ":
                final.append('(')
                final.append('(')
        else:
                final.append(e)
    try:
        while True:
            final.remove('')
    except ValueError:
            pass
    print(final)
    if final[0][0] == '[':
            final[0] = final[0][1:]
            final[-1] = final[-1][:-1]
    print(final)
    
    return final

def masDe2NivelesDeAnidacion(listaDos):
        if isinstance(listaDos[0],list):
                return True
    
def transformar(lista): #recursivo
    if lista == []:
        return []
    else:
        if isinstance(lista[0],list):
            l1 = transformar(lista[0])
            l2 = transformar(lista[1:])
            print("l1: ",l1)
            print("l2: ",l2)
            if l1 == []:
                return l2
            elif l2 == []:
                print("Cuando l2 es vacia, l1 es: ",l1)
                return l1
            else:
                if masDe2NivelesDeAnidacion(l2):
                        return [l1]+l2
                else:
                        return [l1] + [l2]
        else:
            resultado = []
            valorComplejo = ""
            hayIgual = False
            hayIf = False
            while lista != [] and not (isinstance(lista[0],list) and lista[0][0] in {'val','if','let'}):
                if lista[0] == '=':
                    hayIgual = True
                    resultado += [lista[0]]
                elif lista[0] == 'if':
                    hayIf = True
                    resultado += [lista[0]]
                elif lista[0] in {'then','else'}:
                    resultado += [corregirLista(valorComplejo)]
                    resultado += [lista[0]]
                    valorComplejo = ""
                elif hayIgual or hayIf:
                    valorComplejo+=lista[0]
                else:
                    resultado += [lista[0]]
                lista = lista[1:]
            if lista == []:
                if valorComplejo == "":
                    return resultado
                else:
                    valorComplejo = corregirLista(valorComplejo)
                    resultado += [valorComplejo]
                    return resultado
            else:
                resultado += [transformar(lista[0])]
                return resultado

##def analizaVal(line,variable):
##    if len(line[0])>1:
##        if line[0].isdigit():                                           
##            agregardatos(lista,var_temp,int(line[0]),'int')
##            return analizaVal(line[1:],var_temp)
##        elif line[0][0].isalpha():
##            if line[0][0]=='true' or line[0][0]=='false':
##                agregardatos(lista,var_temp,line[0],'bool')
##                var_temp=''
##                encontrarValor(line[1:],var_temp)
##            else:                    
##                if line[0].find('='):
##                    return analizaVal([line[0][line[0].find('='):]]+[line[1:]],line[0][:line[0].find('=')])
##                else:
##                    linear=line[0][0]
##                    while linear.isalpha():
##                        var_temp=var_temp+linear
##                        linear=line[0][1:]
##                    print(linear)
##                    return analizaVal(line,var_temp)
##                
##        elif line[0][0]=='=':
##            if line[0][1].isdigit():
##                agregardatos(lista,variable,line[0][1],'int')
##                variable=''
##                encontrarValor(line[2:],variable)
##        else:
##            return 'Error: No son valores de SML.'
##    elif len(line[0])==1:
##        if line[0].isdigit():
##            agregardatos(lista,var_temp,int(line[0]),'int')
##            analizaVal(line[1:],var_temp)
##        elif line[0].isalpha():
##            analizaVal(line[1:],line[0])
##        else:
##            if line[0]=='+' or line[0]=='/' or line[0]=='-' or line[0]=='*':
##                return 'Falta trabajar valores de operaciones.'
##            elif line[0].find('='):
##                return 'hola'
##                
##            else:
##                return 'Error: Este elemento no es valido en SML.'
##    else:
##        return 'Ya termino'

     
global lista
##lista=[["x",3,"int","global","int"],["z",5,"int","global","int"],["y","false","bool","global","bool"],["e",[5,4,3],"int list","global","list"],["f",[8,9,10],"int list","global","list"],["g",[3,4,9],"int list","global","list"],["k",("false",5,3),"(bool*int*int)","global","tuple"]]
lista = []

#Revisar las listas y tuplas


#re multiples delimitadores
import re
prioridaddp={"*":2,"div":2,"mod":2,"+":1,"-":1,"(":0}
prioridadfp={"*":2,"div":2,"mod":2,"+":1,"-":1,"(":5}

##def resolverLet(listaLet):
##        variables = []
##        while listaLet[0] != 'in': #son vals
##                x = "".join(listaLet[0])
##                        if x.count('[')>0 or x.count('::')>0:
##                                variables += [listaLet[0][1],opcons(listaLet[0][
##
##                listaLet=listaLet[1:]

##def resolverIf(listaIf):

def almacenar(matriz):
        for e in range(len(matriz)):
                print("Val: ",matriz[e])
                tipo = ""
                for p in range(len(matriz[e])):
                    print("Val[p]: ",matriz[e][p])
                    if isinstance(matriz[e][p],list) and matriz[e][p][0] not in {'val','if','let'}:
                            x = "".join(matriz[e][p])
                            print("x: ",x)
                            if x.count('[')>0: #x es lista
                                    tipo = analizador_lista(matriz[e][p])
                            elif x.count('(')>0:
                                    tipo = analizador_tupla(matriz[e][p])
                            else:
                                    matriz[e][p] = op(matriz[e][p])[0]
                                    tipo = 'int'
                agregardatos(matriz[e][1],matriz[e][3],tipo,'global',tipo)
                print("Lista: ",lista)
                        
##def almacenar(matriz):
####    print("MatrizEntrante: ",matriz)
##    for e in range(len(matriz)):
####        print("Val: ",matriz[e])
##        for p in range(len(matriz[e])):
####            print("Val[p]: ",matriz[e][p])
##            if isinstance(matriz[e][p],list) and matriz[e][p][0] not in {'val','if','let'}:
##                x = "".join(matriz[0])
##                if x.count('[') > 0 or x.count('::')>0:
##                        paraOpCons = True
##                else:
##                        paraOp = True
##                if paraOpCons:
##                        for e in range(len(matriz[0])):
##                                if matriz[0][e] == 'hd': #solo con 1 nivel de anidacion
##                                        matriz[0] = opcons(matriz[0])[0]
####                                        if matriz[0][e+1].isalpha(): #accede a una variabla
####                                                matriz[0][e]=
##                else:
##                        matriz[e][p] = op(matriz[e][p])[0]
####                print("Val[p] Nueva: ",matriz[e][p])
##            elif matriz[e][p][0] == 'let':
##                matriz[e][p] = resolverLet(matriz[e][p])
##            elif matriz[e][p][0] == 'if':
##                matriz[e][p] = resolverIf(matriz[e][p])    
####        print("Val: ",matriz[e])
##        agregardatos(matriz[e][1],int(matriz[e][3]),'int','global','int')
####        print("Lista: ",lista)

#Inserta datos al inicio de la lista.  
def agregardatos(variable,valor,tipo,scope,tipo2):
     temp_list=[[variable,valor,tipo,scope,tipo2]]
     global lista
     lista=temp_list+lista
     return lista

     
## resuelve operaciones elementales
def operacion(valor1,operando,valor2):
     if (isinstance(valor1,int) and isinstance(valor2,int)): 
          if operando=="+":
               return (valor1+valor2)
          elif operando=="-":
               return (valor1-valor2)
          elif operando=="*":
               return (valor1*valor2)
          elif operando=="div": #operando=="/" 
               return int(valor1/valor2)
          elif operando=="mod": #operando=="%" 
               return (valor1%valor2)
          else:
               print ("Operacion no permitida")
     elif (isinstance(valor1,int) and verificar_int(valor2)):
          if operando=="+":
               return (valor1+(obtener(valor2)))
          elif operando=="-":
               return (valor1-(obtener(valor2)))
          elif operando=="*":
               return (valor1*(obtener(valor2)))
          elif operando=="div": #operando=="/"
               return int(valor1/(obtener(valor2)))
          elif operando=="mod": #operando=="%" 
               return (valor1%(obtener(valor2)))
          else:
               print ("Operacion no permitida")
     elif (verificar_int(valor1) and isinstance(ConvertirInt(valor2),int)):
##          print("ENTREEEeEEEE AQUIII")
          if operando=="+":
               return ((obtener(valor1))+valor2)
          elif operando=="-":
               return ((obtener(valor1))-valor2)
          elif operando=="*":
               return ((obtener(valor1))*valor2)
          elif operando=="div": #operando=="/"
               return int((obtener(valor1))/valor2)
          elif operando=="mod": #operando=="%"
               return ((obtener(valor1))%valor2)
          else:
               print ("Operacion no permitida")

     elif (verificar_int(valor1) and verificar_int(valor2)):
          if operando=="+":
               return ((obtener(valor1))+(obtener(valor2)))
          elif operando=="-":
               return ((obtener(valor1))-(obtener(valor2)))
          elif operando=="*":
               return ((obtener(valor1))*(obtener(valor2)))
          elif operando=="div": #operando=="/"
               return int((obtener(valor1))/(obtener(valor2)))
          elif operando=="mod": #operando=="%"
               return ((obtener(valor1))%(obtener(valor2)))
          else:
               print ("Operacion no permitida")
     else:
          print ("operacion fallida")


def verificar_vacia(lista):
     if lista==[]:
          return True
     else:
          return False

def isNumber(s):
     try:
          d=int(str(s))
          if isinstance(d,int):
               return True
          
     except:
          return False

def ConvertirInt(s):
     try:
          d=int(str(s))
          return d
     except:
          return s
          
#Operar operaciones complejas
def op(string):
     contador=0
     pilaoperadores=[]
     pilanumeros=[]
     while contador<len(string):
          if (verificar_vacia(pilaoperadores) and (isNumber(string[contador]) or verificar_int(string[contador])) ):
               pilanumeros=insertafinal(pilanumeros,string[contador])
               contador+=1
          else:
               if verificar_vacia(pilaoperadores):
                    pilaoperadores=insertafinal(pilaoperadores,string[contador])
                    contador+=1
               elif (isNumber(string[contador]) or verificar_int(string[contador])):
                    pilanumeros=insertafinal(pilanumeros,string[contador])
                    contador+=1
               else:
                    if ((string[contador])==")"):
                         while (not verificar_vacia(pilaoperadores)):
                              if (obtiene_ultimo(pilaoperadores)=="("):
                                   pilaoperadores=eliminafinal(pilaoperadores)
                                   contador+=1
                                   break
                              else:
                                   valor2=ConvertirInt(obtiene_ultimo(pilanumeros))
                                   pilanumeros=eliminafinal(pilanumeros)
                                   valor1=ConvertirInt(obtiene_ultimo(pilanumeros))
                                   pilanumeros=eliminafinal(pilanumeros)
                                   res=operacion(valor1,obtiene_ultimo(pilaoperadores),valor2)
                                   #print(res)
                                   pilanumeros=insertafinal(pilanumeros,res)
                                   pilaoperadores=eliminafinal(pilaoperadores)
                    else:
                         ultimo=obtiene_ultimo(pilaoperadores)
                         if (prioridaddp[ultimo]<prioridadfp[string[contador]]):
                              pilaoperadores=insertafinal(pilaoperadores,string[contador])
                              contador+=1
                         else:
                              valor2=ConvertirInt(obtiene_ultimo(pilanumeros))
                              pilanumeros=eliminafinal(pilanumeros)
                              valor1=ConvertirInt(obtiene_ultimo(pilanumeros))
                              pilanumeros=eliminafinal(pilanumeros)
                              res=operacion(valor1,obtiene_ultimo(pilaoperadores),valor2)
                              pilanumeros=insertafinal(pilanumeros,res)
                              pilaoperadores=eliminafinal(pilaoperadores)
                              if (not verificar_vacia(pilaoperadores)):
                                   ultimo=obtiene_ultimo(pilaoperadores)
                                   if (prioridaddp[ultimo]<prioridadfp[string[contador]]):
                                        pilaoperadores=insertafinal(pilaoperadores,string[contador])
                                        contador+=1
                                   else:
                                        valor2=ConvertirInt(obtiene_ultimo(pilanumeros))
                                        pilanumeros=eliminafinal(pilanumeros)
                                        valor1=ConvertirInt(obtiene_ultimo(pilanumeros))
                                        pilanumeros=eliminafinal(pilanumeros)
                                        res=operacion(valor1,obtiene_ultimo(pilaoperadores),valor2)
                                        pilanumeros=insertafinal(pilanumeros,res)
                                        pilaoperadores=eliminafinal(pilaoperadores)
                              else:
                                   pilaoperadores=insertafinal(pilaoperadores,string[contador])#deberia quitarse pero aqui no, sino donde estaba
                                   contador+=1
     while not(verificar_vacia(pilaoperadores)):
          valor2=ConvertirInt(obtiene_ultimo(pilanumeros))
          pilanumeros=eliminafinal(pilanumeros)
          valor1=ConvertirInt(obtiene_ultimo(pilanumeros))
          pilanumeros=eliminafinal(pilanumeros)
          res=operacion(valor1,obtiene_ultimo(pilaoperadores),valor2)
          pilanumeros=insertafinal(pilanumeros,res)
          pilaoperadores=eliminafinal(pilaoperadores)
          #pilaoperadores=eliminafinal(pilaoperadores)
##     print (pilanumeros)
     return pilanumeros
     
#Lista="[[tl,x],::,[t1, g],::,[[[hd, j]]]]"
#Lista="[[tl,x],::,[t1, g],::,[[tl, j]]]"
def opcons(listam):
     x=listam.count("::")
     contador=0
     while contador<x:
          listam.remove("::") #Se podria remover los parentesis (* no en string). 
          contador+=1
     resultado=[]

     
     for e in listam:
          if len(e)==2 and e[0]=="tl" and (isinstance (e[1],list) or verificar_list(e[1])):
               if isinstance (e[1],list):
                    resultado.append(tl(e[1]))
                    
               elif verificar_list(e[1]):
                    resultado.append(tl(obtener(e[1])))
                    
          elif len(e)==1 and e[0][0]=="tl" and (isinstance ((e[0][1]),list) or verificar_list(e[0][1])):
               if isinstance (e[0][1],list):
                    resultado.append(tl(e[0][1]))
                    
               elif verificar_list(e[0][1]):
                    resultado.append(tl(obtener(e[0][1])))
                    
          if len(e)==2 and e[0]=="hd" and (isinstance (e[1],list) or verificar_list(e[1])):
               if isinstance (e[1],list):
                    resultado.append(hd(e[1]))
                    
               elif verificar_list(e[1]):
                    resultado.append(hd(obtener(e[1])))
                    
          elif len(e)==1 and e[0][0]=="hd" and (isinstance ((e[0][1]),list) or verificar_list(e[0][1])):
               if isinstance (e[0][1],list):
                    resultado.append(hd(e[0][1]))
                    
               elif verificar_list(e[0][1]):
                    resultado.append(hd(obtener(e[0][1])))
                    
          elif len(e)==1 and e[0][0][0]=="hd" and (isinstance ((e[0][0][1]),list) or verificar_list(e[0][0][1])):
               if isinstance (e[0][0][1],list):
                    resultado.append([hd(e[0][0][1])])
                    
               elif verificar_list(e[0][0][1]):
                    resultado.append([hd(obtener(e[0][0][1]))])
                    
     print (resultado)
     return resultado

#Revisa si lo que recibe es una lista y esta tiene este formato [hd,L3]
def isCons(lista):
     if isinstance(lista,list) and len(lista)==2 and (lista[0]=="hd" or lista[0]=="tl") and (isinstance(lista[1],list) or verificar_list(lista[1])):
               return True
          
     else:
          return False

#Inserta final a la pila
def insertafinal(lista3,elemento):
     lista3=lista3+[elemento]
     return lista3
     
#Elimina final (pila)
def eliminafinal(lista1):
     lista1=lista1[0:(len(lista1)-1)]
     return lista1

def obtiene_ultimo(lista2):
     tamano=len(lista2)
     return (lista2[tamano-1])
     
#La lista que recibe debe ser asi [2,3,4] o [true,false,true,false] o [[2,1],[3,6],[5,6]] o [(5,4),(8,9),(3,6)]
#Los tipos de datos se tuvieron que convertir anteriormente  
def analizador_lista(Lllista):
     Lllista =str(Lllista)
     Llista = eval(Lllista)
     if Llista==[]:
          return ("list")
     elif isinstance (ConvertirInt(Llista[0]),int)or verificar_int(Llista[0]):
          return ("int list")
     elif Llista[0]=="false" or Llista[0]=="true" or verificar_bool(Llista[0]):
          return ("bool list")
     elif isinstance(Llista[0],list):
          return (analizador_lista(Llista[0])+" list")
     elif verificar_list(Llista[0]): # Si la lista esta encapsulada en una variable establecida
          return (obtener_tipo(Llista[0])+" list")
          
     elif isinstance(Llista[0],tuple):
          return (analizador_tupla(Llista[0])+" list")

     elif verificar_tuple(Llista[0]): # Si la lista esta encapsulada en una variable establecida
          return (obtener_tipo(Llista[0])+" list")
     else:
          print ("Error")
          
# Hacer un verificador que me permita si tengo val x, tal que x es una lista, y si esta x esta en una tupla, yo poder colocar el valor y reconocerlo.
def analizador_tupla(Ttupla):
     if len(Ttupla)==0:
          return ("()")
     respuesta="("
     if isinstance (ConvertirInt(Ttupla[0]),int)or verificar_int(Ttupla[0]):
          respuesta=respuesta+"int"     
     elif Ttupla[0]=="false" or Ttupla[0]=="true" or verificar_bool(Ttupla[0]):
          respuesta=respuesta+"bool"
     elif isinstance (Ttupla[0],list):
          respuesta=respuesta+analizador_lista(Ttupla[0])
     elif verificar_list(Ttupla[0]): # Si la lista esta encapsulada en una variable establecida
          respuesta=respuesta+(obtener_tipo(Ttupla[0]))
     elif isinstance (Ttupla[0],tuple):
          respuesta=respuesta+analizador_tupla(Ttupla[0])
     elif verificar_tuple(Ttupla[0]): # Si la tupla esta encapsulada en una variable establecida
          respuesta=respuesta+(obtener_tipo(Ttupla[0]))
          
     for e in Ttupla[1:]:
          if isinstance (ConvertnirInt(e),int):
               respuesta=respuesta+"*int"
          elif e=="false" or e=="true":
               respuesta=respuesta+"*bool"
          elif isinstance (e,list):
               respuesta=respuesta+"*"+analizador_lista(e)
          elif verificar_list(e): # Si la lista esta encapsulada en una variable establecida
               respuesta=respuesta+"*"+(obtener_tipo(e))
          elif isinstance (e,tuple):
               respuesta=respuesta+"*"+analizador_tupla(e)
          elif verificar_tuple(e): # Si la tupla esta encapsulada en una variable establecida
               respuesta=respuesta+"*"+(obtener_tipo(e))
     respuesta+=")"
     return respuesta

# Verificar si la variable es un int y esta esta almacenada en el ambiente
def verificar_int(valor):
     print("Verificarint: ",valor)
     if lista==[]:
          return False

     for e in lista:
          if ((e[0]==valor) and (e[2]=="int")):
               return True
          
     return False


# Verificar si la variable es un int y esta esta almacenada en el ambiente
def verificar_bool(valor):
     if lista==[]:
          return False
     for e in lista:
          if ((e[0]==valor) and (e[2]=="bool")):
               return True
          
     return False

#Verificar si la lista esta encapsulada o oculta, siendo asignada a una variable 
def verificar_list(valor):
     if lista==[]:
          return False
     for e in lista:
          if ((e[0]==valor) and (e[4]=="list")):
               return True
     return False

def verificar_tuple(valor):
     if lista==[]:
          return False
     for e in lista:
          if ((e[0]==valor) and (e[4]=="tuple")):
               return True
     return False


def obtener_tipo(valor):
     for e in lista:
          if (e[0]==valor) and (e[3]=="global"):
               return (e[2])



#Obtener el valor del dato almacenado en la lista siempre y cuando sean GLOBALES
def obtener(valor):
     print("Obtener valor de: ",valor)
     for e in lista:
          print("e in lista: ",e)
          if e[0]==valor and e[3]=="global":
               return (e[1])

#Si se identifica tl
def tl(lista):
     return (lista[1:])

#Si de identifica hd
def hd(lista):
     return (lista[0])


#le: Lista o elemento
def caractercons(le1,le2):
     if le1==[] or le1=="":
          return le2
     else:
          if (isNumber(le1) or verificar_int(le1)) and isinstance(le2,list):
               return [le1]+le2
          elif (isNumber(le2) or verificar_int(le2)) and isinstance(le1,list):
               return le1+[le2]
          elif isinstance(le1,list) and isinstance(le2,list):
               return le1+le2
            

#def esLista(lista):
	#lista es un string que puede o no ser una lista
	#if lista[0] == '['
#def esTupla(tupla):

#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------			MAIN				-----------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

#main de la aplicacion
if __name__ == '__main__':
	#app.debug = True
	app.run(host='192.168.0.7') #CAMBIAR ESTE IP POR EL ACTUAL
