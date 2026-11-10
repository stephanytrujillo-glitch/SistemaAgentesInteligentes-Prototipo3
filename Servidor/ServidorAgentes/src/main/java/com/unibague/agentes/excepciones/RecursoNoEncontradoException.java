package com.unibague.agentes.excepciones;

/** Se lanza cuando el objeto buscado no existe en la base de datos. */
public class RecursoNoEncontradoException extends RuntimeException {
    public RecursoNoEncontradoException(String mensaje) {
        super(mensaje);
    }
}
