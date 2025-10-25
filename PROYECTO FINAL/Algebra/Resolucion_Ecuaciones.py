#---Tema 1: Inversa de una matriz---#



#---Tema 2: Multiplicación de matrices---#
import tkinter as tk
from tkinter import ttk, messagebox


def multiplicar_matrices_manual(matriz_a, matriz_b):
    """Realiza la multiplicación de dos matrices (A * B)."""
    
    try:
        filas_a = len(matriz_a)
        cols_a = len(matriz_a[0]) if filas_a > 0 and matriz_a[0] else 0
        filas_b = len(matriz_b)
        cols_b = len(matriz_b[0]) if filas_b > 0 and matriz_b[0] else 0
    except (IndexError, TypeError):
        return "Error: Asegúrate de que ambas matrices estén completamente llenas con datos válidos."

    if cols_a != filas_b:
        return f"Error: No se pueden multiplicar. El número de columnas de A ({cols_a}) debe ser igual al número de filas de B ({filas_b})."
    
    resultado = [[0 for _ in range(cols_b)] for _ in range(filas_a)]

    for i in range(filas_a):
        for j in range(cols_b):
            suma = 0
            for k in range(cols_a):
                suma += matriz_a[i][k] * matriz_b[k][j]
            resultado[i][j] = suma

    return resultado

# ----------------------------------------------------
# 2. INTERFAZ GRÁFICA (TKINTER)
# ----------------------------------------------------

