package com.unibague.agentes.model;

import java.time.LocalDateTime;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * Clase MAESTRO. Se guarda en la coleccion "agentes_inteligentes".
 * No tiene lista de detalles: la relacion la lleva cada AgenteNavegacion
 * (Collection B --> Collection A), como en la figura 2 del enunciado.
 */
@Document(collection = "agentes_inteligentes")
public class AgenteInteligente {

    @Id
    private int idAgente;                       // int           - llave primaria
    @Indexed(unique = true)
    private String nombre;                      // String        - obligatorio, unico
    private double nivelAutonomia;              // double        - obligatorio (0 - 100)
    @Indexed
    private EstadoOperativo estadoOperativo;    // enum          - obligatorio
    private Double nivelConfianza;              // double        - OPCIONAL (0 - 100)
    private LocalDateTime fechaRegistro;        // LocalDateTime - obligatorio (no futura)
    private boolean aprendizajeContinuo;        // boolean       - obligatorio (atributo de eleccion)
    private String descripcion;                 // String        - OPCIONAL (max 200)

    public AgenteInteligente() {
    }

    private AgenteInteligente(Builder b) {
        this.idAgente = b.idAgente;
        this.nombre = b.nombre;
        this.nivelAutonomia = b.nivelAutonomia;
        this.estadoOperativo = b.estadoOperativo;
        this.nivelConfianza = b.nivelConfianza;
        this.fechaRegistro = b.fechaRegistro;
        this.aprendizajeContinuo = b.aprendizajeContinuo;
        this.descripcion = b.descripcion;
    }

    public static Builder builder() {
        return new Builder();
    }

    public int getIdAgente() { return idAgente; }
    public void setIdAgente(int idAgente) { this.idAgente = idAgente; }
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
    public double getNivelAutonomia() { return nivelAutonomia; }
    public void setNivelAutonomia(double nivelAutonomia) { this.nivelAutonomia = nivelAutonomia; }
    public EstadoOperativo getEstadoOperativo() { return estadoOperativo; }
    public void setEstadoOperativo(EstadoOperativo estadoOperativo) { this.estadoOperativo = estadoOperativo; }
    public Double getNivelConfianza() { return nivelConfianza; }
    public void setNivelConfianza(Double nivelConfianza) { this.nivelConfianza = nivelConfianza; }
    public LocalDateTime getFechaRegistro() { return fechaRegistro; }
    public void setFechaRegistro(LocalDateTime fechaRegistro) { this.fechaRegistro = fechaRegistro; }
    public boolean isAprendizajeContinuo() { return aprendizajeContinuo; }
    public void setAprendizajeContinuo(boolean aprendizajeContinuo) { this.aprendizajeContinuo = aprendizajeContinuo; }
    public String getDescripcion() { return descripcion; }
    public void setDescripcion(String descripcion) { this.descripcion = descripcion; }

    /** Patron Builder para construir agentes de forma legible. */
    public static class Builder {
        private int idAgente;
        private String nombre;
        private double nivelAutonomia;
        private EstadoOperativo estadoOperativo;
        private Double nivelConfianza;
        private LocalDateTime fechaRegistro;
        private boolean aprendizajeContinuo;
        private String descripcion;

        public Builder idAgente(int v) { this.idAgente = v; return this; }
        public Builder nombre(String v) { this.nombre = v; return this; }
        public Builder nivelAutonomia(double v) { this.nivelAutonomia = v; return this; }
        public Builder estadoOperativo(EstadoOperativo v) { this.estadoOperativo = v; return this; }
        public Builder nivelConfianza(Double v) { this.nivelConfianza = v; return this; }
        public Builder fechaRegistro(LocalDateTime v) { this.fechaRegistro = v; return this; }
        public Builder aprendizajeContinuo(boolean v) { this.aprendizajeContinuo = v; return this; }
        public Builder descripcion(String v) { this.descripcion = v; return this; }

        public AgenteInteligente build() {
            return new AgenteInteligente(this);
        }
    }
}
