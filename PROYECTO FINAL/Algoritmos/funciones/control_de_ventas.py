import os
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

# Lista para almacenar las ventas
ventas = []

# Archivo de inventario
INVENTARIO_FILE = 'inventario.xlsx'
SHEET_INVENTARIO = 0  # Hoja de inventario
SHEET_CLIENTES = 1    # Hoja de clientes
SHEET_VENTAS = 2      # Hoja donde se guardan las ventas
SHEET_VENTAS_NAME = f'Hoja_{SHEET_VENTAS+1}_Clientes'

# --- Función para cargar datos del inventario ---
def cargar_inventario():
    if not os.path.exists(INVENTARIO_FILE):
        messagebox.showerror("Error", "El archivo inventario.xlsx no existe.")
        return pd.DataFrame(columns=["codigo", "precio"])
    try:
        df = pd.read_excel(INVENTARIO_FILE, sheet_name=SHEET_INVENTARIO, engine="openpyxl")
        df.columns = [c.strip().lower() for c in df.columns]
        if "codigo" not in df.columns or "precio" not in df.columns:
            messagebox.showerror("Error", "La hoja de inventario debe tener las columnas 'codigo' y 'precio'.")
            return pd.DataFrame(columns=["codigo", "precio"])
        return df
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el inventario: {e}")
        return pd.DataFrame(columns=["codigo", "precio"])

# --- Función para cargar clientes ---
def cargar_clientes():
    if not os.path.exists(INVENTARIO_FILE):
        return pd.DataFrame(columns=["codigo"])
    try:
        df = pd.read_excel(INVENTARIO_FILE, sheet_name=SHEET_CLIENTES, engine="openpyxl")
        df.columns = [c.strip().lower() for c in df.columns]
        if "codigo" not in df.columns:
            messagebox.showerror("Error", "La hoja de clientes debe tener una columna 'codigo'.")
            return pd.DataFrame(columns=["codigo"])
        return df
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer la hoja de clientes: {e}")
        return pd.DataFrame(columns=["codigo"])

# --- Guardar ventas ---
def guardar_datos(df):
    if os.path.exists(INVENTARIO_FILE):
        try:
            with pd.ExcelWriter(INVENTARIO_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=SHEET_VENTAS_NAME, index=False)
            return
        except Exception as e:
            print(f"Error al intentar guardar ventas: {e}")
    with pd.ExcelWriter(INVENTARIO_FILE, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=SHEET_VENTAS_NAME, index=False)

# --- Crear una venta ---
def crear_venta():
    producto = combo_producto.get().strip()
    cliente = combo_cliente.get().strip()
    if not producto or not cliente:
        messagebox.showerror("Error", "Debe seleccionar un producto y un cliente.")
        return

    try:
        cantidad = int(entry_cantidad.get())
        precio_unitario = float(entry_precio.get())
    except ValueError:
        messagebox.showerror("Error", "Cantidad y precio deben ser numéricos.")
        return

    total = cantidad * precio_unitario
    venta = {
        "Producto": producto,
        "Cliente": cliente,
        "Cantidad": cantidad,
        "Precio Unitario": precio_unitario,
        "Total": total
    }
    ventas.append(venta)
    actualizar_tabla()
    limpiar_campos()
    messagebox.showinfo("Éxito", "Venta registrada correctamente.")

    df_ventas = pd.DataFrame(ventas)
    guardar_datos(df_ventas)

# --- Actualizar tabla ---
def actualizar_tabla():
    tabla.delete(*tabla.get_children())
    for i, venta in enumerate(ventas):
        tabla.insert("", "end", iid=i, values=(
            venta["Producto"],
            venta["Cliente"],
            venta["Cantidad"],
            f"Q{venta['Precio Unitario']:.2f}",
            f"Q{venta['Total']:.2f}"
        ))

# --- Anular venta ---
def anular_venta():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Aviso", "Seleccione una venta para anular.")
        return
    index = int(seleccion[0])
    ventas.pop(index)
    actualizar_tabla()
    messagebox.showinfo("Anulado", "Venta anulada correctamente.")
    df_ventas = pd.DataFrame(ventas)
    guardar_datos(df_ventas)

# --- Limpiar campos ---
def limpiar_campos():
    combo_producto.set("")
    combo_cliente.set("")
    entry_cantidad.delete(0, tk.END)
    entry_precio.delete(0, tk.END)

# --- Cuando se selecciona un producto ---
def seleccionar_producto(event):
    producto = combo_producto.get().strip()
    if producto:
        fila = df_inventario[df_inventario["codigo"] == producto]
        if not fila.empty:
            precio = fila.iloc[0]["precio"]
            entry_precio.delete(0, tk.END)
            entry_precio.insert(0, str(precio))
        else:
            entry_precio.delete(0, tk.END)

def boton_regresar():
    root.destroy()
    subprocess.run(['python', 'Algoritmos/main_algoritmos.py'])

# --- Ventana principal ---
root = tk.Tk()
root.state("zoomed")
root.title("Control de Ventas")
root.geometry("800x600")
root.resizable(True, True)

# --- Cargar datos desde Excel ---
df_inventario = cargar_inventario()
df_clientes = cargar_clientes()

# --- Formulario de entrada ---
frame_form = tk.LabelFrame(root, text="Registrar nueva venta", padx=10, pady=10)
frame_form.pack(padx=10, pady=10, fill="x")

tk.Label(frame_form, text="Código de producto:").grid(row=0, column=0, sticky="e")
combo_producto = ttk.Combobox(frame_form, width=30, values=df_inventario["codigo"].tolist())
combo_producto.grid(row=0, column=1)
combo_producto.bind("<<ComboboxSelected>>", seleccionar_producto)

tk.Label(frame_form, text="Código del cliente:").grid(row=1, column=0, sticky="e")
combo_cliente = ttk.Combobox(frame_form, width=30, values=df_clientes["codigo"].tolist())
combo_cliente.grid(row=1, column=1)

tk.Label(frame_form, text="Cantidad de productos:").grid(row=2, column=0, sticky="e")
entry_cantidad = tk.Entry(frame_form, width=30)
entry_cantidad.grid(row=2, column=1)

tk.Label(frame_form, text="Precio unitario:").grid(row=3, column=0, sticky="e")
entry_precio = tk.Entry(frame_form, width=30)
entry_precio.grid(row=3, column=1)

tk.Button(frame_form, text="Crear venta", command=crear_venta, bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=2, pady=10)

# --- Tabla de ventas ---
frame_tabla = tk.LabelFrame(root, text="Listado de ventas", padx=10, pady=10)
frame_tabla.pack(padx=10, pady=10, fill="both", expand=True)

tabla = ttk.Treeview(frame_tabla, columns=("Producto", "Cliente", "Cantidad", "Precio Unitario", "Total"), show="headings")
tabla.heading("Producto", text="Código de producto")
tabla.heading("Cliente", text="Código del cliente")
tabla.heading("Cantidad", text="Cantidad")
tabla.heading("Precio Unitario", text="Precio Unitario")
tabla.heading("Total", text="Total de venta")
tabla.pack(fill="both", expand=True)

# --- Botón para anular venta ---
tk.Button(root, text="Anular venta seleccionada", command=anular_venta, bg="#f44336", fg="white").pack(pady=10)

boton_regresar = ttk.Button(frame_form, text="Regresar al menú principal", command=boton_regresar)
boton_regresar.grid(row=5, column=0, columnspan=2, pady=(12,0), sticky="ew")

root.mainloop()
