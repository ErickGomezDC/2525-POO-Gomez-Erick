# Aplicación GUI utilizando Tkinter en python para crear una agenda personal interactiva permitiendo al usuario ver, agregar y eliminar eventos o tareas segun requiera el usuario

"""
Caracteristicas del programa
Agenda personal en Tkinter
 - interactivo con el usuario
 - capaz de agregar fecha, hora y descripción
 - Mantiene entradas (Entry) para interactuar con el uso de la fecha, hora y descripciones
 - Estas funcionan a base de botones para agregar, eliminar y salir
 - Mantiene un calendario por default para moverse entre fechas de forma más sencillas
 - Marca por default la fecha y hora actual para mayor eficiencia al agregar información
 - Mantiene Etiquetas para todos los campos y botones
 - Dialogo para confirmación de eliminación para eventos
"""

import tkinter as tk #libreria base para interfaces graficas
from tkinter import ttk # widgets para freme, treeview, botonoes, etc
from tkinter import messagebox #mostrara mensajes emergentes
from datetime import datetime #maneja fecha y hora
import calendar # para crear calendarios

try:
    from tkcalendar import DateEntry # se importara un widget de un calendario
    TKCALENDAR_AVAILABLE = True
except Exception:
    TKCALENDAR_AVAILABLE = False


class SimpleCalendarDialog(tk.Toplevel): # crea una ventana aparte de la principal
    def __init__(self, parent, initial_date=None):
        super().__init__(parent) #inicializa la ventana
        self.title("Seleccionar fecha")# nombre de la ventana
        self.resizable(False, False)# no se podra cambiar de tamaño
        self.grab_set()# bloquea interaccion con la ventana principal hasta cerrarla
        self.selected_date = None # guarda la fecha elegida

        # Si el usuario no pone una fecha inicial, por defecto se agregara la de que esta en ese momento
        today = datetime.today()
        self.year = (initial_date.year if initial_date else today.year)
        self.month = (initial_date.month if initial_date else today.month)

        nav_frame = ttk.Frame(self)
        nav_frame.pack(padx=10, pady=(10, 0))
        self.body = ttk.Frame(self)
        self.body.pack(padx=10, pady=10)

        # Aqui se creara un calendario de botones con dias y permite navegar entre meses
        prev_btn = ttk.Button(nav_frame, text="<", width=3, command=self.prev_month)
        prev_btn.grid(row=0, column=0)
        self.month_label = ttk.Label(nav_frame, text="")
        self.month_label.grid(row=0, column=1, padx=8)
        next_btn = ttk.Button(nav_frame, text=">", width=3, command=self.next_month)
        next_btn.grid(row=0, column=2)

        self._draw_calendar()

    def _draw_calendar(self):
        for w in self.body.winfo_children():
            w.destroy()

        self.month_label.config(text=f"{calendar.month_name[self.month]} {self.year}")

        days = ['Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa', 'Do']
        for idx, d in enumerate(days):
            ttk.Label(self.body, text=d).grid(row=0, column=idx, padx=4, pady=2)

        cal = calendar.Calendar(firstweekday=0)
        monthdays = cal.monthdayscalendar(self.year, self.month)

        for r, week in enumerate(monthdays, start=1):
            for c, day in enumerate(week):
                if day == 0:
                    ttk.Label(self.body, text='').grid(row=r, column=c, padx=4, pady=2)
                else:
                    b = ttk.Button(self.body, text=str(day), width=3,
                                   command=lambda d=day: self._select_day(d))
                    b.grid(row=r, column=c, padx=2, pady=2)

    def _select_day(self, day):
        self.selected_date = datetime(self.year, self.month, day)
        self.grab_release()
        self.destroy()

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self._draw_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self._draw_calendar()


