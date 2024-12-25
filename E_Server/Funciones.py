import os
import os.path
import datetime
import random
import base64

from pymongo import MongoClient
from Info_archivos import *  # Importing the Info_archivos class

def cast_to_info_archivos(documento):
    """
    Converts a MongoDB document to an Info_archivos instance.
    
    Input:
        documento (dict): The MongoDB document containing file information.

    Output:
        Info_archivos: An instance of the Info_archivos class.
    """
    return Info_archivos(
        archivo=documento['archivo'],
        nombre=documento['nombre'],
        extension=documento['extension'],
        fecha_creacion=documento['fecha_creacion'],
        fecha_modificacion=documento['fecha_modificacion'],
        tamano=documento['tamano'],
        ttl=documento['ttl'],
        estado_compartido=documento['estado_compartido'],
        local=documento['local'],
        ip_asociada=documento['ip_asociada'],
        uri_asociada=documento['uri_asociada']
    )

def generar_numero_aleatorio(p_min=0, p_max=100):
    """
    Generates a random integer within a specified range.
    
    Input:
        p_min (int): Minimum value (inclusive).
        p_max (int): Maximum value (inclusive).

    Output:
        int: A random integer between p_min and p_max.
    """
    return random.randint(p_min, p_max)
    
def obtener_documentos_en_directorio(ruta_directorio, ip_asociada, uri_asociada):
    """
    Retrieves documents in a specified directory and constructs their metadata.
    
    Input:
        ruta_directorio (str): The path to the directory.
        ip_asociada (str): Associated IP address.
        uri_asociada (str): Associated URI.

    Output:
        list: A list of documents, each represented as a list of metadata attributes.
    """
    try:
        archivos = os.listdir(ruta_directorio)  # List files in the directory
        lista_documentos = []

        for archivo in archivos:
            ruta_completa = os.path.join(ruta_directorio, archivo)

            if os.path.isfile(ruta_completa):
                # Gather metadata into a list
                info_archivo = []
                info_archivo.append(str(archivo))  # File name
                info_archivo.append(str(os.path.splitext(archivo)[0]))  # File base name
                info_archivo.append(str(os.path.splitext(archivo)[1]))  # File extension
                info_archivo.append(str(datetime.datetime.fromtimestamp(os.path.getctime(ruta_completa))))  # Creation date
                info_archivo.append(str(datetime.datetime.fromtimestamp(os.path.getmtime(ruta_completa))))  # Modification date
                info_archivo.append(str(os.path.getsize(ruta_completa)))  # File size
                info_archivo.append(str(generar_numero_aleatorio(50, 100)))  # Random TTL value
                info_archivo.append("-")  # Shared state (placeholder)
                info_archivo.append(str(True))  # Local status
                info_archivo.append(str(ip_asociada))  # Associated IP
                info_archivo.append(str(uri_asociada))  # Associated URI

                lista_documentos.append(info_archivo)  # Add to the list

        return lista_documentos  # Return the list of document metadata
    except FileNotFoundError:
        print(f"El directorio '{ruta_directorio}' no fue encontrado.")
        return []  # Return an empty list on error

def borrar_archivo(ubicacion_archivo, nombre_archivo):
    """
    Deletes a specified file.
    
    Input:
        ubicacion_archivo (str): The directory containing the file.
        nombre_archivo (str): The name of the file to delete.

    Output:
        None: Prints a success or error message.
    """
    archivo_borrar = ubicacion_archivo + "/" + nombre_archivo
    try:
        os.remove(archivo_borrar)  # Attempt to delete the file
        print(f"Archivo en {nombre_archivo} eliminado con éxito.")
    except FileNotFoundError:
        print(f"El archivo en {nombre_archivo} no existe.")
    except Exception as e:
        print(f"Error al intentar eliminar el archivo en {nombre_archivo}: {e}")

def cast_from_list_to_class(lista_de_archivos):
    """
    Converts a list of file metadata to a list of Info_archivos instances.
    
    Input:
        lista_de_archivos (list): A list of file metadata.

    Output:
        list: A list of Info_archivos instances.
    """
    lista_de_elementos = []
    for e in lista_de_archivos:
        new_e = Info_archivos(
            archivo=e[0],
            nombre=e[1],
            extension=e[2],
            fecha_creacion=e[3],
            fecha_modificacion=e[4],
            tamano=e[5],
            ttl=e[6],
            estado_compartido=e[7],
            local=e[8],
            ip_asociada=e[9],
            uri_asociada=e[10]
        )
        lista_de_elementos.append(new_e)  # Add the new instance to the list
    return lista_de_elementos

def cast_from_document_to_list(documento):
    """
    Converts a MongoDB document to a list of attributes.
    
    Input:
        documento (dict): The MongoDB document.

    Output:
        list: A list of attributes extracted from the document.
    """
    return [
        documento['archivo'],
        documento['nombre'],
        documento['extension'],
        documento['fecha_creacion'],
        documento['fecha_modificacion'],
        documento['tamano'],
        documento['ttl'],
        documento['estado_compartido'],
        documento['local'],
        documento['ip_asociada'],
        documento['uri_asociada']
    ]

