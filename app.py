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

##Imports del framework para la aplicacion web: Flask
from flask import Flask, request, redirect, url_for, abort, session, render_template, flash
from werkzeug.utils import secure_filename
import os

##Configuracion de guardar archivos
UPLOAD_FOLDER = '/home/josue/TP3_sml'
ALLOWED_EXTENSIONS = set(['sml'])

##Nombre de la aplicacion: Bumbur
app = Flask("SML")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Para usar flash
#app.secret_key = 'josue'

#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------			FRONTEND	   ------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

##URL y funcion para home
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
			global dic
			lista = []
			lista2 = []
			dic = {}
			return render_template('felicidades.html',dinamico=dinamico,estatico=estatico)
		else:
			return redirect(url_for('error'))
	return render_template('felicidades.html')
##
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

##Funcion para borrar un archivo en uploads despues de ser evaluado
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
    corregida = corregirLets(agrupada)
    print("Corregida de Lets: ",corregida)
    transformada = transformar(corregida)
    print("Transformada: ",transformada)
    almacenar(transformada)
##    print("Lista Final: ",lista)
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

def corregirLets(lista):
##    print("Lista entrante a corregirLets: ",lista)
    lista2 = []
    for val in lista:
##        print("val: ",val)
        let = []
        valEnLet = []
        if val[3] == 'let':
            let += ['let']
            val.pop(3)
            while not val[3] == 'in':
                valEnLet += [val[3]]
                val.pop(3)
            let += [valEnLet]
            let += ['in']
            val.pop(3)
            valEnLet = []
            indice = 3
            largo = len(val)
            while indice != largo:
                valEnLet += [val[3]]
                val.pop(3)
                indice += 1
            let += [valEnLet]
            val.insert(3,let)
        lista2 += [val]
    return lista2
        
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

################################################################################################################################################
                            
        elif ide==2: #let
            vector=matriz[0]
            if vector!=[] and (vector[0]=='let' or vector[0]=='(let'):
                valActual += ['let']
                vector=vector[1:]
                matriz[0]=matriz[0][1:]

            while vector!=[] and vector[0] not in {'end','(end'}:
                valActual += [vector[0]]                
                vector=vector[1:]
                matriz[0]=matriz[0][1:]

            if vector!=[] and vector[0] in {'end','(end'}:
                vector=vector[1:]
                matriz[0]=matriz[0][1:]
                
            #termino el let bien, sml bonito
            if vector == [] and len(matriz)>=2 and len(matriz[1])>= 1 and matriz[1][0] in {'val','(val','let','(let','if','(if'}:
                agrupada+=[valActual]
                if matriz[1][0]=='val' or matriz[1][0]=='(val':
                    matriz = matriz[1:]
                    agrupada2+=agrupada
                    return agrupar(matriz,1,[],agrupada2)
                elif matriz[1][0]=='let' or matriz[1][0]=='(let':
                    matriz = matriz[1:]
                    agrupada2+=agrupada
                    return agrupar(matriz,2,[],agrupada2)
                elif matriz[1][0]=='if' or matriz[1][0]=='(if':
                    matriz = matriz[1:]
                    agrupada2+=agrupada
                    return agrupar(matriz,3,[],agrupada2)

            #No ha terminado el let, sigue en la siguiente linea (lista)     
            elif vector == [] and len(matriz)>=2 and len(matriz[1])>= 1:
                matriz=matriz[1:]
                return agrupar(matriz,2,valActual,agrupada2)

            #ya termino el let, sigue en la misma linea la siguiente expresion    
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
            
