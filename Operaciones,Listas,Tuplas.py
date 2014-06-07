lista=[["x",3,"int","global"],["z",5,"int","global"],["y","false","bool","global"]]

#re multiples delimitadores
import re
prioridaddp={"*":2,"/":2,"%":2,"+":1,"-":1,"(":0}
prioridadfp={"*":2,"/":2,"%":2,"+":1,"-":1,"(":5}


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
          if (verificar_vacia(pilaoperadores) and isNumber(string[contador])):
               pilanumeros=insertafinal(pilanumeros,string[contador])
               contador+=1
          else:
               if verificar_vacia(pilaoperadores):
                    pilaoperadores=insertafinal(pilaoperadores,string[contador])
                    contador+=1
               elif isNumber(string[contador]):
                    pilanumeros=insertafinal(pilanumeros,string[contador])
                    contador+=1
               else:
                    print ("pila operadores")
                    print pilaoperadores
                    print ("pila numeros")
                    print pilanumeros
                    if ((string[contador])==")"):
                         print ("pila operadores")
                         print pilaoperadores
                         print ("pila numeros")
                         print pilanumeros



                         
                         
                         print (verificar_vacia(pilaoperadores))
                         while (not verificar_vacia(pilaoperadores)):
                              if (obtiene_ultimo(pilaoperadores)=="("):
                                   pilaoperadores=eliminafinal(pilaoperadores)
                                   contador+=1
                                   break
                              else:
                                   print ("pila operadores")
                                   print pilaoperadores
                                   print ("pila numeros")
                                   print pilanumeros
                                   
                                   valor2=ConvertirInt(obtiene_ultimo(pilanumeros))
                                   pilanumeros=eliminafinal(pilanumeros)
                                   valor1=ConvertirInt(obtiene_ultimo(pilanumeros))
                                   pilanumeros=eliminafinal(pilanumeros)
                                   res=operacion(valor1,obtiene_ultimo(pilaoperadores),valor2)
                                   print(res)
                                   pilanumeros=insertafinal(pilanumeros,res)
                                   pilaoperadores=eliminafinal(pilaoperadores)
                    else:
                         ultimo=obtiene_ultimo(pilaoperadores)
                         print ("pila operadores")
                         print pilaoperadores
                         print ("pila numeros")
                         print pilanumeros
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

                              pilaoperadores=insertafinal(pilaoperadores,string[contador])
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
     print ("pila operadores")
     print pilaoperadores
     print ("pila numeros")
     print pilanumeros
     
           
          
                              
                              
                         
                              
                              
                              
                              
                    
                    
                    
     
     



#Dividir string para meterlo en una lista cada elemento
#def separar(string):
##     resultado=re.split("(()*|+(*)|(-)*",string)
####     try:
####          while True:
####               resultado.
##     return resultado
     


#Inserta final a la pila
def insertafinal(lista,elemento):
     lista=lista+[elemento]
     return lista
     
#Elimina final (pila)
def eliminafinal(lista):
     lista=lista[0:(len(lista)-1)]
     return lista

def obtiene_ultimo(lista):
     tamano=len(lista)
     return (lista[tamano-1])
     



#La lista que recibe debe ser asi [2,3,4] o [true,false,true,false] o [[2,1],[3,6],[5,6]] o [(5,4),(8,9),(3,6)]
#Los tipos de datos se tuvieron que convertir anteriormente  
def analizador_lista(Llista):
     if Llista==[]:
          return ("list")
     elif isinstance (Llista[0],int):
          return ("int list")
     elif Llista[0]=="false" or Llista[0]=="true":
          return ("bool list")
     elif isinstance(Llista[0],list):
          return (analizador_lista(Llista[0])+" list")
     elif isinstance(Llista[0],tuple):
          return (analizador_tupla(Llista[0])+" list")
     else:
          print ("Errorrsh")
          

def analizador_tupla(Ttupla):
     if len(Ttupla)==0:
          return ("()")
     respuesta="("
     if isinstance (Ttupla[0],int):
          respuesta=respuesta+"int"     
     elif Ttupla[0]=="false" or Ttupla[0]=="true":
          respuesta=respuesta+"bool"
     elif isinstance (Ttupla[0],list):
          respuesta=respuesta+analizador_lista(Ttupla[0])
     elif isinstance (Ttupla[0],tuple):
          respuesta=respuesta+analizador_tupla(Ttupla[0])
     for e in Ttupla[1:]:
          if isinstance (e,int):
               respuesta=respuesta+"*int"
          elif e=="false" or e=="true":
               respuesta=respuesta+"*bool"
          elif isinstance (e,list):
               respuesta=respuesta+"*"+analizador_lista(e)
          elif isinstance (e,tuple):
               respuesta=respuesta+"*"+analizador_tupla(e)
     respuesta+=")"
     return respuesta

# Verificar si la variable es un int
def verificar_int(valor):
     if lista==[]:
          return False
     for e in lista:
          if ((e[0]==valor) and (e[2]=="int")):
               return True
     return False

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
