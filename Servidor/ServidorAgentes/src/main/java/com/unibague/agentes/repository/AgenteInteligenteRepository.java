package com.unibague.agentes.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.Aggregation;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

import com.unibague.agentes.dto.AgenteResumen;
import com.unibague.agentes.model.AgenteInteligente;
import com.unibague.agentes.model.EstadoOperativo;

/**
 * Acceso a la coleccion "agentes_inteligentes" (Spring Data MongoDB).
 * Todas las consultas de listado son PAGINADAS: $sort -> $skip -> $limit se aplican ANTES
 * del $lookup, para que la union con la otra coleccion solo se haga sobre la pagina pedida.
 */
public interface AgenteInteligenteRepository extends MongoRepository<AgenteInteligente, Integer> {

    /** Busqueda individual por nombre (sin distinguir mayusculas). El nombre es unico. */
    Optional<AgenteInteligente> findByNombreIgnoreCase(String nombre);

    /** Total de agentes con un estado (usa el indice de estadoOperativo). */
    long countByEstadoOperativo(EstadoOperativo estado);

    /** Opciones para escoger un agente: busca por nombre y trae solo id y nombre, con limite. */
    @Query(value = "{ 'nombre': { $regex: ?0, $options: 'i' } }", fields = "{ 'nombre': 1 }")
    List<AgenteInteligente> buscarOpciones(String patronNombre, Pageable pagina);

    /** CONSULTA PERSONALIZADA con dos parametros, paginada. */
    @Query(value = "{ 'estadoOperativo': ?0, 'nivelAutonomia': { $gte: ?1 } }", sort = "{ 'nivelAutonomia': -1 }")
    List<AgenteInteligente> buscarPorEstadoYAutonomiaMinima(String estado, double autonomiaMinima, Pageable pagina);

    @Query(value = "{ 'estadoOperativo': ?0, 'nivelAutonomia': { $gte: ?1 } }", count = true)
    long contarPorEstadoYAutonomiaMinima(String estado, double autonomiaMinima);

    /**
     * CONSULTA PERSONALIZADA (maestro + 2 datos del detalle), paginada:
     * cantidad de agentes de navegacion y su precision GPS promedio.
     */
    @Aggregation(pipeline = {
            "{ $sort: { _id: 1 } }",
            "{ $skip: ?0 }",
            "{ $limit: ?1 }",
            "{ $lookup: { from: 'agentes_navegacion', localField: '_id', foreignField: 'idAgenteInteligente', as: 'navs' } }",
            "{ $project: { nombre: 1, nivelAutonomia: 1, estadoOperativo: 1, nivelConfianza: 1, fechaRegistro: 1, aprendizajeContinuo: 1, descripcion: 1, cantidadNavegaciones: { $size: '$navs' }, precisionPromedio: { $ifNull: [ { $avg: '$navs.precisionGPS' }, 0 ] } } }"
    })
    List<AgenteResumen> listarResumen(long saltar, int limite);

    /** Igual que la anterior pero FILTRADA por estado operativo. */
    @Aggregation(pipeline = {
            "{ $match: { estadoOperativo: ?0 } }",
            "{ $sort: { _id: 1 } }",
            "{ $skip: ?1 }",
            "{ $limit: ?2 }",
            "{ $lookup: { from: 'agentes_navegacion', localField: '_id', foreignField: 'idAgenteInteligente', as: 'navs' } }",
            "{ $project: { nombre: 1, nivelAutonomia: 1, estadoOperativo: 1, nivelConfianza: 1, fechaRegistro: 1, aprendizajeContinuo: 1, descripcion: 1, cantidadNavegaciones: { $size: '$navs' }, precisionPromedio: { $ifNull: [ { $avg: '$navs.precisionGPS' }, 0 ] } } }"
    })
    List<AgenteResumen> listarResumenPorEstado(String estado, long saltar, int limite);
}