def c_db(lista_de_archivos):
    """
    Inserts file metadata into a MongoDB collection.
    
    Input:
        lista_de_archivos (list): A list of file metadata.

    Output:
        None: Inserts documents into the MongoDB collection.
    """
    lista_de_elementos = cast_from_list_to_class(lista_de_archivos)

    # Conexión a la instancia local de MongoDB (por defecto en el puerto 27017)
    client = MongoClient('localhost', 27017)
    # Seleccionar la base de datos 'base_archivos'
    db = client.base_archivos
    # Seleccionar la colección 'coleccion_archivos'
    collection = db.coleccion_archivos

    for info_archivo in lista_de_elementos:
        documento = vars(info_archivo)  # Convert the instance to a dictionary
        collection.insert_one(documento)  # Insert the document into the collection

def r_db_all():
    """
    Retrieves all documents from the MongoDB collection.
    
    Output:
        list: A list of all documents in the collection, represented as lists of attributes.
    """
    # Conexión a la instancia local de MongoDB (por defecto en el puerto 27017)
    client = MongoClient('localhost', 27017)
    # Seleccionar la base de datos 'base_archivos'
    db = client.base_archivos
    # Seleccionar la colección 'coleccion_archivos'
    collection = db.coleccion_archivos

    result = collection.find()  # Retrieve all documents
    info_archivo_lists = []
    for document in result:
        info_archivo_list = cast_from_document_to_list(document)  # Convert each document
        info_archivo_lists.append(info_archivo_list)  # Add to the list
    return info_archivo_lists  # Return the list of documents

def r_db_search_all(archivos_buscar):
    """
    Searches for documents by file name in the MongoDB collection.
    
    Input:
        archivos_buscar (str): The file name to search for.

    Output:
        list: A list of matching documents represented as lists of attributes.
    """
    client = MongoClient('localhost', 27017)
    db = client.base_archivos
    collection = db.coleccion_archivos

    filtro = {"archivo": archivos_buscar}  # Define the search filter
    result = collection.find(filtro)  # Retrieve matching documents

    info_archivo_lists = []
    for document in result:
        info_archivo_list = cast_from_document_to_list(document)
        info_archivo_lists.append(info_archivo_list)  # Add to the list
    return info_archivo_lists  # Return the list of matching documents

def r_db_search_one(archivo_buscar):
    """
    Searches for a single document by file name in the MongoDB collection.
    
    Input:
        archivo_buscar (str): The file name to search for.

    Output:
        list: A list of attributes of the found document or None if not found.
    """
    client = MongoClient('localhost', 27017)
    db = client.base_archivos
    collection = db.coleccion_archivos

    filtro = {"archivo": archivo_buscar}  # Define the search filter
    documento_encontrado = collection.find_one(filtro)  # Retrieve the first matching document
    
    if documento_encontrado:
        info_archivo = cast_from_document_to_list(documento_encontrado)  # Convert if found
    else:
        info_archivo = None  # Return None if not found

    return info_archivo  # Return the document attributes or None

def d_db_all():
    """
    Deletes all documents from the MongoDB collection.
    
    Output:
        None: Prints the number of deleted documents.
    """
    client = MongoClient('localhost', 27017)
    db = client.base_archivos
    collection = db.coleccion_archivos
    result = collection.delete_many({})  # Delete all documents
    print(f"Se han borrado {result.deleted_count} documentos.")  # Print the count of deleted documents

def d_db_filter_many(filename):
    """
    Deletes documents with a specific file name from the MongoDB collection.
    
    Input:
        filename (str): The file name to filter by.

    Output:
        None: Prints the number of deleted documents.
    """
    client = MongoClient('localhost', 27017)
    db = client.base_archivos
    collection = db.coleccion_archivos
    result = collection.delete_many({"archivo": filename})  # Delete documents with the specified file name
    print(f"Se han borrado {result.deleted_count} documentos con el nombre {filename}.")  # Print the count of deleted documents

def serializar_archivo(file_path):
    """
    Serializes a file to a base64 encoded string.
    
    Input:
        file_path (str): The path to the file to serialize.

    Output:
        str: The base64 encoded content of the file.
    """
    with open(file_path, 'rb') as file:
        file_content = file.read()  # Read the file content
    return base64.b64encode(file_content).decode('utf-8')  # Return the encoded content as a string

def deserializar_archivo(file_path, serialized_content):
    """
    Deserializes a base64 encoded string and saves it to a file.
    
    Input:
        file_path (str): The path where the file will be saved.
        serialized_content (str): The base64 encoded content to decode and save.

    Output:
        None: Writes the decoded content to the specified file path.
    """
    # Decodificar la cadena codificada en base64 y guardar en el archivo
    decoded_content = base64.b64decode(serialized_content.encode('utf-8'))
    with open(file_path, 'wb') as file:
        file.write(decoded_content)  # Write the decoded content to the file
