package com.unibague.agentes.dto;

import java.time.LocalDateTime;

import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PastOrPresent;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;

/** Datos para CREAR un agente de navegacion (incluye la llave primaria). */
public record AgenteNavegacionInput(

        @NotNull(message = "El ID de navegacion es obligatorio")
        @Positive(message = "El ID de navegacion debe ser un entero positivo")
        Integer idNavegacion,

        @NotBlank(message = "El nombre es obligatorio")
        @Size(min = 3, max = 50, message = "El nombre debe tener entre 3 y 50 caracteres")
        @Pattern(regexp = Validaciones.PATRON_NOMBRE, message = Validaciones.MENSAJE_NOMBRE)
        String nombre,

        @NotBlank(message = "El origen es obligatorio")
        @Size(min = 2, max = 60, message = "El origen debe tener entre 2 y 60 caracteres")
        String origen,

        @NotBlank(message = "El destino es obligatorio")
        @Size(min = 2, max = 60, message = "El destino debe tener entre 2 y 60 caracteres")
        String destino,

        @NotNull(message = "La precision GPS es obligatoria")
        @DecimalMin(value = "0.0", message = "La precision GPS debe estar entre 0 y 100")
        @DecimalMax(value = "100.0", message = "La precision GPS debe estar entre 0 y 100")
        Double precisionGPS,

        @DecimalMin(value = "0.0", inclusive = false, message = "La velocidad maxima debe ser mayor que 0")
        @DecimalMax(value = "500.0", message = "La velocidad maxima no puede superar 500 km/h")
        Double velocidadMaxima,

        @NotNull(message = "La fecha de ultima calibracion es obligatoria")
        @PastOrPresent(message = "La fecha de ultima calibracion no puede ser futura")
        LocalDateTime fechaUltimaCalibracion,

        @NotNull(message = "Debe indicar si la ruta esta optimizada")
        Boolean rutaOptimizada,

        @Positive(message = "El ID del agente inteligente debe ser un entero positivo")
        Integer idAgenteInteligente
) {
}
