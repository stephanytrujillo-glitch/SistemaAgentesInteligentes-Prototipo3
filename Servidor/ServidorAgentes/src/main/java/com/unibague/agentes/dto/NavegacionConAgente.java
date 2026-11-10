package com.unibague.agentes.dto;

import java.time.LocalDateTime;

import org.springframework.data.annotation.Id;

import com.unibague.agentes.model.EstadoOperativo;

/**
 * Resultado de las consultas personalizadas de listado de la coleccion B:
 * TODOS los atributos del agente de navegacion + DOS atributos del agente
 * inteligente (maestro): su nombre y su estado operativo. Se arma con $lookup.
 */
public class NavegacionConAgente {

    @Id
    private int idNavegacion;
    private String nombre;
    private String origen;
    private String destino;
    private double precisionGPS;
    private Double velocidadMaxima;
    private LocalDateTime fechaUltimaCalibracion;
    private boolean rutaOptimizada;
    private Integer idAgenteInteligente;
    // --- datos que vienen de la coleccion maestro ---
    private String nombreAgente;
    private EstadoOperativo estadoAgente;

    public NavegacionConAgente() {
    }

    public int getIdNavegacion() { return idNavegacion; }
    public String getNombre() { return nombre; }
    public String getOrigen() { return origen; }
    public String getDestino() { return destino; }
    public double getPrecisionGPS() { return precisionGPS; }
    public Double getVelocidadMaxima() { return velocidadMaxima; }
    public LocalDateTime getFechaUltimaCalibracion() { return fechaUltimaCalibracion; }
    public boolean isRutaOptimizada() { return rutaOptimizada; }
    public Integer getIdAgenteInteligente() { return idAgenteInteligente; }
    public String getNombreAgente() { return nombreAgente; }
    public EstadoOperativo getEstadoAgente() { return estadoAgente; }
}
