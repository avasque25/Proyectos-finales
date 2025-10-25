import tkinter as tk
from tkinter import messagebox
from sympy import Matrix

class InversaMatrizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inversa Redondeada")
        self.root.geometry("500x400")

        # Selección del tamaño
        tk.Label(root, text="Seleccione el tamaño de la matriz:").pack(pady=5)
        self.tamano_var = tk.StringVar(value="2")
        tk.OptionMenu(root, self.tamano_var, "2", "3", "4", command=self.crear_matriz).pack(pady=5)

        # Frame para la matriz original
        tk.Label(root, text="Matriz Original:").pack()
        self.frame_matriz = tk.Frame(root)
        self.frame_matriz.pack(pady=10)

        # Botones
        self.btn_calcular = tk.Button(root, text="Calcular Inversa", command=self.calcular_inversa)
        self.btn_calcular.pack(pady=5)

        self.btn_limpiar = tk.Button(root, text="Limpiar Todo", command=self.limpiar)
        self.btn_limpiar.pack(pady=5)

        # Label para mostrar la inversa
        self.resultado_label = tk.Label(root, text="", fg="black", font=("Courier", 14), justify="left")
        self.resultado_label.pack(pady=10)

        # Crear matriz inicial
        self.crear_matriz("2")

    def crear_matriz(self, tamano):
        # Limpiar frame
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

            # Convertir la inversa a texto tipo lista de filas, ocultando ceros y redondeando
            filas_texto = []
            for i in range(self.tamano):
                fila = []
                for j in range(self.tamano):
                    valor = float(inversa[i, j])
                    if valor == 0:
                        fila.append("")  # Ocultar ceros
                    else:
                        fila.append(str(round(valor, 1)))  # Redondear a un decimal
                filas_texto.append("[" + ", ".join(fila) + "]")

            matriz_texto = "\n".join(filas_texto)
            self.resultado_label.config(text=matriz_texto)

        except ValueError:
            messagebox.showerror("Error", "Ingrese solo números válidos en todas las celdas.")
        except Exception as e:
            messagebox.showerror("Error", f"{e}")

    def limpiar(self):
        # Limpiar matriz original
        for fila in self.entries:
            for e in fila:
                e.delete(0, tk.END)
        # Limpiar resultado
        self.resultado_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = InversaMatrizApp(root)
    root.mainloop()
