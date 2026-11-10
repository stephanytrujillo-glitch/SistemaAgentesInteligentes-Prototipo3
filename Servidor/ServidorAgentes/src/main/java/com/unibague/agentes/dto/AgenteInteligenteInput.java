package com.unibague.agentes.dto;

import java.time.LocalDateTime;

import com.unibague.agentes.model.EstadoOperativo;

import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PastOrPresent;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;

/** Datos para CREAR un agente inteligente (incluye la llave primaria). */
public record AgenteInteligenteInput(

        @NotNull(message = "El ID del agente es obligatorio")
        @Positive(message = "El ID del agente debe ser un entero positivo")
        Integer idAgente,

        @NotBlank(message = "El nombre es obligatorio")
        @Size(min = 3, max = 50, message = "El nombre debe tener entre 3 y 50 caracteres")
        @Pattern(regexp = Validaciones.PATRON_NOMBRE, message = Validaciones.MENSAJE_NOMBRE)
        String nombre,

        @NotNull(message = "El nivel de autonomia es obligatorio")
        @DecimalMin(value = "0.0", message = "El nivel de autonomia debe estar entre 0 y 100")
        @DecimalMax(value = "100.0", message = "El nivel de autonomia debe estar entre 0 y 100")
        Double nivelAutonomia,

        @NotNull(message = "El estado operativo es obligatorio")
        EstadoOperativo estadoOperativo,

        @DecimalMin(value = "0.0", message = "El nivel de confianza debe estar entre 0 y 100")
        @DecimalMax(value = "100.0", message = "El nivel de confianza debe estar entre 0 y 100")
        Double nivelConfianza,

        @NotNull(message = "La fecha de registro es obligatoria")
        @PastOrPresent(message = "La fecha de registro no puede ser futura")
        LocalDateTime fechaRegistro,

        @NotNull(message = "Debe indicar si el agente tiene aprendizaje continuo")
        Boolean aprendizajeContinuo,

        @Size(max = 200, message = "La descripcion admite maximo 200 caracteres")
        String descripcion
) {
}
