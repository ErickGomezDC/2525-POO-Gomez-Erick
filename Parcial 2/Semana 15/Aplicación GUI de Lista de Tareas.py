#Aplicacion GUI en el uso de una lista de tareas en donde el usuario podra interactuar con el en forma de una agenda personal en donde se podra asignar tareas, fechas, horas, marcado de tareas pendientes y completadas

import tkinter as tk #libreria base para interfaces graficas
from tkinter import ttk, messagebox #mostrara mensajes emergentes
from tkcalendar import DateEntry # widget de calendario para elegir fechas
import json # guarda y carga archivos de las tareas existentes
import os
from datetime import datetime # manejo de fechas y horas actuales


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas")
        self.root.geometry("800x500")
        self.root.config(bg="#e0f7fa")

        # Archivo JSON
        self.file_name = "tareas.json" # nombre del archivo
        self.tasks = [] #lista de almacen para tareas en memoria
        self.load_tasks()

        # Entrada de nueva tarea
        frame_input = tk.Frame(self.root, bg="#e0f7fa")
        frame_input.pack(pady=10)

        tk.Label(frame_input, text="Nueva tarea:", bg="#e0f7fa").grid(row=0, column=0, padx=5)# muestra el texto "nueva tarea"
        self.entry_task = tk.Entry(frame_input, width=40) # campo de texto para escribir la tarea
        self.entry_task.grid(row=0, column=1, padx=5)
        self.entry_task.bind("<Return>", lambda event: self.add_task())# permite presionar enter para añadir la tarea

        tk.Label(frame_input, text="Fecha:", bg="#e0f7fa").grid(row=0, column=2, padx=5)
        self.date_entry = DateEntry(frame_input, width=12, background="darkblue",# calendario desplegable para elegir fecha
                                    foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd",)
        self.date_entry.grid(row=0, column=3, padx=5)

        # Campo para la hora
        tk.Label(frame_input, text="Hora:", bg="#e0f7fa").grid(row=0, column=4, padx=5)
        self.entry_time = tk.Entry(frame_input, width=10)
        self.entry_time.grid(row=0, column=5, padx=5)
        self.entry_time.insert(0, datetime.now().strftime("%H:%M"))  # Hora actual por defecto

        # Lista de tareas en Treeview
        columns = ("Tarea", "Fecha", "Hora", "Estado")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        # Definir estilos con tags
        self.tree.tag_configure("pendiente", background="#fff9c4")
        self.tree.tag_configure("completada", background="#c8e6c9")

        self.tree.bind("<Double-1>", lambda event: self.complete_task())

        # Botones
        frame_buttons = tk.Frame(self.root, bg="#e0f7fa")
        frame_buttons.pack(side="bottom", pady=10)

        btn_add = tk.Button(frame_buttons, text="Añadir Tarea", command=self.add_task, bg="#4fc3f7", fg="white")
        btn_add.grid(row=0, column=0, padx=10)

        btn_complete = tk.Button(frame_buttons, text="Marcar como Completada", command=self.complete_task, bg="#81c784")
        btn_complete.grid(row=0, column=1, padx=10)

        btn_delete = tk.Button(frame_buttons, text="Eliminar Tarea", command=self.delete_task, bg="#e57373")
        btn_delete.grid(row=0, column=2, padx=10)

        btn_exit = tk.Button(frame_buttons, text="Salir", command=self.root.quit, bg="#ffb74d")
        btn_exit.grid(row=0, column=3, padx=10)

        # Cargar tareas en la vista
        self.update_tree()

    def load_tasks(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r", encoding="utf-8") as f:
                self.tasks = json.load(f)

    def save_tasks(self):
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=4, ensure_ascii=False)

    def add_task(self):
        tarea = self.entry_task.get().strip()
        fecha = self.date_entry.get_date().strftime("%Y-%m-%d")
        hora = self.entry_time.get().strip()

        if tarea == "":
            messagebox.showwarning("Advertencia", "Debe ingresar una tarea.")
            return

        if hora == "":
            hora = datetime.now().strftime("%H:%M")

        nueva_tarea = {
            "tarea": tarea,
            "fecha": fecha,
            "hora": hora,
            "estado": "Pendiente"
        }
        self.tasks.append(nueva_tarea)
        self.save_tasks()
        self.update_tree()

        # Limpiar campos
        self.entry_task.delete(0, tk.END)
        self.entry_time.delete(0, tk.END)
        self.entry_time.insert(0, datetime.now().strftime("%H:%M"))

    #tarea completada
    def complete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una tarea para marcar como completada.")
            return

        index = self.tree.index(selected[0])
        self.tasks[index]["estado"] = "Completada"
        self.save_tasks()
        self.update_tree()

    #eliminar tarea
    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una tarea para eliminar.")
            return

        index = self.tree.index(selected[0])
        del self.tasks[index]
        self.save_tasks()
        self.update_tree()

    # Limpia todas las filas del Treeview.
    def update_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for task in self.tasks:
            estado = task["estado"]
            tag = "pendiente" if estado == "Pendiente" else "completada"
            self.tree.insert("", tk.END, values=(task["tarea"], task["fecha"], task["hora"], estado), tags=(tag,))


#ejecucion de la aplicacion creando una ventana principal

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop() # mantiene la ventana abierta hasta que el usuario la cierre
