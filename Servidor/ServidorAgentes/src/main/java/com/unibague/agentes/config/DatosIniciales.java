package com.unibague.agentes.config;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import com.unibague.agentes.model.AgenteInteligente;
import com.unibague.agentes.model.AgenteNavegacion;
import com.unibague.agentes.model.EstadoOperativo;
import com.unibague.agentes.repository.AgenteInteligenteRepository;
import com.unibague.agentes.repository.AgenteNavegacionRepository;

/** Carga datos de prueba en MongoDB solo si las colecciones estan vacias. */
@Component
public class DatosIniciales implements CommandLineRunner {

    private final AgenteInteligenteRepository agentes;
    private final AgenteNavegacionRepository navegaciones;
    private final int masivos;

    public DatosIniciales(AgenteInteligenteRepository agentes, AgenteNavegacionRepository navegaciones,
                          @Value("${datos.prueba.masivos:0}") int masivos) {
        this.agentes = agentes;
        this.navegaciones = navegaciones;
        this.masivos = masivos;
    }

    @Override
    public void run(String... args) {
        if (agentes.count() == 0) {
            agentes.saveAll(List.of(
                    AgenteInteligente.builder().idAgente(1).nombre("Atlas").nivelAutonomia(85.5)
                            .estadoOperativo(EstadoOperativo.ACTIVO).nivelConfianza(92.0)
                            .fechaRegistro(LocalDateTime.of(2026, 2, 10, 9, 0))
                            .aprendizajeContinuo(true).descripcion("Coordinador de rutas urbanas").build(),
                    AgenteInteligente.builder().idAgente(2).nombre("Boreas").nivelAutonomia(60.0)
                            .estadoOperativo(EstadoOperativo.MANTENIMIENTO).nivelConfianza(75.3)
                            .fechaRegistro(LocalDateTime.of(2026, 4, 3, 14, 30))
                            .aprendizajeContinuo(false).build(),
                    AgenteInteligente.builder().idAgente(3).nombre("Cronos").nivelAutonomia(40.2)
                            .estadoOperativo(EstadoOperativo.INACTIVO)
                            .fechaRegistro(LocalDateTime.of(2026, 7, 21, 8, 15))
                            .aprendizajeContinuo(true).descripcion("Agente en pruebas de laboratorio").build()
            ));
        }
        if (navegaciones.count() == 0) {
            navegaciones.saveAll(List.of(
                    AgenteNavegacion.builder().idNavegacion(101).nombre("Nav Centro").origen("Ibague")
                            .destino("Bogota").precisionGPS(97.5).velocidadMaxima(80.0)
                            .fechaUltimaCalibracion(LocalDateTime.of(2026, 10, 1, 10, 0))
                            .rutaOptimizada(true).idAgenteInteligente(1).build(),
                    AgenteNavegacion.builder().idNavegacion(102).nombre("Nav Norte").origen("Ibague")
                            .destino("Medellin").precisionGPS(88.0)
                            .fechaUltimaCalibracion(LocalDateTime.of(2026, 9, 15, 16, 45))
                            .rutaOptimizada(false).idAgenteInteligente(1).build(),
                    AgenteNavegacion.builder().idNavegacion(103).nombre("Nav Sur").origen("Neiva")
                            .destino("Cali").precisionGPS(91.2).velocidadMaxima(65.5)
                            .fechaUltimaCalibracion(LocalDateTime.of(2026, 8, 20, 7, 30))
                            .rutaOptimizada(true).idAgenteInteligente(2).build(),
                    AgenteNavegacion.builder().idNavegacion(104).nombre("Nav Libre").origen("Espinal")
                            .destino("Bogota").precisionGPS(70.0)
                            .fechaUltimaCalibracion(LocalDateTime.of(2026, 6, 5, 12, 0))
                            .rutaOptimizada(false).build()
            ));
        }
        if (masivos > 0 && !agentes.existsById(ID_INICIAL_MASIVO)) {
            generarMasivos();
        }
    }

    private static final int ID_INICIAL_MASIVO = 1001;
    private static final String[] CIUDADES = {"Ibague", "Bogota", "Medellin", "Cali", "Neiva", "Pereira",
            "Manizales", "Armenia", "Espinal", "Honda", "Melgar", "Girardot"};

    /**
     * Genera "masivos" agentes inteligentes y 2 agentes de navegacion por cada uno, para
     * demostrar que el listado paginado responde igual de rapido con miles de registros.
     * Se activa con datos.prueba.masivos en application.properties. Inserta por lotes de 1000.
     */
    private void generarMasivos() {
        Random azar = new Random(2026);
        EstadoOperativo[] estados = EstadoOperativo.values();
        List<AgenteInteligente> loteAgentes = new ArrayList<>();
        List<AgenteNavegacion> loteNavs = new ArrayList<>();
        LocalDateTime base = LocalDateTime.of(2025, 1, 1, 8, 0);

        for (int i = 0; i < masivos; i++) {
            int id = ID_INICIAL_MASIVO + i;
            loteAgentes.add(AgenteInteligente.builder().idAgente(id).nombre("Agente " + id)
                    .nivelAutonomia(Math.round(azar.nextDouble() * 1000) / 10.0)
                    .estadoOperativo(estados[azar.nextInt(estados.length)])
                    .nivelConfianza(azar.nextBoolean() ? Math.round(azar.nextDouble() * 1000) / 10.0 : null)
                    .fechaRegistro(base.plusHours(i))
                    .aprendizajeContinuo(azar.nextBoolean()).build());
            for (int j = 0; j < 2; j++) {
                int origen = azar.nextInt(CIUDADES.length);
                int destino = (origen + 1 + azar.nextInt(CIUDADES.length - 1)) % CIUDADES.length;
                int idNav = 100000 + i * 2 + j;
                loteNavs.add(AgenteNavegacion.builder().idNavegacion(idNav).nombre("Navegacion " + idNav)
                        .origen(CIUDADES[origen]).destino(CIUDADES[destino])
                        .precisionGPS(Math.round(500 + azar.nextDouble() * 500) / 10.0)
                        .velocidadMaxima(azar.nextBoolean() ? Math.round(20 + azar.nextDouble() * 1000) / 10.0 : null)
                        .fechaUltimaCalibracion(base.plusHours(i).plusMinutes(30))
                        .rutaOptimizada(azar.nextBoolean()).idAgenteInteligente(id).build());
            }
            if (loteAgentes.size() == 1000) {
                agentes.insert(loteAgentes);
                navegaciones.insert(loteNavs);
                loteAgentes.clear();
                loteNavs.clear();
            }
        }
        if (!loteAgentes.isEmpty()) {
            agentes.insert(loteAgentes);
            navegaciones.insert(loteNavs);
        }
    }
}
