package com.unibague.agentes.servicios;

import java.util.regex.Pattern;

import org.springframework.stereotype.Service;

import com.unibague.agentes.dto.ActualizarAgenteNavegacionInput;
import com.unibague.agentes.dto.AgenteNavegacionInput;
import com.unibague.agentes.dto.NavegacionConAgente;
import com.unibague.agentes.dto.Pagina;
import com.unibague.agentes.dto.Paginacion;
import com.unibague.agentes.excepciones.RecursoNoEncontradoException;
import com.unibague.agentes.excepciones.ReglaNegocioException;
import com.unibague.agentes.model.AgenteNavegacion;
import com.unibague.agentes.repository.AgenteInteligenteRepository;
import com.unibague.agentes.repository.AgenteNavegacionRepository;

@Service
public class ServicioAgenteNavegacion implements IServicioAgenteNavegacion {

    private final AgenteNavegacionRepository repositorio;
    private final AgenteInteligenteRepository repositorioAgentes;

    public ServicioAgenteNavegacion(AgenteNavegacionRepository repositorio,
                                    AgenteInteligenteRepository repositorioAgentes) {
        this.repositorio = repositorio;
        this.repositorioAgentes = repositorioAgentes;
    }

    @Override
    public Pagina<NavegacionConAgente> listarConAgentePorDestino(String destino, Integer pagina, Integer tamano) {
        int p = Paginacion.pagina(pagina);
        int t = Paginacion.tamano(tamano);
        // Pattern.quote evita que caracteres especiales se interpreten como regex
        String patron = Pattern.quote(destino == null ? "" : destino.trim());
        return Pagina.de(repositorio.listarConAgentePorDestino(patron, Paginacion.saltar(p, t), t),
                repositorio.contarPorDestino(patron), p, t);
    }

    @Override
    public Pagina<NavegacionConAgente> listarConAgentePorAgente(int idAgente, Integer pagina, Integer tamano) {
        if (!repositorioAgentes.existsById(idAgente)) {
            throw new RecursoNoEncontradoException("No existe un agente inteligente con ID " + idAgente);
        }
        int p = Paginacion.pagina(pagina);
        int t = Paginacion.tamano(tamano);
        return Pagina.de(repositorio.listarConAgentePorAgente(idAgente, Paginacion.saltar(p, t), t),
                repositorio.countByIdAgenteInteligente(idAgente), p, t);
    }

    @Override
    public AgenteNavegacion buscarPorId(int idNavegacion) {
        if (idNavegacion <= 0) {
            throw new ReglaNegocioException("El ID debe ser un entero positivo");
        }
        return repositorio.findById(idNavegacion)
                .orElseThrow(() -> new RecursoNoEncontradoException(
                        "No existe un agente de navegacion con ID " + idNavegacion));
    }

    @Override
    public AgenteNavegacion buscarPorNombre(String nombre) {
        if (nombre == null || nombre.isBlank()) {
            throw new ReglaNegocioException("Debe escribir el nombre del agente de navegacion a buscar");
        }
        return repositorio.findByNombreIgnoreCase(nombre.trim())
                .orElseThrow(() -> new RecursoNoEncontradoException(
                        "No existe un agente de navegacion con el nombre '" + nombre.trim() + "'"));
    }

    @Override
    public AgenteNavegacion crear(AgenteNavegacionInput in) {
        if (repositorio.existsById(in.idNavegacion())) {
            throw new ReglaNegocioException("Ya existe un agente de navegacion con ID " + in.idNavegacion());
        }
        validarNombreUnico(in.nombre(), null);
        validarAgenteInteligente(in.idAgenteInteligente());
        validarOrigenDestino(in.origen(), in.destino());

        AgenteNavegacion nav = AgenteNavegacion.builder()
                .idNavegacion(in.idNavegacion())
                .nombre(in.nombre().trim())
                .origen(in.origen().trim())
                .destino(in.destino().trim())
                .precisionGPS(in.precisionGPS())
                .velocidadMaxima(in.velocidadMaxima())
                .fechaUltimaCalibracion(in.fechaUltimaCalibracion())
                .rutaOptimizada(in.rutaOptimizada())
                .idAgenteInteligente(in.idAgenteInteligente())
                .build();
        return repositorio.insert(nav);
    }

    @Override
    public AgenteNavegacion actualizar(int idNavegacion, ActualizarAgenteNavegacionInput in) {
        AgenteNavegacion nav = buscarPorId(idNavegacion);   // busqueda previa
        validarNombreUnico(in.nombre(), idNavegacion);
        validarAgenteInteligente(in.idAgenteInteligente());
        validarOrigenDestino(in.origen(), in.destino());

        nav.setNombre(in.nombre().trim());
        nav.setOrigen(in.origen().trim());
        nav.setDestino(in.destino().trim());
        nav.setPrecisionGPS(in.precisionGPS());
        nav.setVelocidadMaxima(in.velocidadMaxima());
        nav.setFechaUltimaCalibracion(in.fechaUltimaCalibracion());
        nav.setRutaOptimizada(in.rutaOptimizada());
        nav.setIdAgenteInteligente(in.idAgenteInteligente());
        return repositorio.save(nav);
    }

    @Override
    public String eliminar(int idNavegacion) {
        AgenteNavegacion nav = buscarPorId(idNavegacion);   // busqueda previa
        repositorio.deleteById(idNavegacion);
        return "Agente de navegacion '" + nav.getNombre() + "' eliminado correctamente.";
    }

    // ----------------------------------------------------------------- utilidades

    private void validarNombreUnico(String nombre, Integer idActual) {
        repositorio.findByNombreIgnoreCase(nombre.trim()).ifPresent(existente -> {
            if (idActual == null || existente.getIdNavegacion() != idActual) {
                throw new ReglaNegocioException(
                        "Ya existe un agente de navegacion con el nombre '" + nombre.trim() + "'");
            }
        });
    }

    private void validarAgenteInteligente(Integer idAgente) {
        if (idAgente != null && !repositorioAgentes.existsById(idAgente)) {
            throw new ReglaNegocioException("No existe el agente inteligente con ID " + idAgente
                    + ". Elija uno existente o deje el campo sin asignar");
        }
    }

    private void validarOrigenDestino(String origen, String destino) {
        if (origen.trim().equalsIgnoreCase(destino.trim())) {
            throw new ReglaNegocioException("El origen y el destino deben ser diferentes");
        }
    }
}
