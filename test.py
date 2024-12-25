import base64

def serializar_archivo(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
    # Serializar el contenido del archivo como una cadena codificada en base64
    return base64.b64encode(file_content).decode('utf-8')

def deserializar_archivo(serialized_content, file_path):
    # Decodificar la cadena codificada en base64 y guardar en el archivo
    decoded_content = base64.b64decode(serialized_content.encode('utf-8'))
    with open(file_path, 'wb') as file:
        file.write(decoded_content)

# Ejemplo de uso
ruta_del_archivo = "archivo.txt"

# Serializar el contenido del archivo
archivo_serializado = serializar_archivo(ruta_del_archivo)

# Deserializar y guardar en otro archivo
nueva_ruta_del_archivo = "archivo_copia.txt"
deserializar_archivo(archivo_serializado, nueva_ruta_del_archivo)
