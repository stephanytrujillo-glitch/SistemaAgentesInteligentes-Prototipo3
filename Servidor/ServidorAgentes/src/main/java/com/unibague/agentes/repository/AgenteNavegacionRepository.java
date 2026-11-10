package com.unibague.agentes.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.mongodb.repository.Aggregation;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

import com.unibague.agentes.dto.NavegacionConAgente;
import com.unibague.agentes.model.AgenteNavegacion;

/**
 * Acceso a la coleccion "agentes_navegacion" (Spring Data MongoDB).
 * Listados PAGINADOS: el $lookup al maestro se hace solo sobre la pagina pedida.
 */
public interface AgenteNavegacionRepository extends MongoRepository<AgenteNavegacion, Integer> {

    /** Busqueda individual por nombre (sin distinguir mayusculas). El nombre es unico. */
    Optional<AgenteNavegacion> findByNombreIgnoreCase(String nombre);

    /** Agentes de navegacion de un agente inteligente (se usa al eliminar el maestro). */
    @Query("{ 'idAgenteInteligente': ?0 }")
    List<AgenteNavegacion> buscarPorAgenteInteligente(int idAgenteInteligente);

    /** Total para la paginacion del filtro por destino. */
    @Query(value = "{ 'destino': { $regex: ?0, $options: 'i' } }", count = true)
    long contarPorDestino(String patronDestino);

    /** Total para la paginacion del filtro por agente (usa el indice de idAgenteInteligente). */
    long countByIdAgenteInteligente(Integer idAgenteInteligente);

    /**
     * CONSULTA PERSONALIZADA (detalle + 2 atributos del maestro), filtrada por destino y paginada.
     * Si el texto del destino llega vacio, lista TODOS.
     */
    @Aggregation(pipeline = {
            "{ $match: { destino: { $regex: ?0, $options: 'i' } } }",
            "{ $sort: { _id: 1 } }",
            "{ $skip: ?1 }",
            "{ $limit: ?2 }",
            "{ $lookup: { from: 'agentes_inteligentes', localField: 'idAgenteInteligente', foreignField: '_id', as: 'agente' } }",
            "{ $unwind: { path: '$agente', preserveNullAndEmptyArrays: true } }",
            "{ $project: { nombre: 1, origen: 1, destino: 1, precisionGPS: 1, velocidadMaxima: 1, fechaUltimaCalibracion: 1, rutaOptimizada: 1, idAgenteInteligente: 1, nombreAgente: '$agente.nombre', estadoAgente: '$agente.estadoOperativo' } }"
    })
    List<NavegacionConAgente> listarConAgentePorDestino(String patronDestino, long saltar, int limite);

    /** CONSULTA PERSONALIZADA (detalle + 2 atributos del maestro), filtrada por agente y paginada. */
    @Aggregation(pipeline = {
            "{ $match: { idAgenteInteligente: ?0 } }",
            "{ $sort: { _id: 1 } }",
            "{ $skip: ?1 }",
            "{ $limit: ?2 }",
            "{ $lookup: { from: 'agentes_inteligentes', localField: 'idAgenteInteligente', foreignField: '_id', as: 'agente' } }",
            "{ $unwind: { path: '$agente', preserveNullAndEmptyArrays: true } }",
            "{ $project: { nombre: 1, origen: 1, destino: 1, precisionGPS: 1, velocidadMaxima: 1, fechaUltimaCalibracion: 1, rutaOptimizada: 1, idAgenteInteligente: 1, nombreAgente: '$agente.nombre', estadoAgente: '$agente.estadoOperativo' } }"
    })
    List<NavegacionConAgente> listarConAgentePorAgente(int idAgenteInteligente, long saltar, int limite);
}
