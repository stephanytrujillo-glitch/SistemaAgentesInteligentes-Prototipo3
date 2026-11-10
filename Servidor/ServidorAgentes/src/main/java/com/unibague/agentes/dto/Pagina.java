package com.unibague.agentes.dto;

import java.util.List;

/**
 * Una pagina de resultados. El servidor solo envia "tamano" registros por consulta,
 * asi el listado responde igual de rapido con 10 o con 100.000 registros.
 */
public record Pagina<T>(List<T> elementos, int total, int pagina, int tamano, int totalPaginas) {

    public static <T> Pagina<T> de(List<T> elementos, long total, int pagina, int tamano) {
        int totalPaginas = (int) Math.max(1, (total + tamano - 1) / tamano);
        return new Pagina<>(elementos, Math.toIntExact(total), pagina, tamano, totalPaginas);
    }
}
