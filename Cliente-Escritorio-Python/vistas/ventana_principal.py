"""Ventana principal con el menu de casos de uso y el menu Ayuda."""
import tkinter as tk
from tkinter import messagebox, ttk

from config import NOMBRE_APP, TECNOLOGIA, URL_GRAPHQL, VERSION
from servicios.cliente_graphql import ClienteGraphQL
from vistas.acerca_de import VentanaAcercaDe
from vistas.agente_inteligente.vista_actualizar import VistaActualizarAgenteInteligente
from vistas.agente_inteligente.vista_adicionar import VistaAdicionarAgenteInteligente
from vistas.agente_inteligente.vista_consultar import VistaConsultarAgenteInteligente
from vistas.agente_inteligente.vista_eliminar import VistaEliminarAgenteInteligente
from vistas.agente_inteligente.vista_listar import VistaListarAgenteInteligente
from vistas.agente_navegacion.vista_actualizar import VistaActualizarAgenteNavegacion
from vistas.agente_navegacion.vista_adicionar import VistaAdicionarAgenteNavegacion
from vistas.agente_navegacion.vista_consultar import VistaConsultarAgenteNavegacion
from vistas.agente_navegacion.vista_eliminar import VistaEliminarAgenteNavegacion
from vistas.agente_navegacion.vista_listar import VistaListarAgenteNavegacion
from vistas.estilos import aplicar_estilos


class VentanaPrincipal(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title(f"{NOMBRE_APP} · v{VERSION}")
        self.geometry("760x460")
        self.minsize(620, 400)
        aplicar_estilos(self)
        self._abiertas = {}
        self._crear_menu()
        self._crear_portada()

    def _crear_menu(self):
        barra = tk.Menu(self)

        archivo = tk.Menu(barra, tearoff=False)
        archivo.add_command(label="Salir", command=self.destroy)
        barra.add_cascade(label="Archivo", menu=archivo)

        for etiqueta, vistas in (
            ("Agentes inteligentes", [
                ("Adicionar...", VistaAdicionarAgenteInteligente),
                ("Consultar...", VistaConsultarAgenteInteligente),
                ("Listar...", VistaListarAgenteInteligente),
                ("Actualizar...", VistaActualizarAgenteInteligente),
                ("Eliminar...", VistaEliminarAgenteInteligente),
            ]),
            ("Agentes de navegación", [
                ("Adicionar...", VistaAdicionarAgenteNavegacion),
                ("Consultar...", VistaConsultarAgenteNavegacion),
                ("Listar...", VistaListarAgenteNavegacion),
                ("Actualizar...", VistaActualizarAgenteNavegacion),
                ("Eliminar...", VistaEliminarAgenteNavegacion),
            ]),
        ):
            menu = tk.Menu(barra, tearoff=False)
            for texto, clase in vistas:
                menu.add_command(label=texto, command=lambda c=clase: self.abrir(c))
            barra.add_cascade(label=etiqueta, menu=menu)

        ayuda = tk.Menu(barra, tearoff=False)
        ayuda.add_command(label="Acerca de...", command=lambda: VentanaAcercaDe(self))
        barra.add_cascade(label="Ayuda", menu=ayuda)
        self.config(menu=barra)

    def _crear_portada(self):
        marco = ttk.Frame(self, padding=32)
        marco.pack(fill="both", expand=True)
        ttk.Label(marco, text=NOMBRE_APP, style="Portada.TLabel").pack(anchor="w")
        ttk.Label(marco, text=TECNOLOGIA, style="Ayuda.TLabel").pack(anchor="w", pady=(2, 18))
        ttk.Label(marco, wraplength=640, justify="left", text=(
            "Use el menú superior para gestionar los agentes inteligentes (maestro) y sus "
            "agentes de navegación (detalle): adicionar, consultar, listar, actualizar y eliminar. "
            "Cada opción abre una ventana dedicada a un solo caso de uso."
        )).pack(anchor="w")

        estado = ttk.LabelFrame(marco, text="Servidor GraphQL", padding=12)
        estado.pack(fill="x", pady=(24, 0))
        ttk.Label(estado, text=URL_GRAPHQL).pack(side="left")
        self.indicador = ttk.Label(estado, text="Sin verificar", style="Ayuda.TLabel")
        self.indicador.pack(side="left", padx=12)
        ttk.Button(estado, text="Probar conexión", command=self.probar_conexion).pack(side="right")

    def probar_conexion(self):
        try:
            ClienteGraphQL().ejecutar("query { __typename }")
            self.indicador.configure(text="Conectado")
        except Exception as e:  # noqa: BLE001
            self.indicador.configure(text="Sin conexión")
            messagebox.showerror("Sin conexión con el servidor", str(e), parent=self)

    def abrir(self, clase):
        """Abre la ventana del caso de uso; si ya esta abierta, la trae al frente."""
        ventana = self._abiertas.get(clase)
        if ventana is not None and ventana.winfo_exists():
            ventana.deiconify()
            ventana.lift()
            ventana.focus_force()
            return
        self._abiertas[clase] = clase(self)
