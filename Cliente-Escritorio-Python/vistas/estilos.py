"""Paleta y estilos ttk compartidos por todas las ventanas."""
from tkinter import ttk

FONDO = "#E6EBEF"
SUPERFICIE = "#FFFFFF"
TINTA = "#18273A"
TINTA_SUAVE = "#5A6A7E"
PRIMARIO = "#1D5FA8"
PELIGRO = "#B3261E"
FUENTE = ("Segoe UI", 10)


def aplicar_estilos(raiz):
    estilo = ttk.Style(raiz)
    try:
        estilo.theme_use("clam")
    except Exception:
        pass
    raiz.configure(background=FONDO)
    estilo.configure(".", font=FUENTE, background=FONDO, foreground=TINTA)
    estilo.configure("TFrame", background=FONDO)
    estilo.configure("TLabelframe", background=FONDO)
    estilo.configure("TLabelframe.Label", background=FONDO, foreground=TINTA, font=("Segoe UI", 10, "bold"))
    estilo.configure("TLabel", background=FONDO, foreground=TINTA)
    estilo.configure("TCheckbutton", background=FONDO)
    estilo.configure("Ayuda.TLabel", foreground=TINTA_SUAVE, font=("Segoe UI", 9))
    estilo.configure("Etiqueta.TLabel", foreground=TINTA_SUAVE)
    estilo.configure("Barra.TFrame", background=TINTA)
    estilo.configure("TituloVentana.TLabel", background=TINTA, foreground="#FFFFFF", font=("Segoe UI", 14, "bold"))
    estilo.configure("SubtituloVentana.TLabel", background=TINTA, foreground="#C7D3E0", font=("Segoe UI", 9))
    estilo.configure("Portada.TLabel", font=("Segoe UI", 20, "bold"))
    estilo.configure("Primario.TButton", background=PRIMARIO, foreground="#FFFFFF", padding=(14, 6))
    estilo.map("Primario.TButton", background=[("disabled", "#9DB3CC"), ("active", "#17508F")])
    estilo.configure("Peligro.TButton", background=PELIGRO, foreground="#FFFFFF", padding=(14, 6))
    estilo.map("Peligro.TButton", background=[("disabled", "#D9A3A0"), ("active", "#921F18")])
    estilo.configure("Treeview", rowheight=24, background=SUPERFICIE, fieldbackground=SUPERFICIE)
    estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
