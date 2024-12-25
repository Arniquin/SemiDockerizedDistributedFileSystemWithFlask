import Pyro4
from Funciones import *  # Importing functions defined in Funciones module

class Server(object):
    @Pyro4.expose
    def welcomeMessage(self, name):
        """
        Welcomes a user by name.
        
        Input:
            name (str): The name of the user.
        
        Output:
            str: A welcome message.
        """
        return ("Hi welcome " + str(name))

    @Pyro4.expose
    def set_permissions(self):
        """
        Retrieves document permissions from the specified directory.
        
        Output:
            list: A list of document metadata.
        """
        info = obtener_documentos_en_directorio(directorio, ip_local, nombre_local)
        return info

    # Uncommenting this method would allow the server to receive permissions and update the info list.
    # @Pyro4.expose
    # def get_permissions(self, permisos, info):
    #     print("Permisos recibidos")
    #     for i, e in enumerate(info):
    #         e[7] = permisos[i]
    #     return info

    @Pyro4.expose
    def generar_base_local(self, permisos, info):
        """
        Generates a local database with specified permissions.
        
        Input:
            permisos (list): A list of permissions for each document.
            info (list): A list of document metadata to update.
        
        Output:
            None: Updates the database with the provided information.
        """
        for i, e in enumerate(info):
            e[7] = permisos[i]  # Update permissions
        c_db(info)  # Save updated metadata to the database

    @Pyro4.expose
    def leer_base(self):
        """
        Reads all documents from the local database.
        
        Output:
            list: A list of all documents in the database.
        """
        resultados = r_db_all()
        return resultados  # Return the documents

    @Pyro4.expose
    def generar_listas(self):
        """
        Generates a list of documents from local and external databases.
        
        Output:
            list: A combined list of documents from local and external sources.
        """
        try:
            resultados = r_db_all()  # Read local documents
            ns = Pyro4.locateNS(ip_servidor)  # Locate the name server
            all_names = ns.list()  # List all names registered with the name server
            nombres_excluir = ["Pyro.NameServer", nombre_local]  # Exclude certain names
            
            for name, uri in all_names.items():
                if name not in nombres_excluir:
                    try:
                        objeto_remoto = Pyro4.Proxy(uri)  # Create a proxy for the external server
                        resultados_ext = objeto_remoto.leer_base()  # Read documents from external server
                        for e in resultados_ext:
                            e[8] = "Externo"  # Mark as external
                        resultados.extend(resultados_ext)  # Add external documents to the results
                    except Exception as e:
                        pass  # Ignore exceptions during external calls
            return resultados  # Return the combined results
        except Exception as e:
            print(f"Error al obtener resultados generales: {e}")
            return []  # Return an empty list on error

    @Pyro4.expose
    def eliminar_archivo(self, file_name):
        """
        Deletes a specified file from the local database and filesystem.
        
        Input:
            file_name (str): The name of the file to delete.
        
        Output:
            None: Deletes the file from the database and filesystem.
        """
        d_db_filter_many(file_name)  # Remove from database
        borrar_archivo(directorio, file_name)  # Remove from filesystem

    @Pyro4.expose
    def buscar_eliminar_archivo(self, file_name, param_uri):
        """
        Searches for a file and deletes it either locally or externally based on URI.
        
        Input:
            file_name (str): The name of the file to delete.
            param_uri (str): The URI to compare for determining deletion location.
        
        Output:
            None: Deletes the file from the appropriate location.
        """
        if uri == param_uri:
            d_db_filter_many(file_name)  # Delete locally
            borrar_archivo(directorio, file_name)
        else:
            ns = Pyro4.locateNS(ip_servidor)  # Locate the name server
            uri_e = ns.lookup(param_uri)  # Look up the external server's URI
            objeto_remoto = Pyro4.Proxy(uri_e)  # Create a proxy for the external server
            objeto_remoto.eliminar_archivo(file_name)  # Delete the file externally

    @Pyro4.expose
    def copiar_archivo(self, file_name, param_uri):
        """
        Copies a file from an external server to the local directory.
        
        Input:
            file_name (str): The name of the file to copy.
            param_uri (str): The URI of the external server.
        
        Output:
            None: The file is copied to the local directory.
        """
        ns = Pyro4.locateNS(ip_servidor)  # Locate the name server
        uri_e = ns.lookup(param_uri)  # Look up the external server's URI
        objeto_remoto = Pyro4.Proxy(uri_e)  # Create a proxy for the external server
        
        archivo_recibido_serializado = objeto_remoto.generar_archivo(file_name)  # Get serialized file
        deserializar_archivo(directorio + "/" + file_name, archivo_recibido_serializado)  # Save the file

    @Pyro4.expose
    def generar_archivo(self, file_name):
        """
        Generates a serialized version of a specified file.
        
        Input:
            file_name (str): The name of the file to serialize.
        
        Output:
            str: The serialized content of the file.
        """
        return serializar_archivo(directorio + "/" + file_name)  # Serialize the file

def startServer():
    """
    Initializes and starts the Pyro4 server.
    
    Output:
        None: The server runs indefinitely until stopped.
    """
    global ip_local
    global ip_servidor
    global uri
    global directorio
    global nombre_local

    ip_local = "192.168.100.4"  # Local IP address
    ip_servidor = "192.168.100.3"  # Server IP address
    directorio = "C:/Users/GR/Desktop/TEST"  # Directory for files
    ruta_archivo = "C:/Users/GR/Desktop/Proyect arn/DockerFolder/URI/uri.txt"  # Path to store URI
    nombre_local = "CHRIS"  # Local server name

    server = Server()  # Create server instance
    daemon = Pyro4.Daemon(host=ip_local, port=9095)  # Create a Pyro4 daemon
    ns = Pyro4.locateNS(ip_servidor)  # Locate the name server
    uri = daemon.register(server)  # Register the server with the daemon

    with open(ruta_archivo, 'w') as file:
        file.write(str(uri))  # Write the URI to a file
    ns.register(nombre_local, uri)  # Register the server with the name server

    print(uri)  # Print the URI for reference
    daemon.requestLoop()  # Start the server loop

if __name__ == "__main__":
    startServer()  # Start the server
