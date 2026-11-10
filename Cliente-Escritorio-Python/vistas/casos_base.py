"""Ventanas base de los 5 casos de uso (patron Template Method). Cada ventana implementa UN solo caso de uso.

Las subclases de cada paquete (agente_inteligente / agente_navegacion) solo indican
la clase que gestionan: campos, servicio, columnas y filtros.
"""
from tkinter import messagebox, ttk

from modelo.validador import ErrorValidacion
from servicios.notificador import AGENTE_INTELIGENTE, Notificador
from vistas.componentes import Buscador, ComboReferencia, Ficha, Formulario, Tabla
from vistas.ventana_base import VentanaBase


class _ConEntidad:
    nombre_entidad = ""     # ej. "agente inteligente"
    nombre_plural = ""      # ej. "agentes inteligentes"
    campos = []
    servicio_cls = None
    eventos_observados = []

    def _crear_servicio(self):
        self.servicio = self.servicio_cls()

    def proveedor_referencias(self):
        """Funcion que devuelve [(id, nombre)] para los campos de tipo referencia."""
        return None

    def buscar_objeto(self, criterio, valor):
        if not valor:
            raise ErrorValidacion([f"Escriba el {criterio.lower()} a buscar."])
        if criterio == "ID":
            try:
                id_ = int(valor)
            except ValueError:
                raise ErrorValidacion(["El ID debe ser un número entero."])
            if id_ <= 0:
                raise ErrorValidacion(["El ID debe ser un entero positivo."])
            return self.servicio.buscar_por_id(id_)
        return self.servicio.buscar_por_nombre(valor)

    def llave_de(self, objeto):
        return getattr(objeto, self.servicio.LLAVE)


def _observar_referencias(ventana, formulario):
    """Observer: si cambian los agentes inteligentes, recarga las opciones del campo de referencia."""
    if ventana.proveedor_referencias() is None:
        return

    def recargar(_evento):
        if ventana.winfo_exists():
            formulario.recargar_referencias()

    Notificador().suscribir(AGENTE_INTELIGENTE, recargar)
    ventana.bind("<Destroy>", lambda e: Notificador().desuscribir(AGENTE_INTELIGENTE, recargar)
                 if e.widget is ventana else None, add="+")


# --------------------------------------------------------------------------- Adicionar
class VentanaAdicionar(_ConEntidad, VentanaBase):

    def __init__(self, master):
        VentanaBase.__init__(self, master, f"Adicionar {self.nombre_entidad}",
                             "Complete los datos y guarde el nuevo registro.", 820, 500)
        self._crear_servicio()
        self.formulario = Formulario(self.cuerpo, self.campos, self.proveedor_referencias())
        self.formulario.pack(fill="x")
        _observar_referencias(self, self.formulario)

        botones = ttk.Frame(self.cuerpo)
        botones.pack(fill="x", pady=(18, 0))
        ttk.Button(botones, text="Guardar", style="Primario.TButton", command=self.guardar).pack(side="right")
        ttk.Button(botones, text="Limpiar", command=self.formulario.limpiar).pack(side="right", padx=8)

    def guardar(self):
        def accion():
            datos = self.formulario.obtener_datos()
            objeto = self.servicio.crear(datos)
            messagebox.showinfo("Registro guardado",
                                f"El {self.nombre_entidad} '{objeto.nombre}' se guardó correctamente.",
                                parent=self)
            self.formulario.limpiar()
        self.ejecutar(accion)


# --------------------------------------------------------------------------- Consultar
class VentanaConsultar(_ConEntidad, VentanaBase):

    def __init__(self, master):
        VentanaBase.__init__(self, master, f"Consultar {self.nombre_entidad}",
                             "Consulte UN registro escribiendo su ID o su nombre.", 640, 520)
        self._crear_servicio()
        Buscador(self.cuerpo, self._buscar).pack(fill="x")
        self.ficha = Ficha(self.cuerpo, self.campos, f"Datos del {self.nombre_entidad}")
        self.ficha.pack(fill="both", expand=True, pady=(14, 0))

    def _buscar(self, criterio, valor):
        self.ficha.limpiar()

        def accion():
            objeto = self.buscar_objeto(criterio, valor)
            self.ficha.mostrar(objeto.como_dict())
        self.ejecutar(accion)


