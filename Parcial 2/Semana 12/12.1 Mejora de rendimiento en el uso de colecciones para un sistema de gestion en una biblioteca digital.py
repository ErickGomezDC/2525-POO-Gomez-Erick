# Sistema Avanzado en la utilizacion de colecciones para la mejora de rendimiento en la gestion de una biblioteca digital en donde nos permitirá añadir libros, usuarios y prestamos, ademas de poder eliminar usuarios, libros y respectivamente su busqueda y enlistamiento de cada usuario, libro y prestamo.
#Utilizando un manejo eficiente de los ítems del inventario interactuando entre libros y usuarios permitiendo gestionar el almacenamiento y información de cada uno de manera clara y ordenada

#Utilizamos una libreria que nos permitirá trabajar con archivos json
import json
#importamos una libreria con funciones del sistema operativo que comprobara si existe un archivo
import os

# Clase Libro
class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        self.info = (titulo, autor)  # tupla inmutable
        self.categoria = categoria
        self.isbn = isbn

    def to_dict(self):
        return {
            "titulo": self.info[0],
            "autor": self.info[1],
            "categoria": self.categoria,
            "isbn": self.isbn
        }

# Clase Usuario
class Usuario:
    def __init__(self, nombre, user_id):
        self.nombre = nombre
        self.user_id = user_id
        self.prestados = []  # lista de ISBN prestados

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "user_id": self.user_id,
            "prestados": self.prestados
        }

# Clase Biblioteca
class Biblioteca:
    def __init__(self):
        self.libros = {}     # isbn -> Libro
        self.usuarios = {}   # id -> Usuario
        self.prestamos = {}
        self.user_ids = set()
        self.carga_de_datos()

    #carga y guardado de datos
    def carga_de_datos(self):
        if os.path.exists("libros.json"):#verifica si el archivo existe
            with open("libros.json", "r") as f:
                data = json.load(f)
                self.libros = {l["isbn"]: Libro(l["titulo"], l["autor"], l["categoria"], l["isbn"]) for l in data}#los datos se cargan a partir de el ISBN como clave

        #Aqui cargamos los usuarios y libros prestados
        if os.path.exists("usuarios.json"):
            with open("usuarios.json", "r") as f:
                data = json.load(f)
                self.usuarios = {u["user_id"]: Usuario(u["nombre"], u["user_id"]) for u in data}
                for u in data:
                    self.usuarios[u["user_id"]].prestados = u["prestados"]
                    self.user_ids.add(u["user_id"])

        #carga de los prestamos activos
        if os.path.exists("prestamos.json"):
            with open("prestamos.json", "r") as f:
                self.prestamos = json.load(f)

    # aqui se guardan todos los datos en archivos json (libros,usuarios,prestamos)
    def guarda_datos(self):
        with open("libros.json", "w") as f:
            json.dump([l.to_dict() for l in self.libros.values()], f, indent=4)

        with open("usuarios.json", "w") as f:
            json.dump([u.to_dict() for u in self.usuarios.values()], f, indent=4)

        with open("prestamos.json", "w") as f:
            json.dump(self.prestamos, f, indent=4)


    # Funciones para la gestion de la biblioteca

    def añadir_libro(self, titulo, autor, categoria, isbn):
        if isbn in self.libros:
            print("Ya existe un libro con ese ISBN.")
        else:
            self.libros[isbn] = Libro(titulo, autor, categoria, isbn)
            print("Libro añadido con éxito.")

    def quitar_libro(self, isbn):
        if isbn in self.libros:
            del self.libros[isbn]
            print("Libro eliminado.")
        else:
            print("No existe ese libro.")

    def registrar_usuario(self, nombre, user_id):
        if user_id in self.usuarios:
            print("Ese ID ya está registrado.")
        else:
            self.usuarios[user_id] = Usuario(nombre, user_id)
            self.user_ids.add(user_id)
            print("Usuario registrado.")

    def dar_baja_usuario(self, user_id):
        if user_id in self.usuarios:
            del self.usuarios[user_id]
            self.user_ids.remove(user_id)
            print("Usuario dado de baja.")
        else:
            print("No existe ese usuario.")

    def prestar_libro(self, user_id, isbn):
        if user_id not in self.usuarios:
            print("Usuario no registrado.")
            return
        if isbn not in self.libros:
            print("Libro no disponible.")
            return
        if user_id not in self.prestamos:
            self.prestamos[user_id] = []

        if isbn in self.prestamos[user_id]:
            print("Ese libro ya está prestado a este usuario.")
        else:
            self.prestamos[user_id].append(isbn)
            self.usuarios[user_id].prestados.append(isbn)
            print("Libro prestado con éxito.")

    def devolver_libro(self, user_id, isbn):
        if user_id in self.prestamos and isbn in self.prestamos[user_id]:
            self.prestamos[user_id].remove(isbn)
            self.usuarios[user_id].prestados.remove(isbn)
            print("Libro devuelto con éxito.")
        else:
            print("No se puede devolver, no estaba prestado.")

    def buscar_libro(self, clave, tipo="titulo"):
        resultados = []
        for libro in self.libros.values():
            if tipo == "titulo" and clave.lower() in libro.info[0].lower():
                resultados.append(libro)
            elif tipo == "autor" and clave.lower() in libro.info[1].lower():
                resultados.append(libro)
            elif tipo == "categoria" and clave.lower() in libro.categoria.lower():
                resultados.append(libro)

        if resultados:
            print("Resultados de búsqueda:")
            for l in resultados:
                print(f"- {l.info[0]} ({l.info[1]}) - {l.categoria} - ISBN: {l.isbn}")
        else:
            print("No se encontraron coincidencias.")

    def listar_prestados(self, user_id):
        if user_id in self.usuarios:
            if self.usuarios[user_id].prestados:
                print(f"Libros prestados a {self.usuarios[user_id].nombre}:")
                for isbn in self.usuarios[user_id].prestados:
                    libro = self.libros[isbn]
                    print(f"- {libro.info[0]} ({libro.info[1]})")
            else:
                print("No tiene libros prestados.")
        else:
            print("Usuario no encontrado.")

    def listar_todos_libros(self):
        if self.libros:
            print("Todos los libros en la biblioteca:")
            for libro in self.libros.values():
                print(f"- {libro.info[0]} ({libro.info[1]}) - {libro.categoria} - ISBN: {libro.isbn}")
        else:
            print("No hay libros en la biblioteca.")

    def listar_todos_usuarios(self):
        if self.usuarios:
            print("Usuarios registrados:")
            for usuario in self.usuarios.values():
                print(f"- {usuario.nombre} (ID: {usuario.user_id})")
        else:
            print("No hay usuarios registrados.")

    def listar_todos_prestamos(self):
        if self.prestamos:
            print("Todos los préstamos actuales:")
            for user_id, libros_prestados in self.prestamos.items():
                usuario = self.usuarios[user_id].nombre
                print(f"\n {usuario} (ID: {user_id}):")
                for isbn in libros_prestados:
                    libro = self.libros[isbn]
                    print(f"   - {libro.info[0]} ({libro.info[1]})")
        else:
            print("No hay préstamos activos.")

