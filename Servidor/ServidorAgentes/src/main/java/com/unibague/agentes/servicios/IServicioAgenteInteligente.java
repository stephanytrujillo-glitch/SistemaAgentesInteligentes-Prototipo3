package com.unibague.agentes.servicios;

import java.util.List;

import com.unibague.agentes.dto.ActualizarAgenteInteligenteInput;
import com.unibague.agentes.dto.AgenteInteligenteInput;
import com.unibague.agentes.dto.AgenteResumen;
import com.unibague.agentes.dto.Pagina;
import com.unibague.agentes.model.AgenteInteligente;
import com.unibague.agentes.model.EstadoOperativo;

/** Logica de negocio del agente inteligente (maestro). */
public interface IServicioAgenteInteligente {

    Pagina<AgenteResumen> listarResumen(EstadoOperativo estado, Integer pagina, Integer tamano);

    Pagina<AgenteInteligente> listarPorEstadoYAutonomia(EstadoOperativo estado, double autonomiaMinima,
                                                       Integer pagina, Integer tamano);

    List<AgenteInteligente> buscarOpciones(String texto, Integer limite);

    AgenteInteligente buscarPorId(int idAgente);

    AgenteInteligente buscarPorNombre(String nombre);

    AgenteInteligente crear(AgenteInteligenteInput input);

    AgenteInteligente actualizar(int idAgente, ActualizarAgenteInteligenteInput input);

    String eliminar(int idAgente);
}