##            vector=matriz[0]
##            if vector!=[] and (vector[0]=='let' or vector[0]=='(let'):
##                valActual+=[[]]
##                valActual[-1]+= ['let']
##                valActual[-1]+=[[]]
####                print(valActual)
##                vector=vector[1:]
##                matriz[0]=matriz[0][1:]
##                if vector[0]=='val' or vector[0]=='(val':
##                    valActual[-1][-1]+=['val']
##                    vector=vector[1:]
##                    matriz[0]=matriz[0][1:]
####                    print("If que entra si el vector[0] es val",vector[0])
##            while vector!=[] and vector[0] not in {'val','(val','let','(let','if','(if','in','end','end)'}: ##Mete todo lo que tenga el let hasta antes del in
##                valActual[-1][-1]+=[vector[0]]
##                vector=vector[1:]
##                matriz[0]=matriz[0][1:]
##                    
##
##            if vector != [] and vector[0] in {'val','(val','let','(let','if','(if','end','end)'}:
##
##                agrupada+=[valActual]
##                if vector[0]=='val' or vector[0]=='(val':
##                    agrupada2[-1]+=agrupada
##                    return agrupar(matriz,1,[],agrupada2)
##                elif vector[0]=='let' or vector[0]=='(let':
##                    agrupada2[-1]+=agrupada
##                    return agrupar(matriz,2,[],agrupada2)
##                elif vector[0]=='if' or vector[0]=='(if':
##                    agrupada2[-1]+=agrupada
##                    return agrupar(matriz,3,[],agrupada2)
##                    
##                    
##                    
##                
##            if vector!=[] and vector[0]=='in':
####                print('Si vector es distinto de vacio y vector[0] es in',vector[0])
##                valActual+=['in']
##                vector=vector[1:]
##                matriz[0]=matriz[0][1:]
##                while vector!=[] and vector[0] not in {'val','(val','let','(let','if','(if'}:
####                    print(vector[0])
##                    valActual+=[vector[0]]
##                    vector=vector[1:]                        
##                    matriz[0]=matriz[0][1:]
##                    
##            if vector!=[] and (vector[0]=='end' or vector[0]=='end)'):
##                valActual+=['end']
##                vector=vector[1:]
##                matriz[0]=matriz[0][1:]
##                agrupada+=valActual
##                return agrupar(matriz,2,valActual,agrupada2)
##
##                    
##            elif vector == [] and len(matriz)>=2 and len(matriz[1])>= 1: ## and matriz[1][0]=='in':                    
##                matriz=matriz[1:]
####                valActual+=[vector[0]]
##                return agrupar(matriz,2,valActual+[],agrupada2)
##
##            elif vector == [] and len(matriz)>=2 and len(matriz[1])>= 1 and matriz[1][0] in {'val','(val','let','(let','if','(if'}:  
##                matriz=matriz[1:]
##                valActual+=[[]]
####                valActual+=[vector[0]]
####                    print('in',vector[0])
##                return agrupar(matriz,2,valActual,agrupada2)
##
##
##            elif vector == [] and len(matriz)>=2 and len(matriz[1])>= 1 and matriz[1][0] not in {'val','(val','let','(let','if','(if'}:
##                matriz=matriz[1:]
##
####                valActual+=[vector[0]]
####                    print('in',vector[0])
##                return agrupar(matriz,1,valActual,agrupada2)
##            
##
##
##            elif len(matriz)==1 and matriz[0]==[]:
##                matriz=matriz[1:]
##                agrupada2+=[valActual]
##                return agrupada2
    
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

##    print(string)
    
    temp=re.split(',|(=)*(>)*(<)*(`)*(div)*(EEE)*(QQQ)*([)*(])*(mod)*(hd)*(tl)*(::)*(!)*(@)*(%)*(&)*',string)

##    print(temp)
    
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

    l = []
    act = False
    indice = 1
    estar = 0
    for i in final[1:-1]:
        if act and i[-1] != ']':
            l+= [i]
            final.pop(indice)
        elif i[0] == '[':
            l += [i[1:]]
            act = True
            estar = indice
            final.pop(indice)
        elif i[-1] == ']':
            l += [i[:-1]]
            act = False
            final.pop(indice-1)
            final.insert(estar,l)
            l= []
        indice += 1
    
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
            if l1 == []:
                return l2
            elif l2 == []:
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
                lista = lista[1:]
                if lista != []:
                    for e in lista:
                        if isinstance(e,list):
                            for i in e:
                                valorComplejo += i
                            resultado += [corregirLista(valorComplejo)]
                            valorComplejo = ""
                        else:
                            resultado += [e]
                return resultado

     
global lista
##lista=[["x",3,"int","global","int"],["z",5,"int","global","int"],["y","false","bool","global","bool"],["e",[5,4,3],"int list","global","list"],["f",[8,9,10],"int list","global","list"],["g",[3,4,9],"int list","global","list"],["k",("false",5,3),"(bool*int*int)","global","tuple"]]
lista = []
globales = {}

