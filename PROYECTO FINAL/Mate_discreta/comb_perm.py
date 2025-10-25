import tkinter as tk
from tkinter import ttk, messagebox
import math
import subprocess

# ---------------- FUNCIONES MATEMÁTICAS ----------------

def factorial(n):
    return math.factorial(n)

def permutaciones_sin_repeticion(n, r):
    return factorial(n) // factorial(n - r)

def permutaciones_con_repeticion(n, r):
    return n ** r

def combinaciones_sin_repeticion(n, r):
    return factorial(n) // (factorial(r) * factorial(n - r))

def combinaciones_con_repeticion(n, r):
    return factorial(n + r - 1) // (factorial(r) * factorial(n - 1))

# ---------------- FUNCIÓN PRINCIPAL ----------------

def calcular():
    try:
        n = int(entry_n.get())
        r = int(entry_r.get())
        tipo = tipo_operacion.get()
        repeticion = con_repeticion.get()

        if n < 0 or r < 0:
            messagebox.showerror("Error", "Los valores deben ser positivos.")
            return
        if not repeticion and r > n:
            messagebox.showerror("Error", "r no puede ser mayor que n en operaciones sin repetición.")
            return

        if tipo == "Permutaciones":
            if repeticion:
                resultado = permutaciones_con_repeticion(n, r)
                formula = "Fórmula: n^r"
                desarrollo = f"{n}^{r} = {resultado}"
            else:
                resultado = permutaciones_sin_repeticion(n, r)
                formula = "Fórmula: n! / (n - r)!"
                desarrollo = f"{n}! / ({n} - {r})! = {resultado}"
        else:
            if repeticion:
                resultado = combinaciones_con_repeticion(n, r)
                formula = "Fórmula: (n + r - 1)! / (r! * (n - 1)!)"
                desarrollo = f"({n} + {r} - 1)! / ({r}! * ({n} - 1)!) = {resultado}"
            else:
                resultado = combinaciones_sin_repeticion(n, r)
                formula = "Fórmula: n! / (r! * (n - r)!)"
                desarrollo = f"{n}! / ({r}! * ({n} - {r})!) = {resultado}"

        lbl_formula.config(text=formula)
        lbl_resultado.config(text=f"{desarrollo}")

    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa números válidos.")
    except OverflowError:
        messagebox.showerror("Error", "Los números son demasiado grandes.")

def boton_regresar():
    ventana.destroy()
    subprocess.run(['python', 'Mate_discreta/main_mate.py'])

# ---------------- INTERFAZ TKINTER ----------------

ventana = tk.Tk()
ventana.title("Calculadora de Combinaciones y Permutaciones")
ventana.state('zoomed')
ventana.geometry("540x400")

ventana.resizable(True, True)

style = ttk.Style()
style.theme_use("clam")

frame = ttk.Frame(ventana, padding=20)
frame.pack(expand=True, fill="both")

# Título
ttk.Label(
    frame,
    text="Cálculo de Combinaciones y Permutaciones",
    font=("Segoe UI", 16, "bold")
).pack(pady=10)

# Entradas
frm_inputs = ttk.Frame(frame)
frm_inputs.pack(pady=10)

ttk.Label(frm_inputs, text="n:", font=("Segoe UI", 11)).grid(row=0, column=0, padx=8, pady=6)
entry_n = ttk.Entry(frm_inputs, width=10, justify="center")
entry_n.grid(row=0, column=1)

ttk.Label(frm_inputs, text="r:", font=("Segoe UI", 11)).grid(row=1, column=0, padx=8, pady=6)
entry_r = ttk.Entry(frm_inputs, width=10, justify="center")
entry_r.grid(row=1, column=1)

# Tipo de operación
tipo_operacion = tk.StringVar(value="Combinaciones")
ttk.Radiobutton(frm_inputs, text="Combinaciones", variable=tipo_operacion, value="Combinaciones").grid(row=0, column=2, padx=10)
ttk.Radiobutton(frm_inputs, text="Permutaciones", variable=tipo_operacion, value="Permutaciones").grid(row=1, column=2, padx=10)

# Repetición
con_repeticion = tk.BooleanVar(value=False)
chk_repeticion = ttk.Checkbutton(frame, text="Permitir repetición de elementos", variable=con_repeticion)
chk_repeticion.pack(pady=10)

# Botón Calcular
btn_calcular = ttk.Button(frame, text="Calcular", command=calcular)
btn_calcular.pack(pady=10)

# Botón Regresar (usando pack correctamente)
btn_regresar = ttk.Button(frame, text="Regresar al menú principal", command=boton_regresar)
btn_regresar.pack(pady=10)

# Etiquetas de salida
lbl_formula = ttk.Label(frame, text="", font=("Consolas", 12))
lbl_formula.pack(pady=5)

lbl_resultado = ttk.Label(frame, text="", font=("Segoe UI", 13, "bold"))
lbl_resultado.pack(pady=5)

# Pie
ttk.Label(
    frame,
    text="Vstrom © 2024 - Calculadora de Combinaciones y Permutaciones",
    font=("Segoe UI", 9),
    foreground="#666"
).pack(side="bottom", pady=10)

ventana.mainloop()
