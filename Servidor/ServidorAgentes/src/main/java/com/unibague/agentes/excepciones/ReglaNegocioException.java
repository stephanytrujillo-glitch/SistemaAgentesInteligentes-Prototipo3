package com.unibague.agentes.excepciones;

/** Se lanza cuando los datos son validos en formato pero violan una regla del negocio. */
public class ReglaNegocioException extends RuntimeException {
    public ReglaNegocioException(String mensaje) {
        super(mensaje);
    }
}
