package com.unibague.agentes.controller;

import java.util.List;

import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

import com.unibague.agentes.dto.ActualizarAgenteInteligenteInput;
import com.unibague.agentes.dto.AgenteInteligenteInput;
import com.unibague.agentes.dto.AgenteResumen;
import com.unibague.agentes.dto.Pagina;
import com.unibague.agentes.model.AgenteInteligente;
import com.unibague.agentes.model.EstadoOperativo;
import com.unibague.agentes.servicios.IServicioAgenteInteligente;

import jakarta.validation.Valid;

/** Expone el CRUD del agente inteligente como servicio web GraphQL. */
@Controller
public class AgenteInteligenteController {

    private final IServicioAgenteInteligente servicio;

    public AgenteInteligenteController(IServicioAgenteInteligente servicio) {
        this.servicio = servicio;
    }

    /** Listar con parametro opcional y PAGINADO (maestro + 2 datos del detalle). */
    @QueryMapping
    public Pagina<AgenteResumen> agentesInteligentesResumen(@Argument EstadoOperativo estado,
                                                           @Argument Integer pagina, @Argument Integer tamano) {
        return servicio.listarResumen(estado, pagina, tamano);
    }

    @QueryMapping
    public Pagina<AgenteInteligente> agentesPorEstadoYAutonomia(@Argument EstadoOperativo estado,
                                                               @Argument double autonomiaMinima,
                                                               @Argument Integer pagina, @Argument Integer tamano) {
        return servicio.listarPorEstadoYAutonomia(estado, autonomiaMinima, pagina, tamano);
    }

    /** Pocas opciones (busqueda por nombre o ID) para escoger un agente en los formularios. */
    @QueryMapping
    public List<AgenteInteligente> agentesInteligentesOpciones(@Argument String texto, @Argument Integer limite) {
        return servicio.buscarOpciones(texto, limite);
    }

    @QueryMapping
    public AgenteInteligente agenteInteligentePorId(@Argument int idAgente) {
        return servicio.buscarPorId(idAgente);
    }

    @QueryMapping
    public AgenteInteligente agenteInteligentePorNombre(@Argument String nombre) {
        return servicio.buscarPorNombre(nombre);
    }

    @MutationMapping
    public AgenteInteligente crearAgenteInteligente(@Argument @Valid AgenteInteligenteInput input) {
        return servicio.crear(input);
    }

    @MutationMapping
    public AgenteInteligente actualizarAgenteInteligente(@Argument int idAgente,
                                                         @Argument @Valid ActualizarAgenteInteligenteInput input) {
        return servicio.actualizar(idAgente, input);
    }

    @MutationMapping
    public String eliminarAgenteInteligente(@Argument int idAgente) {
        return servicio.eliminar(idAgente);
    }
}
