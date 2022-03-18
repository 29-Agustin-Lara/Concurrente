import asyncio
import threading
import requests
import os
import pymongo 
import json

def cargarDatosServicio():
    for i in range(1,201):
        res = requests.get("https://randomuser.me/api/?inc=gender,name,location")
           
        if res.status_code == 200:         
            
            jsonD = res.json() 
            datos = (jsonD['results'][0])
            gender=(jsonD['results'][0].get('gender'))
            name=(jsonD['results'][0].get('name')) 
            location=(jsonD['results'][0].get('location')) 
    
            datosTexplane=(f"Datos:{i} \n Gender:%s\nName:%s\nLocation:%s"%(gender, name, location))
            
            guardarDatosBD(datos)       
            guardarDatosTxt(datosTexplane)                 
        else:
            print("error de respuesta")

def guardarDatosTxt(datosTexplane):
    print('Entra metodo para guardar datos Txt')
    file = open("/home/agustin/Documentos/datos.txt","a")
    file.write(str(datosTexplane))
    file.write("\n")
    file.close()
    

def guardarDatosBD(datos):
    print('Entra metodo para guardar datos en la base de datos')    
    with open('/home/agustin/Documentos/data.json','w') as fp:
        json.dump(datos,fp)    
    with open('/home/agustin/Documentos/data.json','r') as fp:
        data = json.load(fp)      
    
    print(type(data))  
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = client["personas"]
    mycol = mydb["personas_info"]  

    x = mycol.insert_one(data)
    for y in mycol.find():
        print(y) 

async def main():
    tarea = asyncio.create_task(creandoHilo())
    await tarea

async def creandoHilo():
    threading.Thread(target=cargarDatosServicio,).start()

asyncio.run(main())