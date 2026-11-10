"""Componentes reutilizables: formulario, ficha de solo lectura, grilla y buscador."""
import re
import tkinter as tk
from datetime import datetime
from tkinter import ttk

from modelo.formato import formatear
from modelo.validador import validar

SIN_ASIGNAR = "(sin asignar)"


class ComboReferencia(ttk.Combobox):
    """Selector de agente inteligente que BUSCA en el servidor mientras se escribe.

    No carga todos los agentes (con miles seria lento): pide al servidor maximo 20
    coincidencias por nombre o por ID. Se puede escribir "Atlas", "atl" o "1".
    """

    def __init__(self, master, buscar, permitir_vacio=True, **opciones):
        super().__init__(master, **opciones)
        self._buscar = buscar
        self._permitir_vacio = permitir_vacio
        self._mapa = {}
        self._pendiente = None
        self.bind("<KeyRelease>", self._al_escribir)
        self.refrescar()
        if permitir_vacio:
            self.set(SIN_ASIGNAR)

    def _al_escribir(self, evento):
        if evento.keysym in ("Up", "Down", "Return", "Escape", "Tab", "Left", "Right"):
            return
        if self._pendiente:
            self.after_cancel(self._pendiente)
        # espera 300 ms despues de la ultima tecla para no consultar en cada letra
        self._pendiente = self.after(300, lambda: self.refrescar(self.get()))

    def refrescar(self, texto=""):
        texto = "" if texto in (None, SIN_ASIGNAR) else texto.strip()
        # si el texto ya es una opcion elegida ("1 - Atlas"), se busca por su ID
        coincidencia = re.match(r"^\s*(\d+)\s*-", texto)
        consulta = coincidencia.group(1) if coincidencia else texto
        try:
            pares = self._buscar(consulta)
        except Exception:  # noqa: BLE001 - sin servidor, simplemente no hay opciones
            pares = []
        self._mapa = {f"{i} - {n}": i for i, n in pares}
        # al desplegar la flecha se ven las coincidencias de lo que se escribio
        self["values"] = ([SIN_ASIGNAR] if self._permitir_vacio else []) + list(self._mapa)

    def valor(self):
        """ID elegido, None si esta vacio, o el texto si no corresponde a un agente."""
        texto = self.get().strip()
        if texto in ("", SIN_ASIGNAR):
            return None
        if texto in self._mapa:
            return self._mapa[texto]
        if texto.isdigit():
            return int(texto)
        coincidencia = re.match(r"^\s*(\d+)\s*-", texto)
        return int(coincidencia.group(1)) if coincidencia else texto

    def establecer(self, id_agente):
        if id_agente is None:
            self.set(SIN_ASIGNAR if self._permitir_vacio else "")
            return
        self.refrescar(str(id_agente))
        texto = next((t for t, i in self._mapa.items() if i == id_agente), str(id_agente))
        self.set(texto)

    def limpiar(self):
        self.set(SIN_ASIGNAR if self._permitir_vacio else "")
        self.refrescar()


class Formulario(ttk.Frame):
    """Formulario generado a partir de la definicion de campos de una clase."""

    def __init__(self, master, campos, proveedor_referencias=None, mostrar_ayuda=True):
        super().__init__(master)
        self.campos = campos
        self._proveedor = proveedor_referencias
        self._vars = {}
        self._widgets = {}
        self.columnconfigure(1, weight=1)

        for fila, campo in enumerate(campos):
            texto = campo.etiqueta + (" *" if campo.obligatorio else "")
            ttk.Label(self, text=texto).grid(row=fila, column=0, sticky="w", padx=(0, 10), pady=3)

            if campo.tipo == "booleano":
                var = tk.BooleanVar(value=False)
                widget = ttk.Checkbutton(self, text="Sí", variable=var)
            elif campo.tipo == "opcion":
                var = tk.StringVar()
                widget = ttk.Combobox(self, textvariable=var, values=campo.opciones, state="readonly")
            elif campo.tipo == "referencia":
                var = None
                buscar = self._proveedor or (lambda _texto: [])
                widget = ComboReferencia(self, buscar)
            else:
                var = tk.StringVar()
                widget = ttk.Entry(self, textvariable=var)
            widget.grid(row=fila, column=1, sticky="ew", pady=3)

            if campo.tipo == "fecha":
                ttk.Button(self, text="Ahora", width=7,
                           command=lambda v=var: v.set(datetime.now().strftime("%Y-%m-%d %H:%M"))
                           ).grid(row=fila, column=2, padx=(6, 0))
            if mostrar_ayuda and campo.ayuda:
                ttk.Label(self, text=campo.ayuda, style="Ayuda.TLabel").grid(
                    row=fila, column=3, sticky="w", padx=(10, 0))

            self._vars[campo.clave] = var
            self._widgets[campo.clave] = widget

        ttk.Label(self, text="* Campo obligatorio", style="Ayuda.TLabel").grid(
            row=len(campos), column=0, columnspan=4, sticky="w", pady=(8, 0))

    def recargar_referencias(self):
        for campo in self.campos:
            if campo.tipo == "referencia":
                combo = self._widgets[campo.clave]
                combo.refrescar(combo.get())

    def valores_crudos(self) -> dict:
        valores = {}
        for campo in self.campos:
            if campo.tipo == "referencia":
                valores[campo.clave] = self._widgets[campo.clave].valor()
            else:
                valores[campo.clave] = self._vars[campo.clave].get()
        return valores

    def obtener_datos(self, incluir_llave=True) -> dict:
        """Valida y convierte. Lanza ErrorValidacion con todos los errores encontrados."""
        return validar(self.campos, self.valores_crudos(), incluir_llave)

    def cargar(self, datos: dict):
        for campo in self.campos:
            valor = datos.get(campo.clave)
            var = self._vars[campo.clave]
            if campo.tipo == "booleano":
                var.set(bool(valor))
            elif campo.tipo == "referencia":
                self._widgets[campo.clave].establecer(valor)
            elif campo.tipo == "fecha":
                var.set("" if valor is None else str(valor).replace("T", " ")[:16])
            else:
                var.set("" if valor is None else str(valor))

    def limpiar(self):
        for campo in self.campos:
            var = self._vars[campo.clave]
            if campo.tipo == "booleano":
                var.set(False)
            elif campo.tipo == "referencia":
                self._widgets[campo.clave].limpiar()
            else:
                var.set("")
        primero = self._widgets[self.campos[0].clave]
        if str(primero.cget("state")) != "disabled":
            primero.focus_set()

    def bloquear(self, clave):
        self._widgets[clave].configure(state="disabled")


