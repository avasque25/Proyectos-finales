import tkinter as tk
from tkinter import messagebox
from sympy import Matrix

class InversaEnteraRedondeadaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inversa Entera Redondeada")
        self.root.geometry("500x400")

        tk.Label(root, text="Seleccione el tamaño de la matriz:").pack(pady=5)
        self.tamano_var = tk.StringVar(value="2")
        tk.OptionMenu(root, self.tamano_var, "2", "3", "4", command=self.crear_matriz).pack(pady=5)

        tk.Label(root, text="Matriz Original:").pack()
        self.frame_matriz = tk.Frame(root)
        self.frame_matriz.pack(pady=10)

        self.btn_calcular = tk.Button(root, text="Calcular Inversa Entera", command=self.calcular_inversa)
        self.btn_calcular.pack(pady=5)

        self.btn_limpiar = tk.Button(root, text="Limpiar Todo", command=self.limpiar)
        self.btn_limpiar.pack(pady=5)

        self.resultado_label = tk.Label(root, text="", fg="black", font=("Courier", 14), justify="left")
        self.resultado_label.pack(pady=10)

        self.crear_matriz("2")

    def crear_matriz(self, tamano):
        for widget in self.frame_matriz.winfo_children():
            widget.destroy()

        self.tamano = int(tamano)
        self.entries = []
        for i in range(self.tamano):
            fila_entries = []
            for j in range(self.tamano):
                e = tk.Entry(self.frame_matriz, width=7, justify='center')
                e.grid(row=i, column=j, padx=5, pady=5)
                fila_entries.append(e)
            self.entries.append(fila_entries)

    def calcular_inversa(self):
        try:
            matriz = []
            for fila in self.entries:
                fila_valores = [float(e.get()) for e in fila]
                matriz.append(fila_valores)

            matriz_sym = Matrix(matriz)

            if matriz_sym.shape[0] != matriz_sym.shape[1]:
                messagebox.showerror("Error", "La matriz debe ser cuadrada")
                return
            if matriz_sym.det() == 0:
                messagebox.showerror("Error", "La matriz no tiene inversa (determinante = 0)")
                return

            inversa = matriz_sym.inv()
            
            filas_texto = []
            for i in range(self.tamano):
                fila = []
                for j in range(self.tamano):
                    valor = inversa[i, j]
                    entero = int(round(float(valor)))  # redondear a entero más cercano
                    fila.append(str(entero))  # mostrar todos los valores, incluido 0
                filas_texto.append("[" + ", ".join(fila) + "]")

            self.resultado_label.config(text="\n".join(filas_texto))

        except ValueError:
            messagebox.showerror("Error", "Ingrese solo números válidos.")
        except Exception as e:
            messagebox.showerror("Error", f"{e}")

    def limpiar(self):
        for fila in self.entries:
            for e in fila:
                e.delete(0, tk.END)
        self.resultado_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = InversaEnteraRedondeadaApp(root)
    root.mainloop()
