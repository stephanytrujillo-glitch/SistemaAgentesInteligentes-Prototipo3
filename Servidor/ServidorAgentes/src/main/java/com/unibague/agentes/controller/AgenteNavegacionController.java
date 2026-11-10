package com.unibague.agentes.controller;

import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

import com.unibague.agentes.dto.ActualizarAgenteNavegacionInput;
import com.unibague.agentes.dto.AgenteNavegacionInput;
import com.unibague.agentes.dto.NavegacionConAgente;
import com.unibague.agentes.dto.Pagina;
import com.unibague.agentes.model.AgenteNavegacion;
import com.unibague.agentes.servicios.IServicioAgenteNavegacion;

import jakarta.validation.Valid;

/** Expone el CRUD del agente de navegacion como servicio web GraphQL. */
@Controller
public class AgenteNavegacionController {

    private final IServicioAgenteNavegacion servicio;

    public AgenteNavegacionController(IServicioAgenteNavegacion servicio) {
        this.servicio = servicio;
    }

    /** Listar PAGINADO con parametro destino (vacio = todos): detalle + 2 atributos del maestro. */
    @QueryMapping
    public Pagina<NavegacionConAgente> navegacionesConAgente(@Argument String destino,
                                                            @Argument Integer pagina, @Argument Integer tamano) {
        return servicio.listarConAgentePorDestino(destino, pagina, tamano);
    }

    /** Listar PAGINADO con parametro agente inteligente. */
    @QueryMapping
    public Pagina<NavegacionConAgente> navegacionesPorAgente(@Argument int idAgente,
                                                            @Argument Integer pagina, @Argument Integer tamano) {
        return servicio.listarConAgentePorAgente(idAgente, pagina, tamano);
    }

    @QueryMapping
    public AgenteNavegacion agenteNavegacionPorId(@Argument int idNavegacion) {
        return servicio.buscarPorId(idNavegacion);
    }

    @QueryMapping
    public AgenteNavegacion agenteNavegacionPorNombre(@Argument String nombre) {
        return servicio.buscarPorNombre(nombre);
    }

    @MutationMapping
    public AgenteNavegacion crearAgenteNavegacion(@Argument @Valid AgenteNavegacionInput input) {
        return servicio.crear(input);
    }

    @MutationMapping
    public AgenteNavegacion actualizarAgenteNavegacion(@Argument int idNavegacion,
                                                       @Argument @Valid ActualizarAgenteNavegacionInput input) {
        return servicio.actualizar(idNavegacion, input);
    }

    @MutationMapping
    public String eliminarAgenteNavegacion(@Argument int idNavegacion) {
        return servicio.eliminar(idNavegacion);
    }
}