# --------------------------------------------------------------------------- Eliminar
class VentanaEliminar(_ConEntidad, VentanaBase):
    aviso_eliminar = ""

    def __init__(self, master):
        VentanaBase.__init__(self, master, f"Eliminar {self.nombre_entidad}",
                             "Primero busque el registro y revise toda su información.", 640, 560)
        self._crear_servicio()
        self._actual = None
        Buscador(self.cuerpo, self._buscar).pack(fill="x")
        self.ficha = Ficha(self.cuerpo, self.campos, "Registro a eliminar")
        self.ficha.pack(fill="both", expand=True, pady=(14, 0))

        botones = ttk.Frame(self.cuerpo)
        botones.pack(fill="x", pady=(14, 0))
        self.boton = ttk.Button(botones, text="Eliminar", style="Peligro.TButton",
                                command=self._eliminar, state="disabled")
        self.boton.pack(side="right")

    def _reiniciar(self):
        self._actual = None
        self.ficha.limpiar()
        self.boton.configure(state="disabled")

    def _buscar(self, criterio, valor):
        self._reiniciar()

        def accion():
            self._actual = self.buscar_objeto(criterio, valor)
            self.ficha.mostrar(self._actual.como_dict())
            self.boton.configure(state="normal")
        self.ejecutar(accion)

    def _eliminar(self):
        if self._actual is None:
            return
        llave = self.llave_de(self._actual)
        pregunta = (f"¿Eliminar el {self.nombre_entidad} '{self._actual.nombre}' (ID {llave})?\n"
                    f"{self.aviso_eliminar}\nEsta acción no se puede deshacer.")
        if not messagebox.askyesno("Confirmar eliminación", pregunta, icon="warning", parent=self):
            return

        def accion():
            mensaje = self.servicio.eliminar(llave)
            messagebox.showinfo("Registro eliminado", mensaje, parent=self)
            self._reiniciar()
        self.ejecutar(accion)


# --------------------------------------------------------------------------- Actualizar
class VentanaActualizar(_ConEntidad, VentanaBase):

    def __init__(self, master):
        VentanaBase.__init__(self, master, f"Actualizar {self.nombre_entidad}",
                             "Busque el registro, revise su información actual y modifique uno o varios atributos.",
                             1060, 600)
        self._crear_servicio()
        self._actual = None
        Buscador(self.cuerpo, self._buscar).pack(fill="x")

        contenido = ttk.Frame(self.cuerpo)
        contenido.pack(fill="both", expand=True, pady=(14, 0))
        self.ficha = Ficha(contenido, self.campos, "Información actual")
        self.ficha.pack(side="left", fill="both", expand=True)

        marco = ttk.LabelFrame(contenido, text="Nuevos datos", padding=12)
        marco.pack(side="left", fill="both", expand=True, padx=(14, 0))
        self.formulario = Formulario(marco, self.campos, self.proveedor_referencias(), mostrar_ayuda=False)
        self.formulario.pack(fill="x")
        llave = next(c.clave for c in self.campos if c.es_llave)
        self.formulario.bloquear(llave)  # la llave primaria no se modifica
        _observar_referencias(self, self.formulario)

        botones = ttk.Frame(self.cuerpo)
        botones.pack(fill="x", pady=(14, 0))
        self.boton = ttk.Button(botones, text="Guardar cambios", style="Primario.TButton",
                                command=self._guardar, state="disabled")
        self.boton.pack(side="right")

    def _buscar(self, criterio, valor):
        self._actual = None
        self.ficha.limpiar()
        self.formulario.limpiar()
        self.boton.configure(state="disabled")

        def accion():
            self._actual = self.buscar_objeto(criterio, valor)
            self.ficha.mostrar(self._actual.como_dict())
            self.formulario.recargar_referencias()
            self.formulario.cargar(self._actual.como_dict())
            self.boton.configure(state="normal")
        self.ejecutar(accion)

    def _guardar(self):
        if self._actual is None:
            return

        def accion():
            datos = self.formulario.obtener_datos(incluir_llave=False)
            llave = self.llave_de(self._actual)
            if not messagebox.askyesno("Confirmar actualización",
                                       f"¿Guardar los cambios del {self.nombre_entidad} con ID {llave}?",
                                       parent=self):
                return
            self._actual = self.servicio.actualizar(llave, datos)
            self.ficha.mostrar(self._actual.como_dict())
            self.formulario.cargar(self._actual.como_dict())
            messagebox.showinfo("Registro actualizado",
                                f"El {self.nombre_entidad} '{self._actual.nombre}' se actualizó correctamente.",
                                parent=self)
        self.ejecutar(accion)


