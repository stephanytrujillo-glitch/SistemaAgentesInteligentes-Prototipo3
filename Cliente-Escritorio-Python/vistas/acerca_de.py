"""Ventana Ayuda > Acerca de..."""
import tkinter as tk
from tkinter import ttk

from config import CURSO, INTEGRANTES, NOMBRE_APP, TECNOLOGIA, VERSION


class VentanaAcercaDe(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.title("Acerca de...")
        self.resizable(False, False)
        self.transient(master)
        marco = ttk.Frame(self, padding=24)
        marco.pack(fill="both", expand=True)
        ttk.Label(marco, text=NOMBRE_APP, style="Portada.TLabel").pack(anchor="w")
        ttk.Label(marco, text=f"Versión {VERSION}").pack(anchor="w", pady=(4, 0))
        ttk.Label(marco, text=TECNOLOGIA, style="Ayuda.TLabel").pack(anchor="w")
        ttk.Label(marco, text=CURSO, style="Ayuda.TLabel").pack(anchor="w", pady=(0, 14))
        ttk.Label(marco, text="Integrantes del equipo", style="Etiqueta.TLabel").pack(anchor="w")
        for nombre in INTEGRANTES:
            ttk.Label(marco, text=nombre).pack(anchor="w")
        ttk.Button(marco, text="Cerrar", command=self.destroy).pack(anchor="e", pady=(18, 0))
        self.bind("<Escape>", lambda _e: self.destroy())
        self.grab_set()
