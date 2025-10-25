import tkinter as tk
from tkinter import messagebox
import subprocess
import tkinter.font as tkfont

# --- Funciones de los botones ---
def Control_inventario():
    ventana.destroy()
    subprocess.run(['python', 'Algoritmos/funciones/control_inventario.py'])

def Control_clientes():
    ventana.destroy()
    subprocess.run(['python', 'Algoritmos/funciones/control_clientes.py'])

def Control_ventas():
    ventana.destroy()
    subprocess.run(['python', 'Algoritmos/funciones/control_de_ventas.py'])

def Reportes_basicos():
    ventana.destroy()
    subprocess.run(['python', 'Algoritmos/funciones/reportes_ventas.py'])

# --- Función para salir con confirmación ---
def salir():
    if messagebox.askyesno("Salir", "¿Seguro que quieres salir al menú principal?"):
        ventana.destroy()
        subprocess.run(['python', 'main_mains.py'])

# --- Ventana principal ---
ventana = tk.Tk()
ventana.title("PROYYECTO MATEMÁTICA DISCRETA")
ventana.state('zoomed')
ventana.configure(bg="#ffffff")  # Fondo suave

# --- Fuente ---
titulo_font = tkfont.Font(family="Helvetica", size=36, weight="bold")
btn_font = tkfont.Font(family="Helvetica", size=16, weight="bold")

# --- Grid flexible ---
for i in range(5):
    ventana.columnconfigure(i, weight=1)
for i in range(8):  # más filas para el botón de salir
    ventana.rowconfigure(i, weight=1)

# --- Título ---
titulo = tk.Label(
    ventana,
    text="PROYECTO ALGORITMOS",
    font=titulo_font,
    bg="#ffffff",
    fg="#000000"
)
titulo.grid(row=0, column=0, columnspan=5, pady=(40, 30))

# --- Función para crear botones bonitos ---
def crear_boton(master, text, command):
    boton = tk.Button(
        master,
        text=text,
        font=btn_font,
        bg="#ffffff",
        fg="black",
        activebackground="#ffffff",
        activeforeground="black",
        width=40,
        height=2,
        bd=3,             # Aumentamos el grosor del borde
        relief="ridge",   # Tipo de borde visible
        command=command,
        cursor="hand2"
    )
    boton.bind("<Enter>", lambda e: boton.config(bg="#ffffff"))
    boton.bind("<Leave>", lambda e: boton.config(bg="#ffffff"))
    return boton


# --- Botones principales ---
btn1 = crear_boton(ventana, "Control de inventario", Control_inventario)
btn1.grid(row=2, column=0, columnspan=5, pady=15)

btn2 = crear_boton(ventana, "Administración de clientes", Control_clientes)
btn2.grid(row=3, column=0, columnspan=5, pady=15)

btn3 = crear_boton(ventana, "Control de ventas", Control_ventas)
btn3.grid(row=4, column=0, columnspan=5, pady=15)

btn4 = crear_boton(ventana, "Reportes básicos", Reportes_basicos)
btn4.grid(row=6, column=0, columnspan=5, pady=15)

# --- Botón de salir ---
btn_salir = crear_boton(ventana, "SALIR", salir)
btn_salir.grid(row=7, column=0, columnspan=5, pady=30)

ventana.mainloop()