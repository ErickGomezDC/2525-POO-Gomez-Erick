# Programa que Calcula el área de un círculo
# El programa va a solicitar al usuario el radio de un círculo y calculara su área utilizando los diferentes tipos de datos float, int, string, boolean.

import math  # importa un modulo que contiene funciones que nos ayudaran a calcular pi

def calcular_area_del_circulo(radio: float) -> float:
    """Aquí agregamos una función para calcular el área de un círculo dado su radio."""
    area = math.pi * (radio ** 2)
    return area

def ingreso_de_numeros_validos(valor: str) -> bool:
    """Ingresamos una función que verifica si un valor ingresado es positivo y este posteriormente se convierta en booleano para devolver true si lo logro """
    try:
        numero = float(valor)
        return numero > 0
    # si el usuario ingresa un valor de tipo string o abc devolvera false
    except ValueError:
        return False


def main():
    """Ingresamos una función principal para la función total del programa con un título del programa"""
    print("=== Programa para calculador el área de un círculo ===")
    radio_valido = False #la variable booleana partira como false

    #Se pone un bucle que comprobara si el valor que se ingrese para el radio es un número válido
    while not radio_valido:
        entrada_del_usuario = input("Ingrese el radio del círculo: ")
        radio_valido = ingreso_de_numeros_validos(entrada_del_usuario)

        # si la entrada no es correcta se muestra un mensaje y vuelve a pedir un número correcto
        if not radio_valido:
            print(" Por favor, ingrese un número válido y positivo.")

    radio = float(entrada_del_usuario)
    area = calcular_area_del_circulo (radio)# llamamos a la funcion para obtener el área con el valor del radio

#Imprimimos el resultado del calculo realizado
    print(f"El área del círculo con radio {radio} que ingresaste es: {area:.2f} centímetros cuadrados .")

main()