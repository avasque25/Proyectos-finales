import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
import subprocess

# Archivo de inventario
INVENTARIO_FILE = 'inventario.xlsx'
SHEET_NAME = 1  # Segunda hoja (clientes)


def cargar_datos():
    """
    Carga los datos desde la hoja de clientes.
    Devuelve DataFrame vacío si hay error o la hoja no existe.
    Normaliza nombres de columnas: minúsculas y sin espacios.
    """
    expected_columns = ['codigo', 'nombre', 'direccion']

    if os.path.exists(INVENTARIO_FILE):
        try:
            df = pd.read_excel(
                INVENTARIO_FILE,
                sheet_name=SHEET_NAME,
                dtype=str,
                engine='openpyxl'
            )
            # Normalizar columnas
            df.columns = [c.strip().lower() for c in df.columns]

            # Añadir columnas faltantes
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ""
            return df[expected_columns]
        except Exception as e:
            print(f"Error al cargar Excel: {e}")
            return pd.DataFrame(columns=expected_columns)
    else:
        return pd.DataFrame(columns=expected_columns)


def guardar_datos(df):
    """
    Guarda el DataFrame en la hoja de clientes.
    Normaliza columnas antes de guardar.
    """
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    sheet_name = f'Hoja_{SHEET_NAME+1}_Clientes'

    if os.path.exists(INVENTARIO_FILE):
        try:
            with pd.ExcelWriter(INVENTARIO_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            return
        except Exception as e:
            print(f"Error al guardar Excel: {e}")

    # Crear archivo nuevo si no existe
    with pd.ExcelWriter(INVENTARIO_FILE, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)


# --- Funciones de lógica ---
def crear_cliente_logica(codigo, nombre, direccion):
    df_clientes = cargar_datos()

    if not all([codigo, nombre, direccion]):
        return False, "Error: Todos los campos son obligatorios."

    if codigo in df_clientes['codigo'].values:
        return False, f"Error: El código '{codigo}' ya existe."

    nuevo_cliente = pd.DataFrame({'codigo': [codigo], 'nombre': [nombre], 'direccion': [direccion]})
    df_clientes = pd.concat([df_clientes, nuevo_cliente], ignore_index=True)
    guardar_datos(df_clientes)
    return True, "Cliente creado exitosamente."


def actualizar_cliente_logica(codigo, nuevo_nombre, nueva_direccion):
    df_clientes = cargar_datos()
    idx = df_clientes[df_clientes['codigo'] == codigo].index

    if idx.empty:
        return False, "Error: Cliente no encontrado para actualizar."

    df_clientes.loc[idx, 'nombre'] = nuevo_nombre
    df_clientes.loc[idx, 'direccion'] = nueva_direccion
    guardar_datos(df_clientes)
    return True, "Cliente actualizado exitosamente."


def eliminar_cliente_logica(codigo):
    df_clientes = cargar_datos()
    df_actualizado = df_clientes[df_clientes['codigo'] != codigo]

    if len(df_actualizado) == len(df_clientes):
        return False, "Error: Cliente no encontrado para eliminar."

    guardar_datos(df_actualizado)
    return True, "Cliente eliminado exitosamente."


# --- Interfaz gráfica ---
class ClienteApp:
    def __init__(self, master):
        self.master = master
        self.master.state("zoomed")
        master.title("Control de Clientes")
        self.codigo = tk.StringVar()
        self.nombre = tk.StringVar()
        self.direccion = tk.StringVar()
        self.crear_widgets()
        self.cargar_lista_clientes()

    def regresar(self):
        self.master.destroy()
        subprocess.run(['python', 'Algoritmos\main_algoritmos.py'])

    def crear_widgets(self):
        frame_input = ttk.LabelFrame(self.master, text="Gestión de Cliente", padding="10")
        frame_input.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(frame_input, text="Código:").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Entry(frame_input, textvariable=self.codigo).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame_input, text="Nombre:").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Entry(frame_input, textvariable=self.nombre).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(frame_input, text="Dirección:").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Entry(frame_input, textvariable=self.direccion).grid(row=2, column=1, padx=5, pady=2)

        frame_btns = ttk.Frame(frame_input)
        frame_btns.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(frame_btns, text="Crear", command=self.ejecutar_crear).grid(row=0, column=0, padx=5)
        ttk.Button(frame_btns, text="Actualizar", command=self.ejecutar_actualizar).grid(row=0, column=1, padx=5)
        ttk.Button(frame_btns, text="Eliminar", command=self.ejecutar_eliminar).grid(row=0, column=2, padx=5)
        ttk.Button(frame_btns, text="Regresar al menú principal", command=self.regresar).grid(row=0, column=3, padx=5)

        frame_lista = ttk.LabelFrame(self.master, text="Lista de Clientes", padding="10")
        frame_lista.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.lista_clientes = ttk.Treeview(frame_lista, columns=('codigo', 'nombre', 'direccion'), show='headings')
        self.lista_clientes.heading('codigo', text='Código')
        self.lista_clientes.heading('nombre', text='Nombre')
        self.lista_clientes.heading('direccion', text='Dirección')

        self.lista_clientes.column('codigo', width=70)
        self.lista_clientes.column('nombre', width=150)
        self.lista_clientes.column('direccion', width=200)

        self.lista_clientes.grid(row=0, column=0, sticky="nsew")
        self.lista_clientes.bind('<<TreeviewSelect>>', self.cargar_cliente_seleccionado)

        frame_lista.grid_columnconfigure(0, weight=1)
        frame_lista.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def limpiar_campos(self):
        self.codigo.set("")
        self.nombre.set("")
        self.direccion.set("")

    def cargar_cliente_seleccionado(self, event):
        seleccion = self.lista_clientes.selection()
        if seleccion:
            valores = self.lista_clientes.item(seleccion[0], 'values')
            self.codigo.set(valores[0])
            self.nombre.set(valores[1])
            self.direccion.set(valores[2])

    def cargar_lista_clientes(self):
        for item in self.lista_clientes.get_children():
            self.lista_clientes.delete(item)

        df = cargar_datos()

        for index, row in df.iterrows():
            self.lista_clientes.insert('', tk.END, values=row.tolist())

    def ejecutar_crear(self):
        cod = self.codigo.get()
        nom = self.nombre.get()
        dir = self.direccion.get()
        exito, mensaje = crear_cliente_logica(cod, nom, dir)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_campos()
            self.cargar_lista_clientes()
        else:
            messagebox.showerror("Fallo", mensaje)

    def ejecutar_actualizar(self):
        cod = self.codigo.get()
        nom = self.nombre.get()
        dir = self.direccion.get()
        exito, mensaje = actualizar_cliente_logica(cod, nom, dir)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_campos()
            self.cargar_lista_clientes()
        else:
            messagebox.showerror("Fallo", mensaje)

    def ejecutar_eliminar(self):
        cod = self.codigo.get()
        if not cod:
            messagebox.showerror("Fallo", "Seleccione un cliente de la lista o ingrese un código para eliminar.")
            return
        respuesta = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el cliente con código {cod}?")
        if respuesta:
            exito, mensaje = eliminar_cliente_logica(cod)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_campos()
                self.cargar_lista_clientes()
            else:
                messagebox.showerror("Fallo", mensaje)


if __name__ == '__main__':
    root = tk.Tk()
    app = ClienteApp(root)
    root.mainloop()
