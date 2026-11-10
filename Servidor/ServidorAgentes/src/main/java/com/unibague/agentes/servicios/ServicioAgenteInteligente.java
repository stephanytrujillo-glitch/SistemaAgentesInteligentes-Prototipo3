package com.unibague.agentes.servicios;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import com.unibague.agentes.dto.ActualizarAgenteInteligenteInput;
import com.unibague.agentes.dto.AgenteInteligenteInput;
import com.unibague.agentes.dto.AgenteResumen;
import com.unibague.agentes.dto.Pagina;
import com.unibague.agentes.dto.Paginacion;
import com.unibague.agentes.excepciones.RecursoNoEncontradoException;
import com.unibague.agentes.excepciones.ReglaNegocioException;
import com.unibague.agentes.model.AgenteInteligente;
import com.unibague.agentes.model.AgenteNavegacion;
import com.unibague.agentes.model.EstadoOperativo;
import com.unibague.agentes.repository.AgenteInteligenteRepository;
import com.unibague.agentes.repository.AgenteNavegacionRepository;

@Service
public class ServicioAgenteInteligente implements IServicioAgenteInteligente {

    private final AgenteInteligenteRepository repositorio;
    private final AgenteNavegacionRepository repositorioNavegacion;

    public ServicioAgenteInteligente(AgenteInteligenteRepository repositorio,
                                     AgenteNavegacionRepository repositorioNavegacion) {
        this.repositorio = repositorio;
        this.repositorioNavegacion = repositorioNavegacion;
    }

    @Override
    public Pagina<AgenteResumen> listarResumen(EstadoOperativo estado, Integer pagina, Integer tamano) {
        int p = Paginacion.pagina(pagina);
        int t = Paginacion.tamano(tamano);
        long saltar = Paginacion.saltar(p, t);
        if (estado == null) {
            return Pagina.de(repositorio.listarResumen(saltar, t), repositorio.count(), p, t);
        }
        return Pagina.de(repositorio.listarResumenPorEstado(estado.name(), saltar, t),
                repositorio.countByEstadoOperativo(estado), p, t);
    }

    @Override
    public Pagina<AgenteInteligente> listarPorEstadoYAutonomia(EstadoOperativo estado, double autonomiaMinima,
                                                              Integer pagina, Integer tamano) {
        if (autonomiaMinima < 0 || autonomiaMinima > 100) {
            throw new ReglaNegocioException("La autonomia minima debe estar entre 0 y 100");
        }
        int p = Paginacion.pagina(pagina);
        int t = Paginacion.tamano(tamano);
        return Pagina.de(
                repositorio.buscarPorEstadoYAutonomiaMinima(estado.name(), autonomiaMinima, PageRequest.of(p, t)),
                repositorio.contarPorEstadoYAutonomiaMinima(estado.name(), autonomiaMinima), p, t);
    }

    /**
     * Opciones para escoger un agente en los formularios del detalle: en vez de traer TODOS
     * los agentes, busca por nombre (o por ID si el texto es un numero) y devuelve pocos.
     */
    @Override
    public List<AgenteInteligente> buscarOpciones(String texto, Integer limite) {
        int l = limite == null ? 20 : Math.max(1, Math.min(limite, 50));
        String t = texto == null ? "" : texto.trim();
        List<AgenteInteligente> resultado = new ArrayList<>();
        if (t.matches("\\d{1,9}")) {
            repositorio.findById(Integer.parseInt(t)).ifPresent(resultado::add);
        }
        for (AgenteInteligente a : repositorio.buscarOpciones(Pattern.quote(t),
                PageRequest.of(0, l, Sort.by("idAgente")))) {
            if (resultado.size() >= l) {
                break;
            }
            if (resultado.stream().noneMatch(r -> r.getIdAgente() == a.getIdAgente())) {
                resultado.add(a);
            }
        }
        return resultado;
    }

    @Override
    public AgenteInteligente buscarPorId(int idAgente) {
        validarId(idAgente);
        return repositorio.findById(idAgente)
                .orElseThrow(() -> new RecursoNoEncontradoException(
                        "No existe un agente inteligente con ID " + idAgente));
    }

    @Override
    public AgenteInteligente buscarPorNombre(String nombre) {
        if (nombre == null || nombre.isBlank()) {
            throw new ReglaNegocioException("Debe escribir el nombre del agente a buscar");
        }
        return repositorio.findByNombreIgnoreCase(nombre.trim())
                .orElseThrow(() -> new RecursoNoEncontradoException(
                        "No existe un agente inteligente con el nombre '" + nombre.trim() + "'"));
    }

    @Override
    public AgenteInteligente crear(AgenteInteligenteInput in) {
        if (repositorio.existsById(in.idAgente())) {
            throw new ReglaNegocioException("Ya existe un agente inteligente con ID " + in.idAgente());
        }
        validarNombreUnico(in.nombre(), null);

        AgenteInteligente agente = AgenteInteligente.builder()
                .idAgente(in.idAgente())
                .nombre(in.nombre().trim())
                .nivelAutonomia(in.nivelAutonomia())
                .estadoOperativo(in.estadoOperativo())
                .nivelConfianza(in.nivelConfianza())
                .fechaRegistro(in.fechaRegistro())
                .aprendizajeContinuo(in.aprendizajeContinuo())
                .descripcion(textoOpcional(in.descripcion()))
                .build();
        return repositorio.insert(agente);
    }

    @Override
    public AgenteInteligente actualizar(int idAgente, ActualizarAgenteInteligenteInput in) {
        AgenteInteligente agente = buscarPorId(idAgente);   // busqueda previa
        validarNombreUnico(in.nombre(), idAgente);

        agente.setNombre(in.nombre().trim());
        agente.setNivelAutonomia(in.nivelAutonomia());
        agente.setEstadoOperativo(in.estadoOperativo());
        agente.setNivelConfianza(in.nivelConfianza());
        agente.setFechaRegistro(in.fechaRegistro());
        agente.setAprendizajeContinuo(in.aprendizajeContinuo());
        agente.setDescripcion(textoOpcional(in.descripcion()));
        return repositorio.save(agente);
    }

    @Override
    public String eliminar(int idAgente) {
        AgenteInteligente agente = buscarPorId(idAgente);   // busqueda previa

        // Relacion 0..1: los agentes de navegacion NO se borran, quedan sin agente asignado.
        List<AgenteNavegacion> asociados = repositorioNavegacion.buscarPorAgenteInteligente(idAgente);
        asociados.forEach(n -> n.setIdAgenteInteligente(null));
        repositorioNavegacion.saveAll(asociados);

        repositorio.deleteById(idAgente);
        return "Agente inteligente '" + agente.getNombre() + "' eliminado. "
                + asociados.size() + " agente(s) de navegacion quedaron sin agente asignado.";
    }

    // ----------------------------------------------------------------- utilidades

    private void validarId(int id) {
        if (id <= 0) {
            throw new ReglaNegocioException("El ID debe ser un entero positivo");
        }
    }

    private void validarNombreUnico(String nombre, Integer idActual) {
        repositorio.findByNombreIgnoreCase(nombre.trim()).ifPresent(existente -> {
            if (idActual == null || existente.getIdAgente() != idActual) {
                throw new ReglaNegocioException(
                        "Ya existe un agente inteligente con el nombre '" + nombre.trim() + "'");
            }
        });
    }

    private String textoOpcional(String texto) {
        return (texto == null || texto.isBlank()) ? null : texto.trim();
    }
}
