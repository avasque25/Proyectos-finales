import subprocess
import tkinter as tk
from tkinter import ttk

# ---- CLASE NODO ----
class Nodo:
    def __init__(self, valor):
        self.valor = str(valor)
        self.izquierdo = None
        self.derecho = None

# ---- CLASE ÁRBOL BINARIO ----
class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def agregar(self, padre, valor, lado):
        nuevo = Nodo(valor)
        if self.raiz is None:
            self.raiz = nuevo
            return True
        padre_nodo = self.buscar(self.raiz, padre)
        if padre_nodo is None:
            return False
        if lado == "Izquierdo":
            if padre_nodo.izquierdo is None:
                padre_nodo.izquierdo = nuevo
                return True
            else:
                return False
        else:
            if padre_nodo.derecho is None:
                padre_nodo.derecho = nuevo
                return True
            else:
                return False

    def buscar(self, nodo, valor):
        if nodo is None:
            return None
        if str(nodo.valor).strip() == str(valor).strip():
            return nodo
        izq = self.buscar(nodo.izquierdo, valor)
        if izq:
            return izq
        return self.buscar(nodo.derecho, valor)

    def eliminar(self, valor):
        self.raiz, _ = self._eliminar_rec(self.raiz, valor)

    def _eliminar_rec(self, nodo, valor):
        if nodo is None:
            return nodo, False
        if nodo.valor == valor:
            return None, True
        nodo.izquierdo, eliminado_izq = self._eliminar_rec(nodo.izquierdo, valor)
        if eliminado_izq:
            return nodo, True
        nodo.derecho, eliminado_der = self._eliminar_rec(nodo.derecho, valor)
        return nodo, eliminado_der

    def preorden(self, nodo, recorrido):
        if nodo:
            recorrido.append(nodo.valor)
            self.preorden(nodo.izquierdo, recorrido)
            self.preorden(nodo.derecho, recorrido)

    def inorden(self, nodo, recorrido):
        if nodo:
            self.inorden(nodo.izquierdo, recorrido)
            recorrido.append(nodo.valor)
            self.inorden(nodo.derecho, recorrido)

    def postorden(self, nodo, recorrido):
        if nodo:
            self.postorden(nodo.izquierdo, recorrido)
            self.postorden(nodo.derecho, recorrido)
            recorrido.append(nodo.valor)

# ---- INTERFAZ ----
class InterfazArbol:
    def __init__(self, root):
        self.root = root
        self.root.state('zoomed')
        self.root.title("Árbol Binario Interactivo")
        self.arbol = ArbolBinario()
        self.lado_seleccionado = "Izquierdo"
        self.nodo_seleccionado = None

        # --- Sección 1: Entrada de datos y agregar nodo ---
        frame_datos = ttk.LabelFrame(root, text="Agregar Nodo", padding=10)
        frame_datos.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(frame_datos, text="Padre:").pack(side=tk.LEFT, padx=5)
        self.padre_entry = ttk.Entry(frame_datos, width=10)
        self.padre_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(frame_datos, text="Nuevo Nodo:").pack(side=tk.LEFT, padx=5)
        self.valor_entry = ttk.Entry(frame_datos, width=10)
        self.valor_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_datos, text="Agregar Nodo", command=self.agregar_nodo).pack(side=tk.LEFT, padx=20)

        # --- Sección 2: Selección de lado ---
        frame_lado = ttk.LabelFrame(root, text="Seleccionar Lado", padding=10)
        frame_lado.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(frame_lado, text="Izquierdo", command=lambda: self.set_lado("Izquierdo")).pack(side=tk.LEFT, padx=20)
        ttk.Button(frame_lado, text="Derecho", command=lambda: self.set_lado("Derecho")).pack(side=tk.LEFT, padx=20)

        # --- Sección 3: Acciones sobre el árbol ---
        frame_acciones = ttk.LabelFrame(root, text="Acciones", padding=10)
        frame_acciones.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(frame_acciones, text="PreOrden", command=lambda: self.mostrar_recorrido("preorden")).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_acciones, text="InOrden", command=lambda: self.mostrar_recorrido("inorden")).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_acciones, text="PostOrden", command=lambda: self.mostrar_recorrido("postorden")).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_acciones, text="Eliminar Nodo", command=self.eliminar_nodo).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_acciones, text="Regresar al menú principal", command=self.regresar).pack(side=tk.LEFT, padx=10)

        # Resultado del recorrido
        self.resultado = tk.Text(root, height=3, width=70, bg="#f0f0f0", font=("Arial", 11))
        self.resultado.pack(pady=(5,10))

        # Canvas para dibujar el árbol
        self.canvas = tk.Canvas(root, width=700, height=400, bg="white")
        self.canvas.pack(pady=10)

    def regresar(self):
        self.root.destroy()
        subprocess.run(['python', 'Mate_discreta/main_mate.py'])

    def set_lado(self, lado):
        self.lado_seleccionado = lado

    def agregar_nodo(self):
        padre = self.padre_entry.get().strip()
        valor = self.valor_entry.get().strip()
        lado = self.lado_seleccionado
        if valor == "":
            return
        exito = self.arbol.agregar(padre, valor, lado)
        self.resultado.delete(1.0, tk.END)
        if exito:
            self.dibujar_arbol()
            self.resultado.insert(tk.END, f"Nodo '{valor}' agregado al lado {lado} del padre '{padre}'")
        else:
            self.resultado.insert(tk.END, f"No se pudo agregar nodo '{valor}' al lado {lado} del padre '{padre}'")

    def eliminar_nodo(self):
        if self.nodo_seleccionado:
            self.arbol.eliminar(self.nodo_seleccionado)
            self.nodo_seleccionado = None
            self.dibujar_arbol()

    def mostrar_recorrido(self, tipo):
        recorrido = []
        if tipo == "preorden":
            self.arbol.preorden(self.arbol.raiz, recorrido)
        elif tipo == "inorden":
            self.arbol.inorden(self.arbol.raiz, recorrido)
        else:
            self.arbol.postorden(self.arbol.raiz, recorrido)
        self.resultado.delete(1.0, tk.END)
        self.resultado.insert(tk.END, " → ".join(recorrido))

    def dibujar_arbol(self):
        self.canvas.delete("all")
        if self.arbol.raiz:
            self._dibujar_nodo(self.arbol.raiz, 350, 40, 150)

    def _dibujar_nodo(self, nodo, x, y, dx):
        if nodo is None:
            return
        r = 20
        tag = f"{nodo.valor}_{id(nodo)}"
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="lightblue", tags=tag)
        self.canvas.create_text(x, y, text=nodo.valor, font=("Arial", 10, "bold"), tags=tag)
        self.canvas.tag_bind(tag, "<Button-1>", lambda e, val=nodo.valor: self.seleccionar_nodo(val))

        if nodo.izquierdo:
            self.canvas.create_line(x, y + r, x - dx, y + 60 - r)
            self._dibujar_nodo(nodo.izquierdo, x - dx, y + 60, dx / 2)
        if nodo.derecho:
            self.canvas.create_line(x, y + r, x + dx, y + 60 - r)
            self._dibujar_nodo(nodo.derecho, x + dx, y + 60, dx / 2)

    def seleccionar_nodo(self, valor):
        self.nodo_seleccionado = valor

# ---- EJECUTAR PROGRAMA ----
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazArbol(root)
    root.mainloop()