# --------------------------------------------------------------------------- Listar
TAMANOS_PAGINA = [10, 25, 50, 100]


class VentanaListar(_ConEntidad, VentanaBase):
    """Listado PAGINADO: el servidor solo envia la pagina que se ve (por defecto 25 filas)
    y el total. Asi la ventana responde igual con 10 registros o con miles."""

    columnas = []   # [(clave, titulo, ancho, tipo)]
    filtros = []    # [{"clave": None|str, "etiqueta": str, "tipo": None|"texto"|"opcion"|"referencia", "opciones": []}]

    def __init__(self, master):
        VentanaBase.__init__(self, master, f"Listar {self.nombre_plural}",
                             "Registros en una grilla paginada, con filtro por un parámetro.", 1180, 640)
        self._crear_servicio()
        self._pagina = 0
        self._total_paginas = 1
        self._consulta = (self.filtros[0], None)   # filtro y valor de la ultima consulta aplicada

        barra = ttk.LabelFrame(self.cuerpo, text="Filtro", padding=10)
        barra.pack(fill="x")
        ttk.Label(barra, text="Filtrar por").pack(side="left")
        self.combo_filtro = ttk.Combobox(barra, state="readonly", width=20,
                                         values=[f["etiqueta"] for f in self.filtros])
        self.combo_filtro.current(0)
        self.combo_filtro.pack(side="left", padx=(6, 12))
        self.combo_filtro.bind("<<ComboboxSelected>>", self._cambio_filtro)
        ttk.Label(barra, text="Valor").pack(side="left")

        # el campo de valor cambia segun el filtro: texto/opciones o selector de agente con busqueda
        self._marco_valor = ttk.Frame(barra)
        self._marco_valor.pack(side="left", padx=(6, 12))
        self.combo_valor = ttk.Combobox(self._marco_valor, width=30)
        self.combo_valor.bind("<Return>", lambda _e: self.aplicar())
        self.combo_ref = None
        if any(f["tipo"] == "referencia" for f in self.filtros):
            self.combo_ref = ComboReferencia(self._marco_valor, self.proveedor_referencias(),
                                             permitir_vacio=False, width=30)
            self.combo_ref.bind("<Return>", lambda _e: self.aplicar(), add="+")

        ttk.Button(barra, text="Aplicar filtro", style="Primario.TButton", command=self.aplicar).pack(side="left")
        ttk.Button(barra, text="Listar todos", command=self.listar_todos).pack(side="left", padx=(8, 0))

        self.tabla = Tabla(self.cuerpo, self.columnas)
        self.tabla.pack(fill="both", expand=True, pady=(12, 0))

        # ---- barra de paginacion
        paginacion = ttk.Frame(self.cuerpo)
        paginacion.pack(fill="x", pady=(8, 0))
        self.estado = ttk.Label(paginacion, text="", style="Ayuda.TLabel")
        self.estado.pack(side="left")
        self.boton_siguiente = ttk.Button(paginacion, text="Siguiente ▶", command=lambda: self._ir_a(self._pagina + 1))
        self.boton_siguiente.pack(side="right")
        self.etiqueta_pagina = ttk.Label(paginacion, text="Página 1 de 1")
        self.etiqueta_pagina.pack(side="right", padx=10)
        self.boton_anterior = ttk.Button(paginacion, text="◀ Anterior", command=lambda: self._ir_a(self._pagina - 1))
        self.boton_anterior.pack(side="right")
        self.combo_tamano = ttk.Combobox(paginacion, state="readonly", width=5, values=TAMANOS_PAGINA)
        self.combo_tamano.set(25)
        self.combo_tamano.pack(side="right", padx=(0, 16))
        self.combo_tamano.bind("<<ComboboxSelected>>", lambda _e: self._ir_a(0))
        ttk.Label(paginacion, text="Filas por página").pack(side="right", padx=(0, 6))

        self._cambio_filtro()
        self.after(150, self.listar_todos)

        # Patron Observer: la grilla se refresca sola cuando otra ventana cambia los datos
        for evento in self.eventos_observados:
            Notificador().suscribir(evento, self._datos_cambiaron)
        self.bind("<Destroy>", self._al_destruir, add="+")

    # ---------------------------------------------------------------- Observer
    def _datos_cambiaron(self, evento):
        if not self.winfo_exists():
            return
        if evento == AGENTE_INTELIGENTE and self.combo_ref is not None:
            self.combo_ref.refrescar(self.combo_ref.get())
        # misma pagina y mismo filtro; si falla, se muestra el mensaje en vez de un error en consola
        self.after(0, lambda: self.ejecutar(lambda: self._consultar_pagina(self._pagina)))

    def _al_destruir(self, evento):
        if evento.widget is self:
            for nombre in self.eventos_observados:
                Notificador().desuscribir(nombre, self._datos_cambiaron)

    # ---------------------------------------------------------------- filtro
    def _filtro_actual(self):
        return self.filtros[self.combo_filtro.current()]

    def _cambio_filtro(self, *_):
        filtro = self._filtro_actual()
        for widget in self._marco_valor.winfo_children():
            widget.pack_forget()
        if filtro["tipo"] == "referencia":
            self.combo_ref.limpiar()
            self.combo_ref.pack()
            return
        self.combo_valor.pack()
        self.combo_valor.set("")
        if filtro["tipo"] is None:
            self.combo_valor.configure(state="disabled", values=[])
        elif filtro["tipo"] == "texto":
            self.combo_valor.configure(state="normal", values=[])
            self.combo_valor.focus_set()
        elif filtro["tipo"] == "opcion":
            self.combo_valor.configure(state="readonly", values=filtro["opciones"])

    def _valor_filtro(self, filtro):
        if filtro["tipo"] is None:
            return None
        if filtro["tipo"] == "referencia":
            valor = self.combo_ref.valor()
            if not isinstance(valor, int):
                raise ErrorValidacion(["Escriba el nombre o el ID del agente y elíjalo de la lista."])
            return valor
        texto = self.combo_valor.get().strip()
        if not texto:
            raise ErrorValidacion([f"Escriba o seleccione un valor para '{filtro['etiqueta']}'."])
        return texto

    # ---------------------------------------------------------------- consulta paginada
    def aplicar(self):
        """Toma el filtro de la barra y muestra la PRIMERA pagina."""
        filtro = self._filtro_actual()

        def accion():
            self._consulta = (filtro, self._valor_filtro(filtro))
            self._consultar_pagina(0)
        self.ejecutar(accion)

    def listar_todos(self):
        self.combo_filtro.current(0)
        self._cambio_filtro()
        self.aplicar()

    def _ir_a(self, pagina):
        if 0 <= pagina < self._total_paginas or pagina == 0:
            self.ejecutar(lambda: self._consultar_pagina(pagina))

    def _consultar_pagina(self, pagina):
        filtro, valor = self._consulta
        tamano = int(self.combo_tamano.get())
        resultado = self.consultar(filtro["clave"], valor, pagina, tamano)
        if resultado["elementos"] == [] and pagina > 0 and resultado["total"] > 0:
            # la pagina quedo vacia (p. ej. se elimino su ultimo registro): ir a la ultima
            return self._consultar_pagina(resultado["totalPaginas"] - 1)

        self._pagina = resultado["pagina"]
        self._total_paginas = resultado["totalPaginas"]
        self.tabla.cargar(resultado["elementos"])

        total = resultado["total"]
        desde = self._pagina * tamano + 1 if total else 0
        hasta = self._pagina * tamano + len(resultado["elementos"])
        detalle = "" if filtro["tipo"] is None else f" · filtro {filtro['etiqueta'].lower()}"
        self.estado.configure(text=f"Mostrando {desde}–{hasta} de {total:,} registro(s){detalle}".replace(",", "."))
        self.etiqueta_pagina.configure(text=f"Página {self._pagina + 1} de {self._total_paginas}")
        self.boton_anterior.configure(state="normal" if self._pagina > 0 else "disabled")
        self.boton_siguiente.configure(state="normal" if self._pagina + 1 < self._total_paginas else "disabled")
        return resultado

    def consultar(self, clave_filtro, valor, pagina, tamano):
        """Lo implementa cada clase: devuelve una pagina {elementos, total, pagina, tamano, totalPaginas}."""
        raise NotImplementedError