# Menú interactivo
def menu():
    biblio = Biblioteca()

    while True:
        print("\n===== MENÚ BIBLIOTECA DIGITAL =====")
        print("1. Añadir libro")
        print("2. Quitar libro")
        print("3. Registrar usuario")
        print("4. Dar de baja a usuario")
        print("5. Prestar libro")
        print("6. Devolver libro")
        print("7. Buscar libro")
        print("8. Listar libros prestados (por usuario)")
        print("9. Listar todos los libros")
        print("10. Listar todos los usuarios")
        print("11. Listar todos los préstamos")
        print("12. Guardar y salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            categoria = input("Categoría: ")
            isbn = input("ISBN: ")
            biblio.añadir_libro(titulo, autor, categoria, isbn)

        elif opcion == "2":
            isbn = input("ISBN del libro a eliminar: ")
            biblio.quitar_libro(isbn)

        elif opcion == "3":
            nombre = input("Nombre: ")
            user_id = input("ID de usuario: ")
            biblio.registrar_usuario(nombre, user_id)

        elif opcion == "4":
            user_id = input("ID de usuario a dar de baja: ")
            biblio.dar_baja_usuario(user_id)

        elif opcion == "5":
            user_id = input("ID de usuario: ")
            isbn = input("ISBN del libro: ")
            biblio.prestar_libro(user_id, isbn)

        elif opcion == "6":
            user_id = input("ID de usuario: ")
            isbn = input("ISBN del libro: ")
            biblio.devolver_libro(user_id, isbn)

        elif opcion == "7":
            tipo = input("Buscar por (titulo/autor/categoria): ").lower()
            clave = input("Clave de búsqueda: ")
            biblio.buscar_libro(clave, tipo)

        elif opcion == "8":
            user_id = input("ID de usuario: ")
            biblio.listar_prestados(user_id)

        elif opcion == "9":
            biblio.listar_todos_libros()

        elif opcion == "10":
            biblio.listar_todos_usuarios()

        elif opcion == "11":
            biblio.listar_todos_prestamos()

        elif opcion == "12":
            biblio.guarda_datos()
            print("Datos guardados, cerrando programa...")
            break
        else:
            print("Opción no válida.")

# Ejecutar el programa

if __name__ == "__main__":
    menu()
