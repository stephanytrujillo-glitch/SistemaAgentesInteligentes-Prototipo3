package com.unibague.agentes.dto;

/** Constantes de validacion compartidas por los inputs. */
public final class Validaciones {

    public static final String PATRON_NOMBRE = "^[A-Za-z0-9ÁÉÍÓÚáéíóúÑñÜü _.-]+$";
    public static final String MENSAJE_NOMBRE =
            "El nombre solo admite letras, numeros, espacios, punto, guion y guion bajo";

    private Validaciones() {
    }
}
