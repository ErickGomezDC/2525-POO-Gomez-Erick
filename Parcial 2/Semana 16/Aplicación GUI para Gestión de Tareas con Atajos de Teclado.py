#Aplicacion GUI para la gestion de tareas usando los atajos del teclado usando (enter) para agregar tarea, (C) para completar, (D) para eliminar y (Esc) para salir

import tkinter as tk #libreria base para interfaces graficas
from tkinter import ttk, messagebox #mostrara mensajes emergentes
from tkcalendar import DateEntry # widget de calendario para elegir fechas
import json # guarda y carga archivos de las tareas existentes
import os
from datetime import datetime # manejo de fechas y horas actuales

#Define una clase llamada ToDoApp que contiene toda la lógica y la interfaz.
class ToDoApp:
    def __init__(self, root):# se ejecuta automáticamente al crear el objeto
        self.root = root
        self.root.title("Gestión de Tareas con Atajos")#Se guardan las propiedades de la ventana principal
        self.root.geometry("850x550")
        self.root.config(bg="#e0f7fa")

        #Archivo de almacenamiento
        self.file_name = "tareas.json"
        self.tareas = self.load_tasks()

        #Crea un contenedor para agrupar los widgets de entrada (tarea, fecha, hora).
        frame_input = tk.Frame(self.root, bg="#e0f7fa")
        frame_input.pack(pady=10)

        #Crea una etiqueta, una caja de texto (Entry) y un evento para que al presionar Enter se agregue la tarea.
        tk.Label(frame_input, text="Tarea:", bg="#e0f7fa").grid(row=0, column=0, padx=5)
        self.entry_tarea = tk.Entry(frame_input, width=40)
        self.entry_tarea.grid(row=0, column=1, padx=5)
        self.entry_tarea.bind("<Return>", lambda e: self.agregar_tarea())

        #Selector de fecha
        tk.Label(frame_input, text="Fecha:", bg="#e0f7fa").grid(row=0, column=2, padx=5) # Muestra un calendario desplegable para elegir la fecha de la tarea.
        self.entry_fecha = DateEntry(
            frame_input, width=12, background="darkblue",
            foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd"
        )
        self.entry_fecha.grid(row=0, column=3, padx=5)

        #Selector de hora
        tk.Label(frame_input, text="Hora:", bg="#e0f7fa").grid(row=0, column=4, padx=5)
        hora_actual = datetime.now()
        self.hora_var = tk.StringVar(value=f"{hora_actual.hour:02d}")
        self.minuto_var = tk.StringVar(value=f"{hora_actual.minute:02d}")

        #Obtiene la hora actual y la muestra como valor inicial
        self.spin_hora = tk.Spinbox(frame_input, from_=0, to=23, width=3, textvariable=self.hora_var, format="%02.0f")
        self.spin_hora.grid(row=0, column=5)
        tk.Label(frame_input, text=":", bg="#e0f7fa").grid(row=0, column=6)
        self.spin_minuto = tk.Spinbox(frame_input, from_=0, to=59, width=3, textvariable=self.minuto_var, format="%02.0f")
        self.spin_minuto.grid(row=0, column=7)

        #Tabla (Treeview) para mostrar tareas
        columns = ("Tarea", "Fecha", "Hora", "Estado")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=16)
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

        #Crea una tabla con 4 columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        #Asigna títulos a las columnas y centra el texto
        self.tree.column("Tarea", width=380)
        self.tree.column("Fecha", width=120)
        self.tree.column("Hora", width=80)
        self.tree.column("Estado", width=120)

        #Colorea las filas según el estado (pendiente = amarillo, completada = verde)
        self.tree.tag_configure("pendiente", background="#fff9c4")
        self.tree.tag_configure("completada", background="#c8e6c9")

        #Para doble clic marca tarea completada
        self.tree.bind("<Double-1>", lambda e: self.completar_tarea())

        # Botones
        frame_buttons = tk.Frame(self.root, bg="#e0f7fa")
        frame_buttons.pack(pady=10)

        style = {
            "font": ("Arial", 10, "bold"),
            "width": 15,
            "height": 2,
            "relief": "raised",
            "bd": 2
        }

        self.btn_agregar = tk.Button(frame_buttons, text="Agregar (Enter)", bg="#aed581", activebackground="#9ccc65",
                                     command=self.agregar_tarea, **style)
        self.btn_agregar.grid(row=0, column=0, padx=8)

        self.btn_completar = tk.Button(frame_buttons, text="Completar (C)", bg="#64b5f6", activebackground="#42a5f5",
                                       command=self.completar_tarea, **style)
        self.btn_completar.grid(row=0, column=1, padx=8)

        self.btn_eliminar = tk.Button(frame_buttons, text="Eliminar (D / Supr)", bg="#e57373", activebackground="#ef5350",
                                      command=self.eliminar_tarea, **style)
        self.btn_eliminar.grid(row=0, column=2, padx=8)

        self.btn_salir = tk.Button(frame_buttons, text="Salir (Esc)", bg="#ffb74d", activebackground="#ffa726",
                                   command=self.root.quit, **style)
        self.btn_salir.grid(row=0, column=3, padx=8)

        # Atajos de teclado
        self.root.bind("<c>", self.key_completar)
        self.root.bind("<C>", self.key_completar)
        self.root.bind("<d>", self.key_eliminar)
        self.root.bind("<D>", self.key_eliminar)
        self.root.bind("<Delete>", self.key_eliminar)
        self.root.bind("<Escape>", lambda e: self.root.quit())

        self.update_tree()

    # Carga de tareas
    def load_tasks(self):
        if not os.path.exists(self.file_name):
            return []
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            return []

        tareas = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    tareas.append({
                        "tarea": item.get("tarea", ""),
                        "fecha": item.get("fecha", datetime.now().strftime("%Y-%m-%d")),
                        "hora": item.get("hora", datetime.now().strftime("%H:%M")),
                        "estado": item.get("estado", "Pendiente")
                    })
        return tareas

    # Guardado de tareas
    def save_tasks(self):
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(self.tareas, f, indent=4, ensure_ascii=False)


    def update_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for tarea in self.tareas:
            estado = tarea.get("estado", "Pendiente")
            tag = "pendiente" if estado == "Pendiente" else "completada"
            self.tree.insert("", tk.END, values=(tarea["tarea"], tarea["fecha"], tarea["hora"], estado), tags=(tag,))

    #Agrega una nueva tarea
    def agregar_tarea(self):
        tarea = self.entry_tarea.get().strip()
        fecha = self.entry_fecha.get_date().strftime("%Y-%m-%d")
        hora = f"{int(self.hora_var.get()):02d}:{int(self.minuto_var.get()):02d}"

        if tarea == "":
            messagebox.showwarning("Atención", "Debes escribir una tarea.")
            return

        self.tareas.append({
            "tarea": tarea,
            "fecha": fecha,
            "hora": hora,
            "estado": "Pendiente"
        })
        self.save_tasks()
        self.update_tree()
        self.entry_tarea.delete(0, tk.END)

    #Marcar tarea como completada
    def completar_tarea(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona una tarea para marcar como completada.")
            return
        index = self.tree.index(sel[0])
        self.tareas[index]["estado"] = "Completada"
        self.save_tasks()
        self.update_tree()

    #Eliminar una tarea
    def eliminar_tarea(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona una tarea para eliminar.")
            return
        index = self.tree.index(sel[0])
        del self.tareas[index]
        self.save_tasks()
        self.update_tree()


    def key_completar(self, event):
        if self.root.focus_get() == self.entry_tarea:
            return
        self.completar_tarea()

    def key_eliminar(self, event):
        if self.root.focus_get() == self.entry_tarea:
            return
        self.eliminar_tarea()

# Inicio del programa
if __name__ == "__main__": # Crea la ventana principal e inicializa la clase y se mantiene abierta
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
