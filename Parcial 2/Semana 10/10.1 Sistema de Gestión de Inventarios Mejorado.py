# Sistema mejorado sobre la gestion de un inventario en donde nos permitirá añadir, actualizar, eliminar y buscar productos utilizando estructura de datos personalizada.
#Dentro de estas mejoras ahora puede utilizar archivos para almacenar y recuperar información del inventario adémas de manejar excepciones durante la lectura de archivos

#Utilizamos una libreria que nos permitirá almacenar datos en formato estructurado tipo diccionario
import json
#agregamos una libreria que nos permitirá trabajar con archivos y directorios
import os

# Clase Producto que representa cada artículo del inventario
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Convierte los objetos a tipo diccionario
    def to_dict(self):
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }
    #metodo estático que crea un objeto desde el diccionario cargado JSON
    @staticmethod
    def from_dict(data):
        return Producto(
            data["id_producto"],
            data["nombre"],
            data["cantidad"],
            data["precio"]
        )
    # este metodo asignado definira como se mostrara el producto al imprimirlo
    def __str__(self):
        return f"ID: {self.id_producto}, Nombre: {self.nombre}, Cantidad: {self.cantidad}, Precio: {self.precio:.2f}"


# Clase Inventario
class Inventario:
    def __init__(self, archivo="inventario.json"):# se define donde se guardaran los productos
        self.archivo = archivo
        self.productos = []
        self.cargar_desde_archivo()

    # Guardar productos en archivo JSON
    def guardar_en_archivo(self):
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:#abre el archivo en modo escritura
                json.dump([p.to_dict() for p in self.productos], f ,indent=4 ) # convierte a diccionario los productos
            print(" Inventario guardado correctamente en el archivo.")
        # manejo de errores de permisos o problemas inesperados
        except PermissionError:
            print(" Error: No se tienen permisos para escribir en el archivo.")
        except Exception as e:
            print(f" Error inesperado al guardar: {e}")

    # Cargar productos desde archivo JSON
    # si el archivo todavia no existe, se crea vacío
    def cargar_desde_archivo(self):
        if not os.path.exists(self.archivo):
            # Si el archivo no existe, lo crea vacío
            with open(self.archivo, "w",encoding="utf-8") as f:
                json.dump([], f)

            return
        try:
            #Se abre el archivo en modo lectura
            with open(self.archivo, "r",encoding="utf-8") as f:
                datos = json.load(f)
                self.productos = [Producto.from_dict(d) for d in datos]
            print(f"Inventario cargado exitosamente desde el archivo. {len(self.productos)} producto(s) disponibles.")

        #Manejo de casos donde el archivo esta corrupto o hay errores
        except FileNotFoundError:
            print("Archivo de inventario no encontrado, se creará uno nuevo.")
            self.productos = []
        except json.JSONDecodeError:
            print("Error: El archivo está corrupto, se iniciará un inventario vacío.")
            self.productos = []
        except Exception as e:
            print(f"Error inesperado al cargar: {e}")
            self.productos = []

    #metodo de gestión
    #verifica que el ID sea unico
    def añadir_producto(self, producto):
        for p in self.productos:
            if p.id_producto == producto.id_producto:
                print(" Error: El ID ingresado ya existe en el inventario.")
                return
        self.productos.append(producto)
        self.guardar_en_archivo()
        print("Producto agregado exitosamente.")

    # Busca el producto por ID y lo elimina
    def eliminar_producto(self, id_producto):
        for p in self.productos:
            if p.id_producto == id_producto:
                self.productos.remove(p)
                self.guardar_en_archivo()
                print(" Producto eliminado correctamente.")
                return
        print("Producto no encontrado.")

    #actualizacion de cantidad y precio
    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        for p in self.productos:
            if p.id_producto == id_producto:
                if nueva_cantidad is not None:
                    p.cantidad = nueva_cantidad
                if nuevo_precio is not None:
                    p.precio = nuevo_precio
                self.guardar_en_archivo()
                print("Producto actualizado correctamente.")
                return
        print("Producto no encontrado.")

    #busqueda por nombre parcial
    def buscar_producto(self, nombre):
        resultados = [p for p in self.productos if nombre.lower() in p.nombre.lower()]
        if resultados:
            print("Resultados encontrados:")
            for p in resultados:
                print(p)
        else:
            print("No se encontró ningún producto con ese nombre.")

    #Muestra del inventario
    def mostrar_productos(self):
        if not self.productos:
            print("El inventario está vacío.")
        else:
            print("Productos en inventario:")
            for p in self.productos:
                print(p)


# Menú interactivo
def menu():
    inventario = Inventario()
    while True:
        print("\n--- MENÚ DE GESTIÓN DE INVENTARIO ---")
        print("1. Añadir nuevo producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar cantidad o precio de un producto por ID")
        print("4. Buscar producto(s) por nombre")
        print("5. Mostrar todos los productos en el inventario")
        print("6. Cerrar menú")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                id_producto = input("Ingrese ID único del producto: ")
                nombre = input("Ingrese nombre del producto: ")
                cantidad = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
                producto = Producto(id_producto, nombre, cantidad, precio)
                inventario.añadir_producto(producto)
            except ValueError:
                print("Error: cantidad y precio deben ser números válidos.")

        elif opcion == "2":
            id_producto = input("Ingrese el ID del producto a eliminar: ")
            inventario.eliminar_producto(id_producto)

        elif opcion == "3":
            id_producto = input("Ingrese el ID del producto a actualizar: ")
            try:
                cantidad = input("Ingrese nueva cantidad (deje vacío si no desea cambiarla): ")
                precio = input("Ingrese nuevo precio (deje vacío si no desea cambiarlo): ")

                nueva_cantidad = int(cantidad) if cantidad else None
                nuevo_precio = float(precio) if precio else None

                inventario.actualizar_producto(id_producto, nueva_cantidad, nuevo_precio)
            except ValueError:
                print("Error: los valores no son válidos.")

        elif opcion == "4":
            nombre = input("Ingrese el nombre del producto que quiere buscar: ")
            inventario.buscar_producto(nombre)

        elif opcion == "5":
            inventario.mostrar_productos()

        elif opcion == "6":
            print("Sistema cerrado correctamente...")
            break

        else:
            print("Opción inválida, intente nuevamente.")


if __name__ == "__main__":
    menu()