class MatrixApp:
    def __init__(self, master):
        self.master = master
        master.title("Multiplicación de Matrices Dinámica")
        
        # Máximo de filas/columnas permitido
        self.MAX_DIMENSION = 4 
        
        self.entry_a = []
        self.entry_b = []
        
        self.rows_a = tk.IntVar(value=2)
        self.cols_a = tk.IntVar(value=2)
        self.rows_b = tk.IntVar(value=2)
        self.cols_b = tk.IntVar(value=2)

        # La sincronización solo actualiza la otra variable y llama a redraw.
        self.cols_a.trace_add("write", lambda *args: self.sync_b_rows())
        self.rows_b.trace_add("write", lambda *args: self.sync_a_cols())

        self.create_widgets()
        
    def sync_b_rows(self):
        """Sincroniza filas de B para que coincidan con columnas de A (cols_A = rows_B)."""
        try:
            new_cols_a = self.cols_a.get()
            if self.rows_b.get() != new_cols_a:
                self.rows_b.set(new_cols_a)
                self.update_matrices()
        except tk.TclError:
            pass 

    def sync_a_cols(self):
        """Sincroniza columnas de A para que coincidan con filas de B (rows_B = cols_A)."""
        try:
            new_rows_b = self.rows_b.get()
            if self.cols_a.get() != new_rows_b:
                self.cols_a.set(new_rows_b)
                self.update_matrices()
        except tk.TclError:
            pass 

    def create_widgets(self):
        
        # Frame de Control de Dimensiones
        frame_controls = tk.LabelFrame(self.master, text=f"Definir Dimensiones (Máximo {self.MAX_DIMENSION}x{self.MAX_DIMENSION})")
        frame_controls.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Matriz A Controls
        tk.Label(frame_controls, text="Matriz A (Filas x Cols):").grid(row=0, column=0, padx=5, pady=2)
        ttk.Entry(frame_controls, textvariable=self.rows_a, width=4).grid(row=0, column=1, padx=2)
        ttk.Label(frame_controls, text="x").grid(row=0, column=2)
        ttk.Entry(frame_controls, textvariable=self.cols_a, width=4).grid(row=0, column=3, padx=2)
        
        # Matriz B Controls
        tk.Label(frame_controls, text="Matriz B (Filas x Cols):").grid(row=1, column=0, padx=5, pady=2)
        ttk.Entry(frame_controls, textvariable=self.rows_b, width=4).grid(row=1, column=1, padx=2)
        ttk.Label(frame_controls, text="x").grid(row=1, column=2)
        ttk.Entry(frame_controls, textvariable=self.cols_b, width=4).grid(row=1, column=3, padx=2)

        # Botón para Aplicar Dimensiones
        ttk.Button(frame_controls, text="Aplicar", command=self.update_matrices).grid(row=0, column=4, rowspan=2, padx=10)


        # --- Frames para las Matrices ---
        self.container_matrices = tk.Frame(self.master)
        self.container_matrices.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        
        self.frame_a = tk.LabelFrame(self.container_matrices, text="Matriz A")
        self.frame_a.grid(row=0, column=0, padx=10, pady=10, sticky='n')
        
        self.frame_b = tk.LabelFrame(self.container_matrices, text="Matriz B")
        self.frame_b.grid(row=0, column=1, padx=10, pady=10, sticky='n')
        
        self.update_matrices() 

        # --- Botón de Cálculo ---
        self.calculate_button = tk.Button(self.master, text="Multiplicar A * B", command=self.calcular)
        self.calculate_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # --- Área de Resultado ---
        tk.Label(self.master, text="Resultado (Matriz C):").grid(row=3, column=0, columnspan=2, sticky='w', padx=10)
        self.result_text = tk.Text(self.master, height=6, width=40, state='disabled')
        self.result_text.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # Botón para salir (necesario por 'overrideredirect')
        self.exit_button = tk.Button(self.master, text="Presiona [Esc] o haz clic para salir", 
                                     command=lambda: self.master.destroy())
        self.exit_button.grid(row=5, column=0, columnspan=2, pady=5)
        
        
    def update_matrices(self):
        """Actualiza la GUI para reflejar las nuevas dimensiones de las matrices, aplicando validaciones."""
        
        try:
            r_a = self.rows_a.get()
            c_a = self.cols_a.get()
            r_b = self.rows_b.get()
            c_b = self.cols_b.get()
        except tk.TclError:
            messagebox.showerror("Error", "Las dimensiones deben ser números enteros válidos.")
            return

        # 1. Aplicar límite máximo de 4x4
        limit_exceeded = False
        
        # Validación y ajuste del límite
        if r_a > self.MAX_DIMENSION: self.rows_a.set(self.MAX_DIMENSION); limit_exceeded = True
        if c_a > self.MAX_DIMENSION: self.cols_a.set(self.MAX_DIMENSION); limit_exceeded = True
        if r_b > self.MAX_DIMENSION: self.rows_b.set(self.MAX_DIMENSION); limit_exceeded = True
        if c_b > self.MAX_DIMENSION: self.cols_b.set(self.MAX_DIMENSION); limit_exceeded = True

        # Re-obtener los valores ajustados (si se excedió el límite)
        r_a = self.rows_a.get()
        c_a = self.cols_a.get()
        r_b = self.rows_b.get()
        c_b = self.cols_b.get()

        if limit_exceeded:
            messagebox.showwarning("Límite de Dimensión", f"La dimensión máxima permitida es {self.MAX_DIMENSION}x{self.MAX_DIMENSION}. Los valores se han ajustado.")
        
        # 2. Validación de dimensiones positivas
        if r_a <= 0 or c_a <= 0 or r_b <= 0 or c_b <= 0:
            messagebox.showerror("Error", "Las dimensiones deben ser mayores que cero.")
            return
        
        # 3. Forzar la regla de multiplicación
        if c_a != r_b:
             # Este bloque es redundante debido a las trazas, pero sirve como doble validación
             messagebox.showinfo("Regla Matemática", f"Para multiplicar, Col(A) debe ser igual a Fil(B). Se ajustó Fil(B) a {c_a}.")
             self.rows_b.set(c_a)
             r_b = c_a 
        
        # Destruir widgets antiguos
        for widget in self.frame_a.winfo_children(): widget.destroy()
        for widget in self.frame_b.winfo_children(): widget.destroy()
            
        self.entry_a = []
        self.entry_b = []

        # Re-crear widgets con las dimensiones finales
        self.frame_a.config(text=f"Matriz A ({r_a}x{c_a})")
        self.create_matrix_inputs(self.frame_a, self.entry_a, r_a, c_a)
        
        self.frame_b.config(text=f"Matriz B ({r_b}x{c_b})")
        self.create_matrix_inputs(self.frame_b, self.entry_b, r_b, c_b)


    def create_matrix_inputs(self, frame, entry_list, rows, cols):
        """Crea los campos de entrada para una matriz R x C."""
        for r in range(rows):
            row_entries = []
            for c in range(cols):
                entry = tk.Entry(frame, width=5, justify='center')
                entry.insert(0, "0") 
                entry.grid(row=r, column=c, padx=5, pady=5)
                row_entries.append(entry)
            entry_list.append(row_entries)

    
    def get_matrix_data(self, entry_list, rows, cols):
        """Extrae los datos de la GUI y los convierte a una lista de listas de flotantes."""
        matrix = []
        try:
            for r in range(rows):
                row = []
                for c in range(cols):
                    value = float(entry_list[r][c].get())
                    row.append(value)
                matrix.append(row)
            return matrix
        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, ingresa solo números válidos en las celdas de las matrices.")
            return None

    def display_result(self, result):
        """Muestra el resultado o mensaje de error en el área de texto."""
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)  
        
        if isinstance(result, str):
            self.result_text.insert(tk.END, result)
        else:
            formatted_result = ""
            for row in result:
                formatted_row = [f"{x:^7.2f}" for x in row]
                formatted_result += f"[ {' '.join(formatted_row)} ]\n"
            self.result_text.insert(tk.END, formatted_result.strip())
            
        self.result_text.config(state='disabled')

    def calcular(self):
        """Función principal llamada al hacer clic en el botón."""
        
        r_a = self.rows_a.get()
        c_a = self.cols_a.get()
        r_b = self.rows_b.get()
        c_b = self.cols_b.get()
        
        matriz_a = self.get_matrix_data(self.entry_a, r_a, c_a)
        matriz_b = self.get_matrix_data(self.entry_b, r_b, c_b)
        
        if matriz_a is None or matriz_b is None:
            return 

        resultado = multiplicar_matrices_manual(matriz_a, matriz_b)
        
        self.display_result(resultado)

# ----------------------------------------------------
# 3. Ejecución de la Aplicación
# ----------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    
    # Configuraciones para forzar la pantalla completa:
    
    # 1. Obtener el tamaño de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # 2. Remover los bordes de la ventana (necesario para fullscreen forzado)
    root.overrideredirect(True) 
    
    # 3. Forzar el tamaño de la ventana al tamaño de la pantalla
    root.geometry(f'{screen_width}x{screen_height}+0+0')
    
    # 4. Configurar el evento para salir (tecla ESC)
    root.bind('<Escape>', lambda event: root.destroy()) 
    
    app = MatrixApp(root)
    root.mainloop()

    
#---Tema 3: Resolución de sistemas de ecuaciones lineales (2x2, 3x3, 4x4)---#