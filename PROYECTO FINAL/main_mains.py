import tkinter as tk
from tkinter import messagebox
import subprocess
import tkinter.font as tkfont

def Admin_Ventas():
    ventana.destroy()
    subprocess.run(['python', 'Algoritmos\main_algoritmos.py'])

def Resolucion_ecuaciones():
    ventana.destroy()
    subprocess.run(['python', 'Algebra\ecuaciones_lineales.py'])

def Mate_2():
    ventana.destroy()
    subprocess.run(['python', 'mate_discreta\main_mate.py'])

# --- Función para salir con confirmación ---
def salir():
    if messagebox.askyesno("Salir", "¿Seguro que quieres salir?"):
        ventana.destroy()

# --- Ventana principal ---
ventana = tk.Tk()
ventana.title("PROYECTOS FINALES")
ventana.state('zoomed')
ventana.configure(bg="#e0f2f1")  # Fondo suave

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
    text="PROYECTOS FINALES",
    font=titulo_font,
    bg="#e0f2f1",
    fg="#00695c"
)
titulo.grid(row=0, column=0, columnspan=5, pady=(40, 30))

# --- Función para crear botones bonitos ---
def crear_boton(master, text, command):
    boton = tk.Button(
        master,
        text=text,
        font=btn_font,
        bg="#00897b",
        fg="white",
        activebackground="#26a69a",
        activeforeground="white",
        width=40,
        height=2,
        bd=0,
        relief="ridge",
        command=command,
        cursor="hand2"
    )
    boton.bind("<Enter>", lambda e: boton.config(bg="#26a69a"))
    boton.bind("<Leave>", lambda e: boton.config(bg="#00897b"))
    return boton

# --- Botones principales ---
btn1 = crear_boton(ventana, "Administrador de ventas", Admin_Ventas)
btn1.grid(row=2, column=0, columnspan=5, pady=15)

btn2 = crear_boton(ventana, "Resolución de ecuaciones algebraicas", Resolucion_ecuaciones)
btn2.grid(row=3, column=0, columnspan=5, pady=15)

btn3 = crear_boton(ventana, "Operaciones de matemática 2", Mate_2)
btn3.grid(row=4, column=0, columnspan=5, pady=15)

# --- Botón de salir ---
btn_salir = crear_boton(ventana, "SALIR", salir)
btn_salir.grid(row=7, column=0, columnspan=5, pady=30)

ventana.mainloop()