#Revisar las listas y tuplas


#re multiples delimitadores
import re
prioridaddp={"*":2,"div":2,"mod":2,"+":1,"-":1,"(":0}
prioridadfp={"*":2,"div":2,"mod":2,"+":1,"-":1,"(":5}

##Recibe una lista con valores en strings y devuelve la misma lista con los valores tales y como son con eval
def evali(l,dicc):
    print("l: ",l)
    y = []
    if len(l) == 1:
        return eval(l[0],dicc)
    for each in l:
        if isinstance(each,str) and each in {"true","false"}:
            y+=[eval(each.capitalize())]
        elif isinstance(each,list) and each[0] == '(':
            p = each[1:]
            p = p[:-1]
            y+=[evali(each,dicc)]
        elif isinstance(each,list):
            y+=[evali(each,dicc)]
        else:
            y+=[(eval(each,dicc))]
        print("y: ",y)
    return y

##Recibe la lista que contiene toda la expresion If y devuelve el resultado de todo el if (lo que este en then o else, segun corresponda)
def resolverIf(ifs):
    ##puede ser: que vaya al then o al else
    ## Primero: evaluar la expresion del if (boolean)
    ##print("if: ",ifs)
    y = ""
    for e in ifs:
        if isinstance(e,list):
            y+="".join(e)
            break
            
    y.replace('andalso','and',y.count('andalso'))
    y.replace('orelse','or',y.count('orelse'))

    dic = {}
    for each in lista:
        if not each[0] in dic:
            dic[each[0]]=each[1]

    ##resolver booleano
    resultadoBool = eval(y,dic)

    if resultadoBool: #then -> ifs[3]
        aResolver = ifs[3]
	print("ifs[3]: ",ifs[3])
        #Caso es un boolean
        if "<" in aResolver or ">" in aResolver or "orelse" in aResolver or "andalso" in aResolver:
            q = ""
            for e in aResolver:
                if isinstance(e,list):
                        q+="".join(e)
                        break
            q.replace('andalso','and',q.count('andalso'))
            q.replace('orelse','or',q.count('orelse'))
            return eval(q,dic)
            
        #Caso es una tupla, no resulve operaciones de #2, #1 todavia
        elif '(' in aResolver:
            aResolver = aResolver[1:]
            aResolver = aResolver[:-1]
            return tuple(evali(aResolver,dic))

        #Caso es una lista
        elif aResolver[0][0] == '[':
	    aResolver[0] = aResolver[0][1:]
            aResolver[-1] = aResolver[-1][:1]
            return evali(aResolver,dic)
        
        #Caso es un int
        else:
	    print("Soy un int")
            string = ""
            for ea in aResolver:
                string += ea
            return eval(string,dic)
        
    else: #else -> ifs[5]
        aResolver = ifs[5]
        #Caso es un boolean
        if "<" in aResolver or ">" in aResolver or "orelse" in aResolver or "andalso" in aResolver:
            q = ""
            for e in aResolver:
                if isinstance(e,list):
                        q+="".join(e)
                        break
            q.replace('andalso','and',q.count('andalso'))
            q.replace('orelse','or',q.count('orelse'))
            return eval(q,dic)
            
        #Caso es una tupla, no resulve operaciones de #2, #1 todavia
        elif '(' in aResolver:
            aResolver = aResolver[1:]
            aResolver = aResolver[:-1]
            return tuple(evali(aResolver,dic))

        #Caso es una lista
        elif aResolver[0][0] == '[':
	    aResolver[0] = aResolver[0][1:]
            aResolver[-1] = aResolver[-1][:1]
            return evali(aResolver,dic)
        
        #Caso es un int
        else:
            string = ""
            for ea in aResolver:
                string += ea
            return eval(string,dic)

