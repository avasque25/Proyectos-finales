import tkinter as tk
from tkinter import messagebox
import subprocess
import tkinter.font as tkfont

# --- Funciones de los botones ---
def Recorrido_arboles():
    ventana.destroy()
    subprocess.run(['python', 'Mate_discreta/MCD.py'])

def Comb_per():
    ventana.destroy()
    subprocess.run(['python', 'Mate_discreta/Comb_perm.py'])

def Teo_conjuntos():
    ventana.destroy()
    subprocess.run(['python', 'Mate_discreta/conjunto.py'])

# --- Función para salir con confirmación ---
def salir():
    if messagebox.askyesno("Salir", "¿Seguro que quieres salir al menú principal?"):
        ventana.destroy()
        subprocess.run(['python', 'main_mains.py'])

# --- Ventana principal ---
ventana = tk.Tk()
ventana.state('zoomed')
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
    text="PROYECTO FINAL",
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
btn1 = crear_boton(ventana, "Maximo Comun Divisor", Recorrido_arboles)
btn1.grid(row=2, column=0, columnspan=5, pady=15)

btn2 = crear_boton(ventana, "Combinaciones y permutaciones", Comb_per)
btn2.grid(row=3, column=0, columnspan=5, pady=15)

btn3 = crear_boton(ventana, "Teoría de conjuntos", Teo_conjuntos)
btn3.grid(row=4, column=0, columnspan=5, pady=15)

# --- Botón de salir ---
btn_salir = crear_boton(ventana, "SALIR", salir)
btn_salir.grid(row=7, column=0, columnspan=5, pady=30)

ventana.mainloop()
