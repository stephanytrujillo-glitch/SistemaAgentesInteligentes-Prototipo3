package com.unibague.agentes.dto;

import com.unibague.agentes.excepciones.ReglaNegocioException;

/** Valida y normaliza los parametros de paginacion que llegan del cliente. */
public final class Paginacion {

    public static final int TAMANO_POR_DEFECTO = 25;
    public static final int TAMANO_MAXIMO = 100;

    private Paginacion() {
    }

    public static int pagina(Integer pagina) {
        int p = pagina == null ? 0 : pagina;
        if (p < 0) {
            throw new ReglaNegocioException("La pagina debe ser 0 o mayor");
        }
        return p;
    }

    public static int tamano(Integer tamano) {
        int t = tamano == null ? TAMANO_POR_DEFECTO : tamano;
        if (t < 1 || t > TAMANO_MAXIMO) {
            throw new ReglaNegocioException("El tamano de pagina debe estar entre 1 y " + TAMANO_MAXIMO);
        }
        return t;
    }

    public static long saltar(int pagina, int tamano) {
        return (long) pagina * tamano;
    }
}
