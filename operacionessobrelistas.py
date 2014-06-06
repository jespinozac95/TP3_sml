lista=[["x",3,"int","global","int"],["z",5,"int","global","int"],["y","false","bool","global","bool"],["j",[5,4,3],"int list","global","list"],["k",("false",5,3),"(bool*int*int)","global","tuple"]]

#Revisar las listas y tuplas


#re multiples delimitadores
import re
prioridaddp={"*":2,"/":2,"%":2,"+":1,"-":1,"(":0}
prioridadfp={"*":2,"/":2,"%":2,"+":1,"-":1,"(":5}

#Prioridades para operaciones con listas
prioridaddp2={"(":0,"::":2}
prioridadfp2={"(":5,"::":2}


#Inserta datos al inicio de la lista.  
def agregardatos(lista,variable,valor,tipo,scope):
     temp_list=[[variable,valor,tipo,scope]]
     lista=temp_list+lista
     return lista

     
## resuelve operaciones elementales
def operacion(valor1,operando,valor2):
     if (isinstance(valor1,int) and isinstance(valor2,int)) : 
          if operando=="+":
               return (valor1+valor2)
          elif operando=="-":
               return (valor1-valor2)
          elif operando=="*":
               return (valor1*valor2)
          elif operando=="div": #operando=="/" 
               return (valor1/valor2)
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
               return (valor1/(obtener(valor2)))
          elif operando=="mod": #operando=="%" 
               return (valor1%(obtener(valor2)))
          else:
               print ("Operacion no permitida")
     elif (verificar_int(valor1) and isinstance(valor2,int)):
          if operando=="+":
               return ((obtener(valor1))+valor2)
          elif operando=="-":
               return ((obtener(valor1))-valor2)
          elif operando=="*":
               return ((obtener(valor1))*valor2)
          elif operando=="div": #operando=="/"
               return ((obtener(valor1))/valor2)
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
               return ((obtener(valor1))/(obtener(valor2)))
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
     print pilanumeros
     
           
          
                              
                              

#Dividir string para meterlo en una lista cada elemento
#def separar(string):
##     resultado=re.split("(()*|+(*)|(-)*",string)
####     try:
####          while True:
####               resultado.
##     return resultado



#Operar sobre listas [[hd,L1],::,(,[tl,L2],::,[hd,L3],)]
def opcons(string):
     contador=0
     pilaoperadores2=[] #parentesis, cons 
     pilalistas=[] #[hd,l1] 
     while contador<len(string):
          if (verificar_vacia(pilaoperadores2) and isCons(string[contador])):
               pilalistas=insertafinal(pilalistas,string[contador])
               contador+=1
          else:
               if verificar_vacia(pilaoperadores2):
                    pilaoperadores2=insertafinal(pilaoperadores2,string[contador])
                    contador+=1
               elif (isCons(string[contador])):
                    pilalistas=insertafinal(pilalistas,string[contador])
                    contador+=1
               else:
                    if ((string[contador])==")"):
                         while (not verificar_vacia(pilaoperadores2)):
                              if (obtiene_ultimo(pilaoperadores2)=="("):
                                   pilaoperadores2=eliminafinal(pilaoperadores2)
                                   contador+=1
                                   break
                              else:
                                   valor2=obtiene_ultimo(pilalistas)
                                   if valor2[0]=="hd":
                                        valor2=hd(valor2[1])
                                   else:
                                        valor2=tl(valor2[1])
                                   pilalistas=eliminafinal(pilalistas)
                                   valor1=obtiene_ultimo(pilalistas)
                                   if valor1[0]=="hd":
                                        valor1=hd(valor1[1])
                                   else:
                                        valor1=tl(valor1[1])
                                   pilalistas=eliminafinal(pilalistas)
                                   res=caractercons(valor1,valor2)
                                   print("resultado:")
                                   print(res)
                                   pilalistas=insertafinal(pilalistas,res)
                                   pilaoperadores2=eliminafinal(pilaoperadores2)
                    else:
                         ultimo=obtiene_ultimo(pilaoperadores2)
                         if (prioridaddp2[ultimo]<prioridadfp2[string[contador]]):
                              pilaoperadores2=insertafinal(pilaoperadores2,string[contador])
                              contador+=1
                         else:
                              valor2=obtiene_ultimo(pilalistas)
                              if valor2[0]=="hd":
                                   valor2=hd(valor2[1])
                              else:
                                   valor2=tl(valor2[1])
                              pilalistas=eliminafinal(pilalistas)
                              valor1=obtiene_ultimo(pilalistas)
                              if valor1[0]=="hd":
                                   valor1=hd(valor1[1])
                              else:
                                   valor1=tl(valor1[1])
                              pilalistas=eliminafinal(pilalistas)
                              res=caractercons(valor1,valor2)
                              print("resultado:")
                              print(res)
                              pilalistas=insertafinal(pilalistas,res)
                              pilaoperadores2=eliminafinal(pilaoperadores2)
                              

                              if (not verificar_vacia(pilaoperadores2)):
                                   ultimo=obtiene_ultimo(pilaoperadores2)
                                   if (prioridaddp[ultimo]<prioridadfp[string[contador]]):
                                        pilaoperadores2=insertafinal(pilaoperadores2,string[contador])
                                        contador+=1
                                   else:
                                        valor2=obtiene_ultimo(pilalistas)
                                        if valor2[0]=="hd":
                                             valor2=hd(valor2[1])
                                        else:
                                             valor2=tl(valor2[1])
                                        pilalistas=eliminafinal(pilalistas)
                                        valor1=obtiene_ultimo(pilalistas)
                                        if valor1[0]=="hd":
                                             valor1=hd(valor1[1])
                                        else:
                                             valor1=tl(valor1[1])
                                        pilalistas=eliminafinal(pilalistas)
                                        res=caractercons(valor1,valor2)
                                        print("resultado:")
                                        print(res)
                                        pilalistas=insertafinal(pilalistas,res)
                                        pilaoperadores2=eliminafinal(pilaoperadores2)

                              else:
                                   pilaoperadores2=insertafinal(pilaoperadores2,string[contador])#deberia quitarse pero aqui no, sino donde estaba
                                   contador+=1
     while not(verificar_vacia(pilaoperadores2)):
          valor2=obtiene_ultimo(pilalistas)
          if valor2[0]=="hd":
               valor2=hd(valor2[1])
          else:
               valor2=tl(valor2[1])
          pilalistas=eliminafinal(pilalistas)
          valor1=obtiene_ultimo(pilalistas)
          if valor1[0]=="hd":
               valor1=hd(valor1[1])
          else:
               valor1=tl(valor1[1])
          pilalistas=eliminafinal(pilalistas)
          res=caractercons(valor1,valor2)
          print("resultado:")
          print(res)
          pilalistas=insertafinal(pilalistas,res)
          pilaoperadores2=eliminafinal(pilaoperadores2)
          
     print pilalistas






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
def analizador_lista(Llista):
     if Llista==[]:
          return ("list")
     elif isinstance (Llista[0],int)or verificar_int(Llista[0]):
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
          print ("Errorrsh")
          




# Hacer un verificador que me permita si tengo val x, tal que x es una lista, y si esta x esta en una tupla, yo poder colocar el valor y reconocerlo.
def analizador_tupla(Ttupla):
     if len(Ttupla)==0:
          return ("()")
     respuesta="("
     if isinstance (Ttupla[0],int)or verificar_int(Ttupla[0]):
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
          if isinstance (e,int):
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
     for e in lista:
          if (e[0]==valor) and (e[3]=="global"):
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
               
               
          