class Ficha(ttk.LabelFrame):
    """Muestra TODA la informacion de un objeto en modo solo lectura."""

    def __init__(self, master, campos, titulo="Información del registro"):
        super().__init__(master, text=titulo, padding=12)
        self._filas = {}
        self.columnconfigure(1, weight=1)
        for i, campo in enumerate(campos):
            ttk.Label(self, text=campo.etiqueta + ":", style="Etiqueta.TLabel").grid(
                row=i, column=0, sticky="nw", padx=(0, 12), pady=2)
            valor = ttk.Label(self, text="—", wraplength=340, justify="left")
            valor.grid(row=i, column=1, sticky="w", pady=2)
            self._filas[campo.clave] = (campo, valor)

    def mostrar(self, datos: dict):
        for campo, etiqueta in self._filas.values():
            etiqueta.configure(text=formatear(campo.tipo, datos.get(campo.clave)))

    def limpiar(self):
        for _, etiqueta in self._filas.values():
            etiqueta.configure(text="—")


class Tabla(ttk.Frame):
    """Grilla con barras de desplazamiento. columnas = [(clave, titulo, ancho, tipo), ...]"""

    def __init__(self, master, columnas):
        super().__init__(master)
        self._columnas = columnas
        self.arbol = ttk.Treeview(self, columns=[c[0] for c in columnas], show="headings", height=14)
        for clave, titulo, ancho, tipo in columnas:
            self.arbol.heading(clave, text=titulo, anchor="w")
            alineacion = "e" if tipo in ("entero", "decimal") else "w"
            self.arbol.column(clave, width=ancho, minwidth=60, anchor=alineacion, stretch=True)
        barra_y = ttk.Scrollbar(self, orient="vertical", command=self.arbol.yview)
        barra_x = ttk.Scrollbar(self, orient="horizontal", command=self.arbol.xview)
        self.arbol.configure(yscrollcommand=barra_y.set, xscrollcommand=barra_x.set)
        self.arbol.grid(row=0, column=0, sticky="nsew")
        barra_y.grid(row=0, column=1, sticky="ns")
        barra_x.grid(row=1, column=0, sticky="ew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def cargar(self, filas):
        self.arbol.delete(*self.arbol.get_children())
        for fila in filas:
            valores = [formatear(tipo, fila.get(clave)) for clave, _, _, tipo in self._columnas]
            self.arbol.insert("", "end", values=valores)


class Buscador(ttk.LabelFrame):
    """Busqueda previa de UN objeto por ID o por nombre."""

    def __init__(self, master, al_buscar, titulo="Buscar registro"):
        super().__init__(master, text=titulo, padding=10)
        self._al_buscar = al_buscar
        ttk.Label(self, text="Buscar por").pack(side="left")
        self.criterio = ttk.Combobox(self, values=["ID", "Nombre"], state="readonly", width=9)
        self.criterio.set("ID")
        self.criterio.pack(side="left", padx=(6, 12))
        self.valor = ttk.Entry(self, width=30)
        self.valor.pack(side="left", fill="x", expand=True)
        self.valor.bind("<Return>", lambda _e: self._buscar())
        ttk.Button(self, text="Buscar", style="Primario.TButton", command=self._buscar).pack(side="left", padx=(10, 0))
        self.valor.focus_set()

    def _buscar(self):
        self._al_buscar(self.criterio.get(), self.valor.get().strip())
