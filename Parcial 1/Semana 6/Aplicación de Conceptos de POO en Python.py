# Programa que gestiona la información de los empleados, salarios y ventas realizadas en el día de una tienda de tecnologia

# Clase base general para todas las personas con nombre y edad
# Sirve para de base para añadir a otras clases como empleado, gerente y cliente
class persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre # este atributo es publico
        self.__edad = edad  # este atributo es privado o encapsulamiento

    def mostrar_informacion(self):
        #este metodo puede ser sobreescrito por las clases hijas o polimorfismo
        print(f"-Nombre: {self.nombre}, Edad: {self.__edad}")

#Las clases siguientes son heredadas de la clase persona, su clase padre
# Clase derivada: Gerente
class Gerente(persona):
    def __init__(self, nombre, edad):
        super().__init__(nombre, edad) #toma o hereda los atributos de la clase padre "persona"

    def mostrar_informacion(self):
        # se sobreescribe el metodo mostrar_informacion
        print(f"-Gerente: {self.nombre}")


# Clase derivada: Empleado
class Empleado(persona):
    def __init__(self, nombre, edad, salario):
        super().__init__(nombre, edad)
        self.__salario = salario #atributo privado o encapsulado

    def mostrar_informacion(self):
        # se sobreescribe el metodo mostrar_informacion pero con empleados
        print(f"-Empleado: {self.nombre}, Salario: ${self.__salario:.2f}")

    def obtener_salario(self):
        #Usamos el metodo para acceder al salario
        return self.__salario

    def aumentar_salario(self, nuevo_salario):
        #funcion que aumenta el salario por rendimiento de los empleados
        if nuevo_salario > self.__salario:
            self.__salario = nuevo_salario
            print(f"Salario de {self.nombre} aumentado a ${self.__salario:.2f}")
        else:
            print("Requisitos inválidos.No se realizaran cambios.")


# Clase derivada: Cliente Registrado
# Almacena una lista de compras hechas por los clientes
class ClienteRegistrado(persona):
    def __init__(self, nombre, edad):
        super().__init__(nombre, edad)
        self.compras = []  # Lista de tuplas por producto, precio y cantidad

    def agregar_compra(self, producto, precio, cantidad):
        #Aqui se agrega una compra al historial del cliente
        self.compras.append((producto, precio, cantidad))

    def mostrar_informacion(self):
        #Mostramos las compras del cliente
        print(f"\n-Cliente: {self.nombre}")
        if self.compras:
            print("Compras realizadas:")
            for producto, precio, cantidad in self.compras:
                total = precio * cantidad
                print(f"   - {cantidad}x {producto} a ${precio:.2f} = ${total:.2f}")
        else:
            print("No ha realizado compras.")

    def total_gastado(self):
        #se retorna al total gastado por el cliente
        return sum(precio * cantidad for _, precio, cantidad in self.compras)


# Función que ayuda a evaluar empleados y aumentar su salario
def evaluar_empleado(empleado, motivo="Buen desempeño"):
    print(f"\n Evaluación de {empleado.nombre}: {motivo}")
    nuevo_salario = empleado.obtener_salario() + 460
    empleado.aumentar_salario(nuevo_salario)


#creamos las personas que interactuaran con la tienda

# Creamos al gerente (instancia)
gerente1 = Gerente("Mario Delatorre", 45)

# Creamos a los empleados (instancias)

empleados = [
    Empleado("Carlos", 38, 1500.0),
    Empleado("Lucía", 29, 1700.0),
    Empleado("Sofía", 22, 800.0),
    Empleado("Evelyn", 24, 1000.0),
    Empleado("Renato", 27, 460.0)
]

# Creamos a los clientes (instancias)

clientes = [
    ClienteRegistrado("Luis", 34),
    ClienteRegistrado("Ana", 28),
    ClienteRegistrado("Santiago", 26),
    ClienteRegistrado("Emilia", 18),
    ClienteRegistrado("Sebastián", 22)
]

# Agregamos las compras respectivas hechas por los clientes

clientes[0].agregar_compra("Laptop Lenovo", 800.0, 1)
clientes[0].agregar_compra("Mouse Logitech", 25.0, 2)

clientes[1].agregar_compra("Impresora HP", 150.0, 1)
clientes[1].agregar_compra("Hojas de papel", 5.0, 10)

clientes[2].agregar_compra("Monitor ASUS", 500.0, 2)
clientes[2].agregar_compra("Gráfica RTX 5090", 4473.0, 1)

clientes[3].agregar_compra("Audífonos Sony", 400.0, 1)

clientes[4].agregar_compra("Laptop HP", 500.0, 1)
clientes[4].agregar_compra("Teclado 60%", 200.0, 1)
clientes[4].agregar_compra("Monitor Samsung", 150.0, 1)

# Mostramos la  información general
print(" Información del gerente y empleados:\n")
gerente1.mostrar_informacion()
for empleado in empleados:
    empleado.mostrar_informacion()

#Mostramos la informacion de los clientes
print("\n Información de clientes:")
for cliente in clientes:
    cliente.mostrar_informacion()

# Tambien para los salarios antes del aumento
print("\n Salarios actuales:")
for empleado in empleados[:5]:
    print(f"  {empleado.nombre}: ${empleado.obtener_salario():.2f}")

# La evaluación de los empleados por rendimiento
evaluar_empleado(empleados[0], "Cumplió metas trimestrales")
evaluar_empleado(empleados[1], "Buen trato al cliente")

# Agregue la informacion actualizada despues del aumento
print("\n Información tras evaluación:")
empleados[0].mostrar_informacion()
empleados[1].mostrar_informacion()

# También Agregue la información del resumen de compras para evaluación de marketing o cambios de estrategia
print("\n Resumen de clientes y compras:")
for cliente in clientes:
    cliente.mostrar_informacion()

# Y por ultimo añadi un recuento del total de dinero obtenido durante el dia laboral
total_ventas = sum(c.total_gastado() for c in clientes)
print(f"\n Total de clientes atendidos: {len(clientes)}")
print(f" Total recaudado en ventas del día: ${total_ventas:.2f}")
