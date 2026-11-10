package com.unibague.agentes.model;

import java.time.LocalDateTime;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * Clase DETALLE. Se guarda en la coleccion "agentes_navegacion".
 * Referencia a su maestro con idAgenteInteligente. Segun el diagrama (0..1),
 * un agente de navegacion puede quedar sin agente inteligente asignado.
 */
@Document(collection = "agentes_navegacion")
public class AgenteNavegacion {

    @Id
    private int idNavegacion;                     // int           - llave primaria
    @Indexed(unique = true)
    private String nombre;                        // String        - obligatorio, unico
    private String origen;                        // String        - obligatorio
    @Indexed
    private String destino;                       // String        - obligatorio
    private double precisionGPS;                  // double        - obligatorio (0 - 100)
    private Double velocidadMaxima;               // double        - OPCIONAL (> 0 y <= 500 km/h)
    private LocalDateTime fechaUltimaCalibracion; // LocalDateTime - obligatorio (no futura)
    private boolean rutaOptimizada;               // boolean       - obligatorio (atributo de eleccion)
    @Indexed
    private Integer idAgenteInteligente;          // referencia al maestro - OPCIONAL

    public AgenteNavegacion() {
    }

    private AgenteNavegacion(Builder b) {
        this.idNavegacion = b.idNavegacion;
        this.nombre = b.nombre;
        this.origen = b.origen;
        this.destino = b.destino;
        this.precisionGPS = b.precisionGPS;
        this.velocidadMaxima = b.velocidadMaxima;
        this.fechaUltimaCalibracion = b.fechaUltimaCalibracion;
        this.rutaOptimizada = b.rutaOptimizada;
        this.idAgenteInteligente = b.idAgenteInteligente;
    }

    public static Builder builder() {
        return new Builder();
    }

    public int getIdNavegacion() { return idNavegacion; }
    public void setIdNavegacion(int idNavegacion) { this.idNavegacion = idNavegacion; }
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
    public String getOrigen() { return origen; }
    public void setOrigen(String origen) { this.origen = origen; }
    public String getDestino() { return destino; }
    public void setDestino(String destino) { this.destino = destino; }
    public double getPrecisionGPS() { return precisionGPS; }
    public void setPrecisionGPS(double precisionGPS) { this.precisionGPS = precisionGPS; }
    public Double getVelocidadMaxima() { return velocidadMaxima; }
    public void setVelocidadMaxima(Double velocidadMaxima) { this.velocidadMaxima = velocidadMaxima; }
    public LocalDateTime getFechaUltimaCalibracion() { return fechaUltimaCalibracion; }
    public void setFechaUltimaCalibracion(LocalDateTime f) { this.fechaUltimaCalibracion = f; }
    public boolean isRutaOptimizada() { return rutaOptimizada; }
    public void setRutaOptimizada(boolean rutaOptimizada) { this.rutaOptimizada = rutaOptimizada; }
    public Integer getIdAgenteInteligente() { return idAgenteInteligente; }
    public void setIdAgenteInteligente(Integer idAgenteInteligente) { this.idAgenteInteligente = idAgenteInteligente; }

    /** Patron Builder. */
    public static class Builder {
        private int idNavegacion;
        private String nombre;
        private String origen;
        private String destino;
        private double precisionGPS;
        private Double velocidadMaxima;
        private LocalDateTime fechaUltimaCalibracion;
        private boolean rutaOptimizada;
        private Integer idAgenteInteligente;

        public Builder idNavegacion(int v) { this.idNavegacion = v; return this; }
        public Builder nombre(String v) { this.nombre = v; return this; }
        public Builder origen(String v) { this.origen = v; return this; }
        public Builder destino(String v) { this.destino = v; return this; }
        public Builder precisionGPS(double v) { this.precisionGPS = v; return this; }
        public Builder velocidadMaxima(Double v) { this.velocidadMaxima = v; return this; }
        public Builder fechaUltimaCalibracion(LocalDateTime v) { this.fechaUltimaCalibracion = v; return this; }
        public Builder rutaOptimizada(boolean v) { this.rutaOptimizada = v; return this; }
        public Builder idAgenteInteligente(Integer v) { this.idAgenteInteligente = v; return this; }

        public AgenteNavegacion build() {
            return new AgenteNavegacion(this);
        }
    }
}
