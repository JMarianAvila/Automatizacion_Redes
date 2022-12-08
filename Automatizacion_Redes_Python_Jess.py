from netmiko import ConnectHandler #librería para establecer la conexión con el dispositivo a ingresar(sw)
import re #librería para las expresiones regulares
import json #librería para crearalmacenar los datos en formato json
import os #nos permite ingresar a funciones dpendientes del sistema operativo
os.system('cls')


'''Se solicitan las credenciales para poder ingresar por medio de SSH al dispositivo 
# en donde empezaremos la busqueda según lo que se seleccione en el menú'''

host = input("Ingresa el IP del dispositivo a conectar: ")
#usuario = input("Ingresa el usuario:")
usuario= "cisco" # /Aquí ponemos como resultado predeterminado cisco, debido a 
                 # /que así es como se encuentra el nombre del usuario en todos los dispositivos que se buscarán

#contraseña = input("ingresa la contraseña:")
contraseña="cisco"
contra_e = "cisco"

#CONECION CON EL SWITCH---------------------------|
'''Se realizó un diccionario en el cual se almacenan los datos de las credenciales antes ingresados '''
Dispositivo = {
    "host":host,
    "username":usuario,
    "password":contraseña,
    "device_type":"cisco_ios",
    "secret": contra_e,}

try:
    ''' Aquí es en donde realizamos la conexión con el dispositvo con el ConnectHandler
     y se tiene que poner doble** ya que es la forma predeterminada para realizar la conexión,
      al igual que esta conexión que tenemosya establecida la almacenamos en una variable que luego se usará '''
    conexion = ConnectHandler(**Dispositivo)
    conexion.enable()

except:
    print("LAS CREDENCIALES NO SON CORRECTAS")#en caso de que las credenciales no sean correctas pasa al except y mostrará el aviso
#Estos print muestran la presentación del programa
print("--------------------------------------------|")
print("        Automatización de redes             |")
print("  Alumna: Jessica Marian Avila Flores       |")
print("  Maestro: Eliud Bueno Moreno               |")
print("  Ingeniería en Redes y Telecomunicaciones  |")
print("                   4A                       |")
print("--------------------------------------------|")

print(">>>>>>>>     Hola, se bienvenido a mi programa   <<<<<<<<<")

iniciando = True #Se creea la variable iniciando que nos servirá para iniciar el ciclo while, 
                 #donde si es True lo iniciará y si es false no lo inicia o lo termina

