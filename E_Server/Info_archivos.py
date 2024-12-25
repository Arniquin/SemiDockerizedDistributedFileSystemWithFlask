class Info_archivos:
    def __init__(self, archivo, nombre, extension,
                fecha_creacion, fecha_modificacion, tamano, ttl,
                estado_compartido, local, ip_asociada, uri_asociada):
        self.archivo = archivo #0
        self.nombre = nombre #1
        self.extension = extension #2
        
        self.fecha_creacion = fecha_creacion #3
        self.fecha_modificacion = fecha_modificacion #4
        self.tamano = tamano #5
        self.ttl = ttl #6
        
        self.estado_compartido = estado_compartido #7
        self.local = local #8
        self.ip_asociada = ip_asociada #9
        self.uri_asociada = uri_asociada #10

    def __str__(self):
        return f"Archivo: {self.archivo}\n" \
               f"Nombre: {self.nombre}\n" \
               f"Extensión: {self.extension}\n" \
               f"Fecha de Creación: {self.fecha_creacion}\n" \
               f"Fecha de Modificación: {self.fecha_modificacion}\n" \
               f"Tamaño: {self.tamano} bytes\n" \
               f"TTL: {self.ttl}\n" \
               f"Estado Compartido: {self.estado_compartido}\n" \
               f"Local: {self.local}\n" \
               f"IP Asociada: {self.ip_asociada}\n" \
               f"URI Asociada: {self.uri_asociada}"
    

