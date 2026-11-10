package com.unibague.agentes.servicios;

import com.unibague.agentes.dto.ActualizarAgenteNavegacionInput;
import com.unibague.agentes.dto.AgenteNavegacionInput;
import com.unibague.agentes.dto.NavegacionConAgente;
import com.unibague.agentes.dto.Pagina;
import com.unibague.agentes.model.AgenteNavegacion;

/** Logica de negocio del agente de navegacion (detalle). */
public interface IServicioAgenteNavegacion {

    Pagina<NavegacionConAgente> listarConAgentePorDestino(String destino, Integer pagina, Integer tamano);

    Pagina<NavegacionConAgente> listarConAgentePorAgente(int idAgente, Integer pagina, Integer tamano);

    AgenteNavegacion buscarPorId(int idNavegacion);

    AgenteNavegacion buscarPorNombre(String nombre);

    AgenteNavegacion crear(AgenteNavegacionInput input);

    AgenteNavegacion actualizar(int idNavegacion, ActualizarAgenteNavegacionInput input);

    String eliminar(int idNavegacion);
}
