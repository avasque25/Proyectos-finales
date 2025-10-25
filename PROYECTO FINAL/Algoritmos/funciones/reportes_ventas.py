import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from email.message import EmailMessage
import mimetypes
import smtplib
import ssl
import os
import subprocess

# ---------------- CONFIGURACIÓN DE SERVIDOR ----------------
SERVIDOR = "smtp.gmail.com"
PUERTO = 587
CONTRASENA = os.getenv('GOOGLE_APP_PASS')
USUARIO = os.getenv("GOOGLE_EMAIL")

# ---------------- FUNCIÓN PARA ENVIAR CORREO ----------------
def enviar_mensaje(asunto, cuerpo, destinatario, titulo, nombre_archivo, ruta_de_adjunto):
    mensaje = EmailMessage()
    mensaje["Subject"] = asunto
    mensaje["From"] = USUARIO
    mensaje["To"] = destinatario

    # Cuerpo de texto
    mensaje.set_content(cuerpo)

    # Cuerpo HTML
    html_content = f"""
    <html>
        <body>
            <h1>{titulo}</h1>
            <p>{cuerpo}</p>
        </body>
    </html>
    """
    mensaje.add_alternative(html_content, subtype="html")

    # Adjuntar archivo si existe
    if nombre_archivo and ruta_de_adjunto:
        ctype, encoding = mimetypes.guess_type(nombre_archivo)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        tipo_principal, sub_tipo = ctype.split("/", 1)

        with open(os.path.join(ruta_de_adjunto, nombre_archivo), 'rb') as archivo:
            mensaje.add_attachment(
                archivo.read(),
                maintype=tipo_principal,
                subtype=sub_tipo,
                filename=nombre_archivo
            )

    # Enviar el correo
    context = ssl.create_default_context()
    with smtplib.SMTP(SERVIDOR, PUERTO) as smtp:
        smtp.starttls(context=context)
        smtp.login(USUARIO, CONTRASENA)
        smtp.send_message(mensaje)

# ---------------- FUNCIONES DE INTERFAZ ----------------
def seleccionar_archivo():
    ruta_completa = filedialog.askopenfilename(title="Seleccionar archivo adjunto")
    if ruta_completa:
        ruta, nombre = os.path.split(ruta_completa)
        entry_archivo.delete(0, tk.END)
        entry_archivo.insert(0, nombre)
        entry_ruta.delete(0, tk.END)
        entry_ruta.insert(0, ruta)

def enviar():
    asunto = entry_asunto.get()
    cuerpo = txt_cuerpo.get("1.0", tk.END).strip()
    destinatario = entry_destinatario.get()
    titulo = entry_titulo.get()
    nombre_archivo = entry_archivo.get()
    ruta_de_adjunto = entry_ruta.get()

    if not asunto or not cuerpo or not destinatario:
        messagebox.showwarning("Campos incompletos", "Por favor completa los campos obligatorios.")
        return

    try:
        enviar_mensaje(asunto, cuerpo, destinatario, titulo, nombre_archivo, ruta_de_adjunto)
        messagebox.showinfo("Éxito", "Correo enviado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo enviar el correo.\n{e}")

def boton_regresar():
    ventana.destroy()
    subprocess.run(['python', 'Algoritmos\main_algoritmos.py'])

# ---------------- INTERFAZ GRÁFICA ----------------
ventana = tk.Tk()
ventana.state('zoomed')
ventana.title("Envío de Correos con Adjunto")
ventana.geometry("500x550")
ventana.resizable(True, True)

tk.Label(ventana, text="Asunto:").pack(anchor="w", padx=10, pady=(10, 0))
entry_asunto = tk.Entry(ventana, width=60)
entry_asunto.pack(padx=10, pady=5)

tk.Label(ventana, text="Destinatario:").pack(anchor="w", padx=10)
entry_destinatario = tk.Entry(ventana, width=60)
entry_destinatario.pack(padx=10, pady=5)

tk.Label(ventana, text="Título (opcional):").pack(anchor="w", padx=10)
entry_titulo = tk.Entry(ventana, width=60)
entry_titulo.pack(padx=10, pady=5)

tk.Label(ventana, text="Cuerpo del mensaje:").pack(anchor="w", padx=10)
txt_cuerpo = tk.Text(ventana, height=10, width=58)
txt_cuerpo.pack(padx=10, pady=5)

tk.Label(ventana, text="Archivo adjunto (opcional):").pack(anchor="w", padx=10)
frame_archivo = tk.Frame(ventana)
frame_archivo.pack(padx=10, pady=5, fill="x")

entry_archivo = tk.Entry(frame_archivo, width=35)
entry_archivo.pack(side="left", padx=5)

tk.Button(frame_archivo, text="Buscar", command=seleccionar_archivo).pack(side="left", padx=5)

tk.Label(ventana, text="Ruta del adjunto:").pack(anchor="w", padx=10)
entry_ruta = tk.Entry(ventana, width=60)
entry_ruta.pack(padx=10, pady=5)

tk.Button(
    ventana,
    text="Enviar Correo",
    command=enviar,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12, "bold"),
    width=20
).pack(pady=20)

tk.Button(
    ventana,
    text="Regresar al menú principal",
    command=boton_regresar,
    bg="#f44336",
    fg="white",
    font=("Arial", 12, "bold"),
    width=25
).pack(pady=(10, 20))

ventana.mainloop()
