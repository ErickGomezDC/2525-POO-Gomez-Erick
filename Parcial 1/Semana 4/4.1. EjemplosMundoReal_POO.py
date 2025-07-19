#Programa que modela una tienda de helado que utiliza la Programación Orientada a Objetos

# Creamos una clase que representa un sabor de helado
class Sabor:
    def __init__(self, nombre, precio_por_bola, stock_bolas): #hacemos una función en donde se ejecutara al crear un nuevo sabor de helado con su respectivo precio y stock
        self.nombre = nombre
        self.precio_por_bola = precio_por_bola
        self.stock_bolas_helado = stock_bolas

    def mostrar_info(self): # aqui imprimimos el nombre del sabor y cuantas bolas de helado quedan en stock
        print(f"Sabor: {self.nombre} - Precio por bola de helado: ${self.precio_por_bola} - Stock: {self.stock_bolas_helado} bolas")

    def reducir_stock(self, cantidad): #se usara para reducir su cantidad cuando cada cliente compre helado
        if self.stock_bolas_helado >= cantidad:# verificara las bolas de helado disponibles
            self.stock_bolas_helado -= cantidad# si todavia estan en stock entonces restara su cantidad
            return True
        else:
            print(f"Ya no nos queda helado de {self.nombre}. Solo quedan {self.stock_bolas_helado} bolas.")# si no existe suficiente stock saltara un mensaje fuera de stock
            return False

# Creamos una clase para crear un cliente
class Cliente:
    def __init__(self, nombre):#guardamos el nombre del cliente
        self.nombre = nombre

    def mostrar_info(self):#mostramos el nombre del cliente que esta comprando
        print(f"Cliente: {self.nombre}")

# Ahora creamos una clase de tienda de helados
class TiendaHelados:
    def __init__(self, nombre):
        self.nombre = nombre#agregue un diccionario que almacenara los sabores
        self.sabores = {}

    def agregar_sabor(self, sabor):
        self.sabores[sabor.nombre] = sabor# aqui se agregara los sabores al diccionario usando sus nombres clave

    def mostrar_sabores(self):
        print(f"\nSabores disponibles en la {self.nombre}:")#mostraremos todos los sabores disponibles de cada objeto
        for sabor in self.sabores.values():
            sabor.mostrar_info()

    def vender_helado(self, cliente, sabor_nombre, cantidad_bolas):#agregamos un metodo para la venta del helado al cliente
        print(f"\n{cliente.nombre} quiere comprar {cantidad_bolas} bolas de {sabor_nombre}.")#imprimimos la intención de la compra del cliente

        if sabor_nombre in self.sabores: # agregamos una función donde verificara si el sabor existe en la tienda
            sabor = self.sabores[sabor_nombre]#verifica si el nombre existe
            if sabor.reducir_stock(cantidad_bolas):#obtiene el objeto sabor desde el diccionario
                total = sabor.precio_por_bola * cantidad_bolas
                print(f"Son: ${total} deniques gracias por su compra disfrute su dia")# si queda stock aqui se calculara el precio total y un mensaje de compra
            else:
                print("Lo sentimos se nos agoto o son muchas bolas de helado de ese sabor vuelve mas tarde.")# si no hay stock suficiente le hacemos saber que se termino
        else:
            print(f"El helado de '{sabor_nombre}' no lo disponemos en nuestra tienda lo sentimos.") # si el helado que se registro no existe reflejamos un mensaje

# creamos el programa principal
if __name__ == "__main__":
    # Agregamos una tienda en este caso la voy a inspirar en un videojuego
    tienda = TiendaHelados("Heladería Nueva Eridu")

    #Agregamos los sabores
    sabor1 = Sabor("Chocolate", 1.50, 20)
    sabor2 = Sabor("Vainilla", 1.30, 15)
    sabor3 = Sabor("Fresa", 1.40, 10)

    # Agregamos los sabores al inventario de la tienda
    tienda.agregar_sabor(sabor1)
    tienda.agregar_sabor(sabor2)
    tienda.agregar_sabor(sabor3)

    # Mostramos los sabores disponibles
    tienda.mostrar_sabores()

    # Agregamos los clientes
    cliente1 = Cliente("Hoshimi Miyabi")
    cliente2 = Cliente("Billy Kid")
    cliente3 = Cliente("Tsukishiro Yanagi")
    cliente4 = Cliente("Ellen Joe")

    # lo que compran los clientes
    tienda.vender_helado(cliente1, "Chocolate", 3)
    tienda.vender_helado(cliente2, "Vainilla", 16)  # Prueba de stock insuficiente
    tienda.vender_helado(cliente3, "Fresa", 4)
    tienda.vender_helado(cliente4, "Hielo", 2) # Prueba de sabor inexistente

    # Mostramos los sabores que quedan restantes
    tienda.mostrar_sabores()