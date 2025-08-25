# Sistema que gestiona un inventario sobre el inventario de una tienda en donde nos permitirá añadir, actualizar, eliminar y buscar productos utilizando estructura de datos personalizada.

    #Agregamos la clase producto que representara los artículos del inventario
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto # agregamos los atributos de los artículos que el constructor inicializara
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Asignamos getters que accederan al valor atributo
    def get_id(self):
        return self.id_producto

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.precio

    # Agregamos setters que modificaran los atributos nombre, cantidad y precio
    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    def set_precio(self, precio):
        self.precio = precio

    # este metodo asignado definira como se mostrara el producto al imprimirlo
    def __str__(self):
        return f"ID: {self.id_producto}, Nombre: {self.nombre}, Cantidad: {self.cantidad}, Precio: {self.precio:.2f}"

# creamos la clase inventario
#asignamos una lista vacia que almacenara los productos
class Inventario:
    def __init__(self):
        self.productos = []

        # agregamos un metodo que verificara el ID
    def añadir_producto(self, producto):
        # Validar ID único
        for p in self.productos:
            if p.get_id() == producto.get_id():
                print(" Error: El ID ingresado pertenece a un producto ya existente.")
                return
        self.productos.append(producto)
        print(" El producto agregado exitosamente.")

        #metodo que eliminara un producto en base a su ID
    def eliminar_producto(self, id_producto):
        for p in self.productos:
            if p.get_id() == id_producto:
                self.productos.remove(p)
                print("Producto fue eliminado correctamente.")
                return
        print("No se pudo encontrar ese producto.")

        #Actualiza la cantidad y/o el precio de un producto segun el ID
    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        for p in self.productos:
            if p.get_id() == id_producto:
                if nueva_cantidad is not None:
                    p.set_cantidad(nueva_cantidad)
                if nuevo_precio is not None:
                    p.set_precio(nuevo_precio)
                print(" El producto se actualizo correctamente.")
                return
        print(" Producto no encontrado.")

        #Buscara los productos por nombre parcial o completo
    def buscar_producto(self, nombre):
        resultados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        if resultados:
            print(" Resultados encontrados:")
            for p in resultados:
                print(p)
        else:
            print("El nombre ingresado no encontró resultados.")

        #Mostrara todos los productos guardados en el inventario
    def mostrar_productos(self):
        if not self.productos:
            print("El inventario está vacío.")
        else:
            print(" Productos del inventario:")
            for p in self.productos:
                print(p)


# Creamos un inventario vacio
def menu():
    inventario = Inventario()
    # Aqui imprimiremos un menu en bucle infinito que se asignara los productos hasta que termine su proceso y se cierre el menu
    while True:
        print("\n--- MENÚ DE LA GESTIÓN DE INVENTARIO ---")
        print("1. Añadir nuevo producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar cantidad o precio de un producto por ID")
        print("4. Buscar producto(s) por nombre")
        print("5. Mostrar todos los productos en el inventario")
        print("6. Cerrar menu")

        # Asignado que dejara al usuario elegir una opcion del 1 al 6
        opcion = input("Seleccione una opción: ")

       # Agregamos los datos que se pediran para crear un producto y añadirlo al inventario
        if opcion == "1":
            try:
                id_producto = input("Ingrese ID único del producto: ")
                nombre = input("Ingrese nombre del producto: ")
                cantidad = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
                producto = Producto(id_producto, nombre, cantidad, precio)
                inventario.añadir_producto(producto)
            except ValueError:
                print(" Error: cantidad y precio deben ser digitados correctamente.")

       # Aqui la opcion 2 eliminara un producto en base al ID
        elif opcion == "2":
            id_producto = input("Ingrese el ID del producto que desea eliminar: ")
            inventario.eliminar_producto(id_producto)

        # Aqui la opcion 3 Actualizara el producto en donde tambien se puede cambiar su precio
        elif opcion == "3":
            id_producto = input("Ingrese el ID del producto que desea actualizar: ")
            try:
                cantidad = input("Ingrese una nueva cantidad (deje en blanco si no hay actualización): ")
                precio = input("Ingrese un nuevo precio (deje en blanco si no hay actualización): ")

                nueva_cantidad = int(cantidad) if cantidad else None
                nuevo_precio = float(precio) if precio else None

                inventario.actualizar_producto(id_producto, nueva_cantidad, nuevo_precio)
            except ValueError:
                print(" Error: los valores no son correctos.")

        # Aqui la opcion 4 buscara el nombre que se encuentre en el inventario
        elif opcion == "4":
            nombre = input("Ingrese el nombre que quiere buscar: ")
            inventario.buscar_producto(nombre)

        # Aqui la opcion 5 mostrara lo que se encuentre agregado al inventario
        elif opcion == "5":
            inventario.mostrar_productos()

        # Aqui la opcion 6 cerrara el menu y finalizara el programa
        elif opcion == "6":
            print(" sistema cerrado correctamente...")
            break

        else:
            print("Ocurrio un error imprevisto, intente de nuevo.")


# Ejecuta el programa
if __name__ == "__main__":
    menu()
