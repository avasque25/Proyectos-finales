from asyncio import subprocess
import tkinter as tk
from tkinter import messagebox
import math
import subprocess

# Función para calcular el MCD
def calcular_mcd():
    try:
        # Obtener valores de las entradas
        num1_str = entry_num1.get().strip()
        num2_str = entry_num2.get().strip()

        if not num1_str or not num2_str:
            messagebox.showwarning("Advertencia", "Por favor completa ambos campos.")
            return

        num1 = int(num1_str)
        num2 = int(num2_str)

        num1 = abs(num1)
        num2 = abs(num2)

        if num1 == 0 and num2 == 0:
            messagebox.showwarning("Advertencia", "El MCD no está definido para (0, 0).")
            return

        # Calcular el MCD
        resultado = math.gcd(num1, num2)
        label_resultado.config(text=f"El MCD de {num1} y {num2} es: {resultado}")

    except ValueError:
        messagebox.showerror("Error", "Entrada inválida. Ingresa solo números enteros.")

def boton_regresar():
    ventana.destroy()
    subprocess.run(['python', 'Mate_discreta\main_mate.py'])

# Crear ventana principal
ventana = tk.Tk()
ventana.state('zoomed')
ventana.title("Calculadora de MCD")
ventana.geometry("350x270")
ventana.resizable(True, True)
ventana.config(bg="#f0f0f0")

# Título
titulo = tk.Label(ventana, text="Cálculo del Máximo Común Divisor", font=("Arial", 14, "bold"), bg="#f0f0f0")
titulo.pack(pady=10)

# Campo para número 1 y 2
frame_num1 = tk.Frame(ventana, bg="#f0f0f0")
frame_num1.pack(pady=5)
tk.Label(frame_num1, text="Primer número:", bg="#f0f0f0").pack(side="left", padx=5)
entry_num1 = tk.Entry(frame_num1, width=10)
entry_num1.pack(side="left")

frame_num2 = tk.Frame(ventana, bg="#f0f0f0")
frame_num2.pack(pady=5)
tk.Label(frame_num2, text="Segundo número:", bg="#f0f0f0").pack(side="left", padx=5)
entry_num2 = tk.Entry(frame_num2, width=10)
entry_num2.pack(side="left")

# Botón para calcular
boton_calcular = tk.Button(
    ventana,
    text="Calcular MCD",
    command=calcular_mcd,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold"),
)
boton_calcular.pack(pady=15)

btn_regresar = tk.Button(ventana, text="Regresar al menú principal", command=boton_regresar)
btn_regresar.pack(pady=10)

label_resultado = tk.Label(ventana, text="", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#333")
label_resultado.pack(pady=10)

ventana.mainloop()
