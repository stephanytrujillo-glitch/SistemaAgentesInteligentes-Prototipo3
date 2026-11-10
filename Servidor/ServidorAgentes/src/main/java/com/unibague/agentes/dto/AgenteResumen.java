package com.unibague.agentes.dto;

import java.time.LocalDateTime;

import org.springframework.data.annotation.Id;

import com.unibague.agentes.model.EstadoOperativo;

/**
 * Resultado de la consulta personalizada "agentesInteligentesResumen":
 * TODOS los datos del maestro + DOS datos calculados del detalle
 * (cantidad de agentes de navegacion y su precision GPS promedio).
 */
public class AgenteResumen {

    @Id
    private int idAgente;
    private String nombre;
    private double nivelAutonomia;
    private EstadoOperativo estadoOperativo;
    private Double nivelConfianza;
    private LocalDateTime fechaRegistro;
    private boolean aprendizajeContinuo;
    private String descripcion;
    // --- datos que vienen de la coleccion detalle ---
    private int cantidadNavegaciones;
    private double precisionPromedio;

    public AgenteResumen() {
    }

    public int getIdAgente() { return idAgente; }
    public String getNombre() { return nombre; }
    public double getNivelAutonomia() { return nivelAutonomia; }
    public EstadoOperativo getEstadoOperativo() { return estadoOperativo; }
    public Double getNivelConfianza() { return nivelConfianza; }
    public LocalDateTime getFechaRegistro() { return fechaRegistro; }
    public boolean isAprendizajeContinuo() { return aprendizajeContinuo; }
    public String getDescripcion() { return descripcion; }
    public int getCantidadNavegaciones() { return cantidadNavegaciones; }
    public double getPrecisionPromedio() { return precisionPromedio; }
}