##Recibe la lista que contiene toda la expresion Let y devuelve el resultado de todo el let (lo que este en el in)
##['let', ['val', 'p', '=', ['4']], 'in', ['4', '*', 'p', '+', '50']] a 66
def resolverLet(let):
    dic = {}
    toResolve = []
    siguiente = False
    for each in let:
        if siguiente:
            toResolve = each
        elif isinstance(each,list) and each[0] == 'val':
            valResuelto = resolverVal(each)
            dic[valResuelto[0]]=valResuelto[1]
        elif isinstance(each,str) and each == 'in':
            siguiente = True
    x = "".join(toResolve)
    esIterable = False
    for ea in x:
        if ea == '(':
            esIterable = True
            break
        elif ea[0] == '[':
            esIterable = True
	    toResolve[0] = toResolve[0][1:]
            toResolve[-1] = toResolve[-1][:1]
            break
    if esIterable:
        return evali(toResolve,dic)
    else:
        return eval(x,dic)

##Funcion que resuelve el val dentro de un let    
def resolverVal(l):
    for p in range(len(l)):
        if isinstance(l[p],list) and l[p][0] not in {'val','if','let'}:
            x = ""
            for u in l[p]:
                if isinstance(u,list):
                        y = "".join(u)
                        x += "["+y+"]"
                else:
                        x += u
            if x[0] == '[': #x es lista
                    subLista = l[p]
                    subLista[0] = subLista[0][1:]
                    subLista[-1] = subLista[-1][:1]
                    print("subLista Lista = ",subLista)
                    l[p] = evali(subLista,globales)
                    print("After Evali = ",l[p])
            elif x[0] == '(':
                    subLista = l[p]
                    subLista = subLista[1:]
                    subLista = subLista[:-1]
                    print("subLista Tupla = ",subLista)
                    l[p] = tuple(evali(subLista,globales))
                    print("After Evali = ",l[p])
            else:
                    if x  == 'true':
                        l[p] = True
                    elif x == 'false':
                        l[p] = False
                    else:
                        l[p] = op(l[p])[0]
                        l[p] = int(l[p])
        elif isinstance(l[p],list) and l[p][0] in {'if','let'}: #es un if o un let
            if l[p][0] == 'if':
                l[p] = resolverIf(l[p])
            else:
                l[p] = resolverLet(l[p])
    dic = []
    dic.append(l[1])
    print("dic[0]: ",dic[0])
    dic.append(l[3])
    print("dic[1]: ",dic[1])
    return dic