while iniciando:#Iniciamos el ciclo
    print()
    print()#Aquí se muestra el menú 
    print("----------------------------------------------------|")
    print("                   Menú                             |")
    print("----------------------------------------------------|")
    print(" Ingresa el número del menú que quieres seleccionar |")
    print("----------------------------------------------------|")
    print("      1.Mostrar la tabla de enrutamiento            |")
    print("      2.Mostrar los vecinos                         |")
    print("      3.Buscar MAC dentro de los dispositivos       |")
    print("      4.Salir                                       |")
    print("----------------------------------------------------|")

    opcion = ""  #Aquí se crea una variable vacia que se usará 
                 #para almacenar el resultado  de la opción que seleccionen en el menú anterior
   
    
    while opcion not in ("1","2","3","4"):
        try:
            opcion = input("->")#se guarda la opción seleccionada del menú


            if opcion == "1":# si se seleccionó la opción 1 se enviará el comando 
                             #para mostrar la tabla de MAC en el dispositivo al que se ha ingresado, se guarda en una variable, 
                             # con la cual se mostrará el resultado de la busqueda con un print
                    SHtabla_mac  =  conexion.send_command('sh mac address-table')
                    print(SHtabla_mac)


            elif opcion == "2":#si se selecciona la opción 2 se enviará el comando 
                               #para mostrar los vecinos con CDP en el dispositivo al que se ha ingresado, 
                               #se guarda enuna variable con la cual se mostrará en un print
                    SHCDP  =  conexion.send_command('sh cdp neighbors')
                    print(SHCDP)


            elif opcion == "3":#si se selecciona la opción 3 se realizará la busqueda de una Mac que se desee encontrar

                    ciclo = 1#se creea una variable igual a 1 para que inicie el ciclo de la busqueda
                    Macbus = input("Ingrsa la MAC que deseas buscar: ")#se creea una variable en la que se almacenará 
                                                                       #el valor de la mac que se desea buscar
                    #mac2=Macbus
                    '''con el replace lo que hace es remplazar los guiones o los puntos
                       que se encuentren al ingresar la mac por espacios vacios'''
                    Macbus = Macbus.replace("-","")
                    Macbus = Macbus.replace(".","")
                    Macbus = Macbus.upper()#las letras se pasan a mayúsculas con el upper
                    Macbus = Macbus.upper()

                    while ciclo == 1:#mientras que el ciclo  sea igual a 1 se realizará el proceso de la busqueda
                        try:
                            ''' se creea una variable para almacenar el resultado que se obiene al enviar el comando 
                               de los detalles de los vecinos en el dispositivo al que se ha ingresado en el inicio,
                               después se usa el módulo textfsm que sirve para parsear el resultado del comando enviado,
                               posteriormente con el json.dumps se crea y retorna una cadena de caracteres con el nombre y valor 
                               que arrojo el comando para que por último se pase el texto plano a modo json'''

                            salida_cdp = conexion.send_command("show cdp neighbors detail",use_textfsm = True)
                            salida_cdp = (json.dumps(salida_cdp, indent = 2))#Se reduce la cantidad de datos de nombre y resultado ejemplo:(vlan =vlan1.../dispositivo=sw1...etc)
                            cdp_j = json.loads(salida_cdp)#sirve para cambiar a json el texto plano

                            #mac= f"show mac address-table | include {mac2}"
                           #print(mac)
                           # salida_mac = conexion.send_command(mac,use_textfsm = True)
                            #salida_mac = (json.dumps(salida_mac, indent = 2))#Se reduce la cantidad de datos de nombre y resultado
                            #cdp_jmac = json.loads(salida_mac)#sirve para cambiar a json el texto plano
                            #print ("1",cdp_jmac)

                            '''De la misma manera en la que anteriormente se realizó el proceso de obtener el resultado del comando de CDP en modo json
                               se realizará de la misma manera, solo que en este caso es con el comando para obtener la tabla de las MAC en modo json'''
                            salidaMac = conexion.send_command("show mac address-table",use_textfsm = True)
                            salidaMac = (json.dumps(salidaMac, indent = 2))#obtiene los datos de 2 en 2
                            MacJ = json.loads(salidaMac)#se convierte a json el que antes era el texto plano
    ##### MACJSON        ########               
                            print("\nImprime MACJSON 1111________", MacJ)

                            print ("\nImprime CDPJSON  ",cdp_j)
                            veci = (len(cdp_j))#muestra en json el total de los vecinos
                            lista_cdp = []#se crea una lista para los vecinos que se obtendrán con el cdp

                            if veci==0:
                                print("No hay vecinos")
                                
                                
                            for cont  in range(veci):#se hace el ciclo for para ir buscando de vecino en vecino 
                                #y poder buscar las coincidencias de la mac en cada dispositivo

                                #selecciona los datos que son necesarios de los vecinos para así poder mostrarlo en formato json 
                                # para tener mayor accebilidad después de haber tenido los datos del cdp
                                cdp_host = (cdp_j[cont]["destination_host"])#Dentro de la lista se toma el host destino
                                # y se almacena en la variable 
                                cdp_ip = (cdp_j [cont]["management_ip"])#Dentro de la lista se toma la ip del dispositivo
                                # y se almacena en la variable 
                                cdp_puerto = (cdp_j[cont]["local_port"])

                                try:
                                    #si el puerto esta con el formato FastEthernet se cambiará al formato Fa, ya que así es como arroja el resultado en el dispositivo
                                    fast_puerto=list(cdp_puerto)
                                    cdp_puerto=""
                                    dellist=("s","t","E","t","h","e","r","n","e","t")
                                    
                                    for l in dellist:#el for es para eliminar las letras que no se usarán
                                        fast_puerto.remove(l)

                                    for letras in fast_puerto:#se guardan las letras restantes
                                        cdp_puerto+=letras

                                    cdp_puerto=str(cdp_puerto)#imprime los datos almacenados

                                except:
                                    #si el puerto esta con el formato GigabitEthernet se cambiará al formato Gi
                                    fast_puerto = list(cdp_puerto)
                                    cdp_puerto = ""
                                    dellist = ("g","a","b","i","t","E","t","h","e","r","n","e","t")

                                    for l in dellist:#el for es para eliminar las letras que no se usarán
                                        fast_puerto.remove(l)#//Elimina letras que no se usarán

                                    for letra in fast_puerto:
                                        cdp_puerto+=letra#se guardan las letras restantes

                                    cdp_puerto = str(cdp_puerto)#imprime los datos almacenados
                            #se agrega en la lista anteriormente creada para almacenar los datos importantes que arroja cada vecino
                                lista_cdp.append({"destination_host":cdp_host,"management_ip":cdp_ip,"local_port":cdp_puerto})
                                
                        except:#//try_CDP
                            print("Ocurrió un ERROR al buscar los vecinos con cdp")#cuando no se tiene conexión con los vecinos arroja el anuncio
                            break
                        try:
                            print("\n lista CDP",lista_cdp)#imprime los datos importantes  de los vecinos que se almacenaron en
                            #listaCdp_detail=[]
                            #salidaCDP_Detail = conexion.send_command("sh cdp neighbors {cdp_puerto} detail",use_textfsm = True)
                            #salidaCDP_Detail = (json.dumps(salidaCDP_Detail, indent = 2))#obtiene los datos de 2 en 2
                            #MacJ = json.loads(salidaCDP_Detail)#se convierte a json el que antes era el texto plano

                            #listaCdp_detail.append({"destination_host":cdp_host,"management_ip":cdp_ip,"local_port":cdp_puerto})

                            #guarda en la variable el resultado de la busqueda con el comando
                            salidaMac = conexion.send_command("show mac address-table",use_textfsm = True)
                            salidaMac = (json.dumps(salidaMac, indent = 2))#obtiene los datos de 2 en 2 (nombre/valor)
                            MacJ = json.loads(salidaMac)#se convierte a json el que antes era el texto plano
    ##### MACJSON        ########               
                            #print("Imprime MACJSON  ", MacJ)
                            mac_can = (len(MacJ))#muestra en json el total de MAC
                            listaMac = []#se crea una lista para las mac

                            for m in range(mac_can) :
                                #Guarda los datos que se utilizarán de cada una de las MAC como lo es el nombre del dispositivo y el puerto
                                IPMac = (MacJ[m]["destination_address"])
                                PuertoMac = (MacJ[m]['destination_port'])

                                listaMac.append({'destination_address':IPMac , 'destination_port': PuertoMac})

                                #elimina el formato de la busqueda de las MAC
                                CodigoMac = (listaMac[m]['destination_address'])#Código de las MAC
                                busquedaMac = re.compile(r"\w\w\w\w.\w\w\w\w.\w\w\w\w")#Busqueda de las MAC con el formato mostrado
                                MacRE = (busquedaMac.search(CodigoMac))#Expresion regular de las MAC

                                DelMAC = MacRE.group()#Se elimina el formato de las MAC
                                DelMAC = DelMAC.replace(".","")#Se remplaza
                                DelMAC = DelMAC.upper()#se cambian a mayúsculas

                                #Se cambia el formato inicial por el modificado
                                MacJ[m]["destination_address"] = DelMAC

                        except:
                            print("Ocurrió un ERROR al buscar la MAC en las interfaces")
                            break
                        for m in range(mac_can):#Se buscan en la lista cada MAC

                            if Macbus == (MacJ[m]['destination_address']):#Se comparan las MAC para encontrar similitud
                                macR = (MacJ[m]['destination_address'])
                                puerto = (MacJ[m]['destination_port'])[0]#Encuentra el Puerto en el que se encuentra la MAC
                            
                            else:
                                pass#Si no se encuentra la Mac en este dispositivo se salta al siguiente
                        
                        for cont in range(veci):#//Por cada switch vecino
                            
                            #print (cont)
                            #print (veci)
                            puertoDes = (lista_cdp[cont]["local_port"])#Busca los datos que solo son necesarios
                            IPSSH = (lista_cdp[cont]["management_ip"])
                            #print(puertoDes)
                            #print (IPSSH)

                            if puerto == puertoDes:#//Compara el peurto de la mac, con los puertos vecinos
                                #Se ingresa por SSH
                                print("\n---->>>>>.......    Buscando      ........<<<<<------")
                                print(f"Conectado a la IP {IPSSH}\n")#imprime la ip del dispositivo al que se esta  conectando

                                #Se solicitan las credenciales para poder ingresar por medio de SSH
                                host = IPSSH
                                #usuario = input("Ingresa el usuario:")
                                usuario="cisco"
                                #contraseña = input("ingresa la contraseña:")
                                contraseña="cisco"
                                contra_e = "cisco"

                                #CONECION CON EL SWITCH---------------------------|
                                Dispositivo = {
                                    "host":host,
                                    "username":usuario,
                                    "password":contraseña,
                                    "device_type":"cisco_ios",
                                    "secret": contra_e,}

                                try:
                                    conexion = ConnectHandler(**Dispositivo)
                                    conexion.enable()
                                except:
                                    print("LAS CREDENCIALES NO SON CORRECTAS")

                            else:#Cuando ya no hay vecinos y encuentra la MAC
                                #Se obtiene el nombre del SW
                                shrun = conexion.send_command("show run | include hostname",use_textfsm = True)             

                                #Se muestran los resultados  que se obtuvieron de la busqueda de la MAC             
                                print(f"\nLa Mac solicitada {Macbus} fue encontrada ")
                                print(f"Se encuentra conectada al puerto {puerto} en {shrun}")
                                ciclo=0
                                break          
                            #print("Fallo la conexión")
                            break


            elif opcion == "4":
                    iniciando = False

        except ValueError:
            print("Ha ocurrido un error. Ingresa correctamente con número entero.")
            continue
