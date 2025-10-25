import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Función para convertir texto a conjunto
def texto_a_conjunto(texto):
    try:
        elementos = texto.split(',')
        conjunto = set(int(e.strip()) for e in elementos if e.strip() != "")
        return conjunto
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa solo números separados por comas.")
        return None

# Operaciones con manejo de contingencias
def union():
    A = texto_a_conjunto(entry_A.get())
    B = texto_a_conjunto(entry_B.get())
    if A is not None and B is not None:
        if not A and not B:
            resultado.set("Ambos conjuntos están vacíos.")
        else:
            union_AB = A | B
            if not union_AB:
                resultado.set("La unión de A y B está vacía.")
            else:
                resultado.set(f"Unión (A ∪ B): {sorted(union_AB)}")

def interseccion():
    A = texto_a_conjunto(entry_A.get())
    B = texto_a_conjunto(entry_B.get())
    if A is not None and B is not None:
        interseccion_AB = A & B
        if not interseccion_AB:
            resultado.set("No hay elementos en común entre A y B.")
        else:
            resultado.set(f"Intersección (A ∩ B): {sorted(interseccion_AB)}")

def diferencia():
    A = texto_a_conjunto(entry_A.get())
    B = texto_a_conjunto(entry_B.get())
    if A is not None and B is not None:
        diferencia_AB = A - B
        if not diferencia_AB:
            resultado.set("La diferencia (A - B) está vacía. Todos los elementos de A están en B.")
        else:
            resultado.set(f"Diferencia (A - B): {sorted(diferencia_AB)}")

def diferencia_simetrica():
    A = texto_a_conjunto(entry_A.get())
    B = texto_a_conjunto(entry_B.get())
    if A is not None and B is not None:
        diferencia_sim_AB = A ^ B
        if not diferencia_sim_AB:
            resultado.set("No hay diferencia simétrica. Los conjuntos A y B son iguales.")
        else:
            resultado.set(f"Diferencia Simétrica (A Δ B): {sorted(diferencia_sim_AB)}")

def boton_regresar():
    ventana.destroy()
    subprocess.run(['python', 'Mate_discreta/main_mate.py'])

# Interfaz principal
ventana = tk.Tk()
ventana.state('zoomed')
ventana.title("Teoría de Conjuntos con Tkinter")
ventana.geometry("480x380")
ventana.config(bg="#e8f0fe")

# Etiquetas y entradas
tk.Label(ventana, text="Conjunto A (separa por comas):", bg="#e8f0fe", font=("Arial", 11, "bold")).pack(pady=5)
entry_A = tk.Entry(ventana, width=40)
entry_A.pack()

tk.Label(ventana, text="Conjunto B (separa por comas):", bg="#e8f0fe", font=("Arial", 11, "bold")).pack(pady=5)
entry_B = tk.Entry(ventana, width=40)
entry_B.pack()

# Botones de operaciones
frame_botones = tk.Frame(ventana, bg="#e8f0fe")
frame_botones.pack(pady=15)

tk.Button(frame_botones, text="Unión (A ∪ B)", command=union, bg="#4caf50", fg="white", width=20).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_botones, text="Intersección (A ∩ B)", command=interseccion, bg="#2196f3", fg="white", width=20).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_botones, text="Diferencia (A - B)", command=diferencia, bg="#ff9800", fg="white", width=20).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_botones, text="Diferencia Simétrica (A Δ B)", command=diferencia_simetrica, bg="#9c27b0", fg="white", width=20).grid(row=1, column=1, padx=5, pady=5)
btn_regresar = ttk.Button(frame_botones, text="Regresar al menú principal", command=boton_regresar)
btn_regresar.grid(row=2, column=0, columnspan=2, pady=10)
# Resultado
resultado = tk.StringVar()
tk.Label(ventana, textvariable=resultado, bg="#e8f0fe", fg="black", wraplength=440, font=("Arial", 11)).pack(pady=10)

# Ejecutar la ventana
ventana.mainloop()
