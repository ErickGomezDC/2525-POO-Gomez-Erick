# Programa que gestiona un archivo txt para escritura en donde utiliza constructor para abrirlo y destructor para cerrarlo correctamente

class gestor_de_archivos:
    def __init__(self, nombre_archivo):
        """
        Agregamos el constructor de la clase.
        Se ejecuta automáticamente cuando se crea un objeto de la clase.
        También definimos el archivo en modo escritura.
        """
        self.nombre_archivo = nombre_archivo
        self.archivo = open(nombre_archivo, 'w')
        print(f"[Aviso] El archivo '{self.nombre_archivo}' esta abierto para escritura.")

    def escribir_linea_de_archivo(self, texto):
        """
        Agregamos el metodo para escribir texto dentro del archivo.
        """
        self.archivo.write(texto + '\n')
        print(f"escrito en el archivo: {texto}")

    def __del__(self):
        """
        Agregamos el destructor de la clase.
        Este se ejecutara automáticamente cuando el objeto es destruido o el programa termina.
        En este caso se cerrara el archivo abierto para liberar recursos.
        """
        self.archivo.close()
        print(f"[Aviso] El archivo '{self.nombre_archivo}' fue cerrado correctamente.")

# Creamos los objetos de la clase y escribimos líneas en el archivo respectivamente
gestor = gestor_de_archivos("Constructores y destructores.txt")
gestor.escribir_linea_de_archivo("Buenas Tardes, este archivo fue creado con la implementación de constructores y destructores.")
gestor.escribir_linea_de_archivo("Los constructores y destructores son los encargados de inicializar un objeto cuando este es creado y cerrar o eliminar el espacio de memoria.")

# El destructor se ejecutará automáticamente al final del programa o al eliminar el objeto