##Funcion que resuelve las variables y las manda a almacenarse en la lista final
def almacenar(matriz):
        for e in range(len(matriz)):
                tipo = ""
                for p in range(len(matriz[e])):
                    if isinstance(matriz[e][p],list) and matriz[e][p][0] not in {'val','if','let'}:
                            largo = len(matriz[e][p])
                            x = ""
                            for u in matriz[e][p]:
                                if isinstance(u,list):
                                        y = "".join(u)
                                        x += "["+y+"]"
                                else:
                                        x += u
                            if x[0] == '[': #x es lista
                                    subLista = matriz[e][p]
                                    subLista[0] = subLista[0][1:]
                                    subLista[-1] = subLista[-1][:1]
                                    print("subLista Lista = ",subLista)
                                    matriz[e][p] = evali(subLista,globales)
                                    print("After Evali = ",matriz[e][p])
                                    tipo = analizador_lista(matriz[e][p])
                                    print("After tipo = ",tipo)
                            elif x[0] == '(':
                                    subLista = matriz[e][p]
                                    subLista = subLista[1:]
                                    subLista = subLista[:-1]
                                    print("subLista Tupla = ",subLista)
                                    matriz[e][p] = tuple(evali(subLista,globales))
                                    print("After Evali = ",matriz[e][p])
				    print("list(matriz[e][p]) = ",list(matriz[e][p]))
                                    tipo = analizador_tupla(list(matriz[e][p]))
                                    print("After tipo = ",tipo)
                            else:
                                    if x  == 'true':
                                        tipo = "Boolean"
                                        matriz[e][p] = True
                                    elif x == 'false':
                                        tipo = "Boolean"
                                        matriz[e][p] = False
                                    else:
                                        matriz[e][p] = op(matriz[e][p])[0]
                                        matriz[e][p] = int(matriz[e][p])
                                        tipo = 'int'
                    elif isinstance(matriz[e][p],list) and matriz[e][p][0] in {'val','if','let'}: #es un if o un let
                        if matriz[e][p][0] == 'if':
                            matriz[e][p] = resolverIf(matriz[e][p])
			    print("type(matriz[e][p]): ",type(matriz[e][p]))
                            tipo = str(type(matriz[e][p]))[7:-2]
			    if tipo == 'list':
				    tipo = analizador_lista(matriz[e][p])
			    elif tipo == 'tuple':
				    tipo = analizador_tupla(matriz[e][p])
			    elif tipo == 'bool':
				    tipo = 'Boolean'
                        else:
                            matriz[e][p] = resolverLet(matriz[e][p])
			    print("type(matriz[e][p]): ",type(matriz[e][p]))
                            tipo = str(type(matriz[e][p]))[7:-2]
			    if tipo == 'list':
				    tipo = analizador_lista(matriz[e][p])
			    elif tipo == 'tuple':
				    tipo = analizador_tupla(list(matriz[e][p]))
			    elif tipo == 'bool':
				    tipo = 'Boolean'
			    
                agregardatos(matriz[e][1],matriz[e][3],tipo,'global',tipo)
                global globales
                globales[matriz[e][1]] = matriz[e][3]

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
          return ("a' list")
     elif isinstance(Llista[0],int) or isinstance (ConvertirInt(Llista[0]),int)or verificar_int(Llista[0]):
          return ("int list")
     elif Llista[0]=="false" or Llista[0]=="true" or Llista[0]=="False" or Llista[0]=="True" or Llista[0]==False or Llista[0]==True or verificar_bool(Llista[0]):
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
##     print("Ttupla: ",Ttupla)
     if len(Ttupla)==0:
          return ("()")
     respuesta="("
     print("Ttupla[0]= ",Ttupla[0])
     if (isinstance(Ttupla[0],int) or isinstance(ConvertirInt(Ttupla[0]),int) or verificar_int(Ttupla[0])) and not (Ttupla[0]==False or Ttupla[0]==True):
          respuesta=respuesta+"int"     
     elif Ttupla[0]=="false" or Ttupla[0]=="true" or Ttupla[0]=="False" or Ttupla[0]=="True" or Ttupla[0]==False or Ttupla[0]==True or verificar_bool(Ttupla[0]):
          respuesta=respuesta+"bool"
     elif isinstance (Ttupla[0],list):
          respuesta=respuesta+analizador_lista(Ttupla[0])
     elif verificar_list(Ttupla[0]): # Si la lista esta encapsulada en una variable establecida
          respuesta=respuesta+(obtener_tipo(Ttupla[0]))
     elif isinstance (Ttupla[0],tuple):
          respuesta=respuesta+analizador_tupla(Ttupla[0])
     elif verificar_tuple(Ttupla[0]): # Si la tupla esta encapsulada en una variable establecida
          respuesta=respuesta+(obtener_tipo(Ttupla[0]))
     print("respuesta = ",respuesta)
##
##     print("Ttupla[1:]: ",Ttupla[1:])
     for e in Ttupla[1:]:
	  print("e= ",e)
          if (isinstance(e,int) or isinstance (ConvertirInt(e),int) or verificar_int(e)) and not (e==False or e==True):
               respuesta=respuesta+"*int"
          elif e==False or e==True or e=="false" or e=="true" or e=="False" or e=="True" or verificar_bool(e):
               respuesta=respuesta+"*bool"
          elif isinstance (e,list):
               respuesta=respuesta+"*"+analizador_lista(e)
          elif verificar_list(e): # Si la lista esta encapsulada en una variable establecida
               respuesta=respuesta+"*"+(obtener_tipo(e))
          elif isinstance (e,tuple):
               respuesta=respuesta+"*"+analizador_tupla(e)
          elif verificar_tuple(e): # Si la tupla esta encapsulada en una variable establecida
               respuesta=respuesta+"*"+(obtener_tipo(e))
	  print("respuesta = ",respuesta)
     respuesta+=")"
     return respuesta

# Verificar si la variable es un int y esta esta almacenada en el ambiente
def verificar_int(valor):
##     print("Verificarint: ",valor)
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
##     print("Obtener valor de: ",valor)
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


#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------			MAIN				-----------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
##
##main de la aplicacion
if __name__ == '__main__':
	#app.debug = True
	app.run(host='192.168.0.8') #CAMBIAR ESTE IP POR EL ACTUAL
