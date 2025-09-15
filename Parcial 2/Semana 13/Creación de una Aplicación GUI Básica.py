"""
    Este es un programa que simula una interfaz grafica de usuario GUI en la cual utiliza la libreria tkinter
    en la cual le permite al usuario interactuar por medio de botones que le permiten
    agregar texto o informacion almacena datos visualmente
"""

import tkinter as tk # importa una biblioteca estandar para una interfaz grafica
from tkinter import messagebox # exporta un submodulo que exportara ventanas emergentes

#se ejecutara cuando el usuario pulse un boton
# Función para agregar datos a la lista
def agregar_dato():
   dato = entrada.get().strip() #obtiene el texto actual
   if dato:  # Verifica que no esté vacío
       lista.insert(tk.END, dato)
       entrada.delete(0, tk.END)  # Limpia el campo de texto
   else:
       messagebox.showwarning("Advertencia", "No puedes agregar un campo vacío.")

# Función para limpiar la lista
def limpiar_dato():
   seleccion = lista.curselection()
   if seleccion:
       lista.delete(seleccion[0])  # elimina solo el primer seleccionado
   else:
       lista.delete(0, tk.END)  # si no hay selección, borra toda la lista


# Crear ventana principal
ventana = tk.Tk()
ventana.title("Gestor de Datos Básico")
ventana.geometry("500x500")

# Instruccion inicial
Instruccion = tk.Label(ventana, text="Ingrese un dato:", font=("Arial", 12))
Instruccion.pack(pady=5)

# Campo de texto
entrada = tk.Entry(ventana, width=30)
entrada.pack(pady=5)

# Botones
boton_agregar = tk.Button(ventana, text="Agregar", command=agregar_dato, bg="lightgreen")
boton_agregar.pack(pady=5)

boton_limpiar = tk.Button(ventana, text="Limpiar", command=limpiar_dato, bg="lightcoral")
boton_limpiar.pack(pady=5)

# Lista para mostrar varias lineas de datos
lista = tk.Listbox(ventana, width=40, height=10)
lista.pack(pady=10)

# Ejecuta la aplicación
ventana.mainloop()
