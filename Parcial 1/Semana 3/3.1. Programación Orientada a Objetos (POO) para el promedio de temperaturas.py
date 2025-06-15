# Programa que calcula el promedio semanal de la temperatura diaria en un intervalo de 7 días utilizando la Programación Orientada a Objetos

# definimos una clase que representa información climática de los dias
class Dias_del_clima:
    def __init__(self, dia, temperatura):
        self._dia = dia # utilizamos un encapsulamiento con "_" para indicar que los valores estan protegidos o privados
        self._temperatura = temperatura #aqui guardamos la temperatura

#metodo publico que nos permite acceder a la temperatura fuera de la clase
    def temperatura_obtenida(self):
        return self._temperatura

# Aquí se muestra el dia y la temperatura en pantalla para observar los datos de cualquier dia
    def informacion(self):
        print(f"{self._dia}: {self._temperatura}°C")


# Agregamos una clase hija porque mantiene una herencia y es tambien polimorfismo
class Descripcion_delclima(Dias_del_clima):
    def __init__(self, dia, temperatura, descripcion):
        super().__init__(dia, temperatura) #Aqui llamamos a la clase padre para iniciar dia y temperatura
        self._descripcion = descripcion # le agregue como extra el comportamiento climatico como un sia lluvioso o soleado y aqui guardamos el texto de dicha implementación

    def informacion(self):
        print(f"{self._dia}: {self._temperatura}°C - {self._descripcion}") #mostramos, el dia , temperatura y comportamiento


# Creamos una clase que represente toda la semana con los dias y su clima respectivamente
class Clima_de_la_semana:
    def __init__(self):
        self._dias = [] #Creamos una lista que almacenara todos los objetos como el clima del día y su comportamiento

    def agregar_dia(self, clima_dia):
        self._dias.append(clima_dia) #Aqui se agrega un objeto como el dia y su clima a la lista de la semana

    def calcular_promedio(self):
        suma = sum(dia.temperatura_obtenida() for dia in self._dias)
        return suma / len(self._dias) #Aquí procedemos a calcular el promedio de las temperaturas

    def mostrar_dias(self):
        for dia in self._dias: #aqui recorremos la lista con su informacion de cada dia
            dia.informacion()


# Creamos una lista de los dias de la semana para que el programa se vea mas detallado respecto a la información
Dias_de_la_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

semana = Clima_de_la_semana() #se crea un objeto que lo usaremos para guardar los datos de todos los días
# Decoramos un poco la informacion del programa para diferenciar las instrucciones
print("°" * 46)
print("      PROMEDIO SEMANAL DE TEMPERATURA")

print("Utilizando la Programación Orientada a Objetos")
print("°" * 46)

#mostramos las instrucciones al usuario y le pedimos que ingrese los datos a calcular
print("Ingrese la temperatura y el comportamiento del clima (nublado,soleado,lluvioso,etc) para cada día:\n")
print()

#creamos un bucle que recorrera cada dia de la semana
for nombre in Dias_de_la_semana:
    while True:
        try:
            temp = float(input(f"Temperatura del día {nombre} (°C): "))
            break
        except ValueError:#utilize esta excepcion para validar que puedan ser numeros flutantes
            print("ingrese un número válido por favor .")# pero el texto no esta permitido y mostramos un error y el bucle volvera a comenzar
    descripcion = input(f"Comportamiento del clima para {nombre} : ") # A qui pedimos al usuario el comportamiento del clima como extra para una información más detallada
    semana.agregar_dia(Descripcion_delclima(nombre, temp, descripcion)) # este es un objeto que se agregara a la semana
    print("")

# Mostrar los datos ingresados
print("_" * 30)
print("\nResumen del clima esta semana:")# mostramos al usuario un resumen de los datos registrados
print("_" * 30)
semana.mostrar_dias()
print()

# Calcular y mostrar el promedio
promedio = semana.calcular_promedio()
print("_" * 52)
print(f"\nTemperatura promedio calculado de la semana: {promedio:.2f}°C") # Por ultimo devolvemos al usuario su promedio de la temperatura en la semana
print("_" * 52)