class AgendaApp(tk.Tk): # crea la ventana principal
    def __init__(self):
        super().__init__()
        self.title("Agenda Personal")
        self.geometry("720x560") # tamaño inicial de la ventana

        # Frame superior: lista de eventos
        self.top_frame = ttk.Frame(self, padding=10)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Frame inferior: entradas y botones
        self.bottom_frame = ttk.Frame(self, padding=10)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self._build_event_list(self.top_frame)
        self._build_entry_panel(self.bottom_frame)

    # crea una etiqueta encima de la lista
    def _build_event_list(self, parent):
        header = ttk.Label(parent, text="Eventos programados")
        header.pack(anchor='w')

        #muestra los eventos en forma de tabla con columnas
        columns = ("fecha", "hora", "descripcion")
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', selectmode='browse')
        self.tree.heading('fecha', text='Fecha')
        self.tree.heading('hora', text='Hora')
        self.tree.heading('descripcion', text='Descripción')

        #nombre de las columnas
        self.tree.column('fecha', width=100, anchor='center')
        self.tree.column('hora', width=80, anchor='center')
        self.tree.column('descripcion', width=500, anchor='w')

        # añade un scrollbar vertical
        vsb = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y, in_=parent)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def _build_entry_panel(self, parent):
        entry_frame = ttk.Frame(parent)
        entry_frame.pack(fill=tk.X, pady=(0, 10))

        # toma la fecha y hora actual como valores por defect
        now = datetime.now()


        ttk.Label(entry_frame, text="Fecha:").grid(row=0, column=0, sticky='w')
        if TKCALENDAR_AVAILABLE:
            self.date_entry = DateEntry(entry_frame, date_pattern='yyyy-mm-dd') #Se usa un selector de calendario moderno
            self.date_entry.set_date(now.date())
            self.date_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        else:
            self.date_var = tk.StringVar(value=now.strftime('%Y-%m-%d'))
            self.date_entry = ttk.Entry(entry_frame, textvariable=self.date_var) #Usa un campo de texto simple con la fecha de hoy
            self.date_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=2)
            cal_btn = ttk.Button(entry_frame, text="📅", width=3, command=self.open_simple_calendar)
            cal_btn.grid(row=0, column=2, padx=2)

        ttk.Label(entry_frame, text="Hora (HH:MM):").grid(row=1, column=0, sticky='w')
        self.time_var = tk.StringVar(value=now.strftime('%H:%M'))
        self.time_entry = ttk.Entry(entry_frame, textvariable=self.time_var)
        self.time_entry.grid(row=1, column=1, columnspan=2, sticky='ew', padx=5, pady=2)

        ttk.Label(entry_frame, text="Descripción:").grid(row=2, column=0, sticky='nw')
        self.desc_text = tk.Text(entry_frame, height=3, width=40, wrap='word')
        self.desc_text.grid(row=2, column=1, columnspan=3, sticky='ew', padx=5, pady=2)

        entry_frame.columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X)

        add_btn = ttk.Button(btn_frame, text="Agregar Evento", command=self.add_event)
        add_btn.pack(side=tk.LEFT, padx=5, pady=5)

        del_btn = ttk.Button(btn_frame, text="Eliminar Evento Seleccionado", command=self.delete_seleccion_evento)
        del_btn.pack(side=tk.LEFT, padx=5, pady=5)

        exit_btn = ttk.Button(btn_frame, text="Salir", command=self.on_exit)
        exit_btn.pack(side=tk.RIGHT, padx=5, pady=5)

    def open_simple_calendar(self):
        initial = None
        cur = self.date_var.get().strip()
        try:
            initial = datetime.strptime(cur, "%Y-%m-%d")
        except Exception:
            initial = datetime.today()

        dlg = SimpleCalendarDialog(self, initial_date=initial)
        self.wait_window(dlg)
        if getattr(dlg, 'selected_date', None):
            self.date_var.set(dlg.selected_date.strftime('%Y-%m-%d'))

    def add_event(self):
        if TKCALENDAR_AVAILABLE:
            fecha = self.date_entry.get_date().strftime('%Y-%m-%d')
        else:
            fecha = self.date_var.get().strip()

        hora = self.time_var.get().strip()
        descripcion = self.desc_text.get('1.0', tk.END).strip()

        if not descripcion:
            messagebox.showwarning("Campo faltante", "Por favor ingrese una descripción.")
            return

        try:
            datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Formato incorrecto", "La fecha debe tener formato YYYY-MM-DD.")
            return

        try:
            datetime.strptime(hora, '%H:%M')
        except ValueError:
            messagebox.showerror("Formato incorrecto", "La hora debe tener formato HH:MM (24h).")
            return

        self.tree.insert('', tk.END, values=(fecha, hora, descripcion))

        now = datetime.now()
        if TKCALENDAR_AVAILABLE:
            self.date_entry.set_date(now.date())
        else:
            self.date_var.set(now.strftime('%Y-%m-%d'))
        self.time_var.set(now.strftime('%H:%M'))
        self.desc_text.delete('1.0', tk.END)

    def delete_seleccion_evento(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Nada seleccionado", "Seleccione un evento para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar el evento seleccionado?")
        if not confirm:
            return

        for item in sel:
            self.tree.delete(item)

    # Pregunta antes de cerrar la aplicación
    def on_exit(self):
        if messagebox.askokcancel("Salir", "¿Desea salir de la aplicación?"):
            self.destroy()

# Crea una instancia de la app y arranca el bucle principal (mainloop) para que la ventana quede abierta
if __name__ == '__main__':
    app = AgendaApp()
    app.mainloop()