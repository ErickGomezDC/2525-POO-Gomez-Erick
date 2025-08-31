# Sistema Avanzado sobre la gestion de un inventario en donde nos permitirá añadir, actualizar, eliminar y buscar productos utilizando estructura de datos personalizada.
#Utilizando un manejo eficiente de los ítems del inventario y el almacenamiento de la información de inventario en archivos

#Utilizamos una libreria que nos permitirá trabajar con archivos json
import json
#importamos una libreria con funciones del sistema operativo que comprobara si existe un archivo
import os

# Clase Producto
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    #agregamos un constructor qie se ejecutara cada vez qie se crea un nuevo producto
    def to_dict(self):
        return {
            "id": self.id_producto,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }
    #Metodo estatico que crea un objeto a partir de un diccionario
    @staticmethod
    def from_dict(data):
        return Producto(data["id"], data["nombre"], data["cantidad"], data["precio"])



# Clase Inventario
class Inventario:
    def __init__(self):
        self.productos = {}# es un diccionario donde la clave es el id de producto y el valor un producto

    def añadir_producto(self, producto):#verificara si el ID ya existe
        if producto.id_producto in self.productos:
            print("El producto con este ID ya existe.")
        else:
            self.productos[producto.id_producto] = producto
            print("Producto añadido con éxito.")

    def eliminar_producto(self, id_producto):# si el ID existe puede eliminar el producto del inventario
        if id_producto in self.productos:
            del self.productos[id_producto]
            print("Producto eliminado.")
        else:
            print("No se encontró el producto con ese ID.")

    def actualizar_cantidad(self, id_producto, nueva_cantidad):#se busca por ID el producto y cambia su cantidad
        if id_producto in self.productos:
            self.productos[id_producto].cantidad = nueva_cantidad
            print("Cantidad actualizada.")
        else:
            print("No se encontró el producto con ese ID.")

    def actualizar_precio(self, id_producto, nuevo_precio):# busca el producto por su ID y cambia su precio
        if id_producto in self.productos:
            self.productos[id_producto].precio = nuevo_precio
            print("Precio actualizado.")
        else:
            print("No se encontró el producto con ese ID.")

    def buscar_por_nombre(self, nombre):#se utiliza para filtrar productos en base a su nombre parcial o completo
        encontrados = [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]
        if encontrados:
            print("\n🔎 Resultados de búsqueda:")
            self.organizacion_de_inventario (encontrados)
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar_todos(self):# imprime la tabla con todos los productos almacenados
        if not self.productos:
            print("El inventario está vacío.")
        else:
            print("\n Inventario actual:")
            self.organizacion_de_inventario (self.productos.values())

    def organizacion_de_inventario(self, lista_productos):# para un mejor orden creamos una tabla con columnas con ID, nombre, cantidad y precio
        print("-" * 58)
        print(f"{'ID':<8} | {'Nombre':<15} | {'Cantidad':<10} | {'Precio':<10}")
        print("-" * 58)
        for p in lista_productos:
            print(f"{p.id_producto:<8} | {p.nombre:<15} | {p.cantidad:<10} | ${p.precio:<10.2f}")
        print("-" * 58)

    def guardar_en_archivo(self, filename="inventario.json"):#convierte todos los productos a diccionario y los guarda en archivo json
        with open(filename, "w", encoding="utf-8") as f:
            data = {id: p.to_dict() for id, p in self.productos.items()}
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Inventario guardado en archivo.")

    def cargar_desde_archivo(self, filename="inventario.json"):#si el archivo existe lo abre y carga en json
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.productos = {id: Producto.from_dict(p) for id, p in data.items()}
            print(" Inventario cargado desde archivo.")
        else:
            print("No existe un archivo de inventario. Se creará uno nuevo.")


# Interfaz de Usuario

def menu():
    inventario = Inventario()
    inventario.cargar_desde_archivo()

    # mostramos menu de opciones
    while True:
        print("\n----- MENÚ DE INVENTARIO -----")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar cantidad")
        print("4. Actualizar precio")
        print("5. Buscar producto por nombre")
        print("6. Mostrar todos los productos")
        print("7. Guardar inventario")
        print("8. Salir")

    # pide al usuario elegir una opcion
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id_producto = input("ID del producto: ")
            nombre = input("Nombre: ")
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))
            producto = Producto(id_producto, nombre, cantidad, precio)
            inventario.añadir_producto(producto)

        elif opcion == "2":
            id_producto = input("Ingrese el ID del producto a eliminar: ")
            inventario.eliminar_producto(id_producto)

        elif opcion == "3":
            id_producto = input("ID del producto a actualizar cantidad: ")
            cantidad = int(input("Nueva cantidad: "))
            inventario.actualizar_cantidad(id_producto, cantidad)

        elif opcion == "4":
            id_producto = input("ID del producto a actualizar precio: ")
            precio = float(input("Nuevo precio: "))
            inventario.actualizar_precio(id_producto, precio)

        elif opcion == "5":
            nombre = input("Nombre a buscar: ")
            inventario.buscar_por_nombre(nombre)

        elif opcion == "6":
            inventario.mostrar_todos()

        elif opcion == "7":
            inventario.guardar_en_archivo()

        elif opcion == "8":
            inventario.guardar_en_archivo()
            print("Saliendo del sistema. ¡Hasta pronto!")
            break

        else:
            print("Opción inválida. Intente de nuevo.")

# Ejecutar el programa

if __name__ == "__main__":
    menu()