# Programa que calcula el promedio semanal de la temperatura diaria en un intervalo de 7 días utilizando programación tradicional

#Creamos la función para la entrada de las temperaturas diarias que nos la proporcionara el usuario
def temperaturas_diarias():
    temperaturas = [] # guardaremos aquí los datos de la temperatura durante 7 días
    for i in range(7): # dentro de un rango de 7 días
        temp = float(input(f"Ingrese su temperatura para el día {i + 1}: ")) #solicitamos que ingrese el usuario la temperatura
        temperaturas.append(temp) # utilizamos append para los elementos a la lista
    return temperaturas


# Aquí calcularemos el promedio de las temperaturas diarias
def promedios(temperaturas):
    return sum(temperaturas) / len(temperaturas) #aqui se calcula y se devuelve el promedio

# Función principal donde se coordina el proceso total
def main():
    print("_" * 38)
    print("   PROMEDIO SEMANAL DE TEMPERATURA ")
    print("Utilizando la Programación Tradicional")
    print("_" * 38)
    temperaturas = temperaturas_diarias()
    promedio = promedios(temperaturas) #llamamos a la función para pedir los datos y guardar el resultado
    print("_" * 66)
    print(f"El promedio calculado de la temperatura en esta semana es: {promedio:.2f}°C")
    print("_" * 66)


# función utilizada para ejecutar el programa en su totalidad
main()