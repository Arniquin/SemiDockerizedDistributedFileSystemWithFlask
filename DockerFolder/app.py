from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import Pyro4
import logging
import os

app=Flask(__name__)

# client = MongoClient(host='test_mongodb',port=27017, username='root', password='pass',authSource="admin")
# db = client.mytododb
# tasks_collection = db.tasks

global nFiles
nFiles=0

global tasks
global base
global fileList
fileList=[]

global server
with open('/app/URI/uri.txt', 'r') as file:
    uri = file.readline()
server=Pyro4.Proxy(uri)


@app.route('/')
def inicio():
    global tasks
    tasks=server.set_permissions()
    base=server.leer_base()
    nombres_archivos_lista2 = [archivo[0] for archivo in base]
    tasks = [archivo for archivo in tasks if archivo[0] not in nombres_archivos_lista2]
    if len(tasks) == 0:
        tasks2=server.generar_listas()
        return render_template('index.html',tasks=tasks2)
    task=tasks[nFiles]
    return render_template('permisos.html',task=task)

@app.route('/procesar_seleccion', methods=['POST'])
def procesar_seleccion():
    global nFiles
    global fileList
    print("tamaño lista ",str(len(tasks)))
    if nFiles<len(tasks):
        file_perm=request.form['opcion']  
        fileList.append(file_perm)
        nFiles+=1
        if nFiles==len(tasks):
            # tasks2=server.get_permissions(fileList,tasks)
            server.generar_base_local(fileList,tasks)
            tasks2=server.generar_listas()
            nFiles=0
            fileList.clear()
            return render_template('index.html',tasks=tasks2)
        task=tasks[nFiles]
        return render_template('permisos.html',task=task)
    else:
        server.generar_base_local(fileList,tasks)
        tasks2=server.generar_listas()
        nFiles=0
        fileList.clear()
        return render_template('index.html',tasks=tasks2)
         
# @app.route('/files', methods=['POST'])
# def files():
#      print()         





@app.route('/copy_task/<file_name>/<uri>', methods=['GET'])
def copy_task(file_name, uri):
    print("file_name:",file_name)
    print("uri:",uri)

    server.copiar_archivo(file_name, uri)
    
    tasks2=server.generar_listas()
    return render_template('index.html',tasks=tasks2)

@app.route('/delete_task/<file_name>/<uri>', methods=['GET'])
def delete_task(file_name, uri):
    print("file_name:",file_name)
    print("uri:",uri)

    server.buscar_eliminar_archivo(file_name, uri)
    tasks2=server.generar_listas()
    return render_template('index.html',tasks=tasks2)






if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
