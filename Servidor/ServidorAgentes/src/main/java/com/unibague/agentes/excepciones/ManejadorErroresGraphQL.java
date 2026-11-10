package com.unibague.agentes.excepciones;

import java.util.stream.Collectors;

import org.springframework.dao.DataAccessResourceFailureException;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.graphql.execution.DataFetcherExceptionResolverAdapter;
import org.springframework.graphql.execution.ErrorType;
import org.springframework.stereotype.Component;

import graphql.GraphQLError;
import graphql.GraphqlErrorBuilder;
import graphql.schema.DataFetchingEnvironment;
import jakarta.validation.ConstraintViolation;
import jakarta.validation.ConstraintViolationException;

/**
 * Convierte las excepciones del servidor en errores GraphQL con mensajes claros
 * que los clientes muestran directamente al usuario.
 */
@Component
public class ManejadorErroresGraphQL extends DataFetcherExceptionResolverAdapter {

    @Override
    protected GraphQLError resolveToSingleError(Throwable ex, DataFetchingEnvironment env) {
        ErrorType tipo;
        String mensaje;

        if (ex instanceof RecursoNoEncontradoException) {
            tipo = ErrorType.NOT_FOUND;
            mensaje = ex.getMessage();
        } else if (ex instanceof ReglaNegocioException) {
            tipo = ErrorType.BAD_REQUEST;
            mensaje = ex.getMessage();
        } else if (ex instanceof ConstraintViolationException cve) {
            tipo = ErrorType.BAD_REQUEST;
            mensaje = cve.getConstraintViolations().stream()
                    .map(ConstraintViolation::getMessage)
                    .sorted()
                    .collect(Collectors.joining("; "));
        } else if (ex instanceof DuplicateKeyException) {
            tipo = ErrorType.BAD_REQUEST;
            mensaje = "Ya existe un registro con ese ID o con ese nombre";
        } else if (ex instanceof DataAccessResourceFailureException) {
            tipo = ErrorType.INTERNAL_ERROR;
            mensaje = "No se pudo conectar con la base de datos MongoDB. Verifique que este en ejecucion";
        } else {
            tipo = ErrorType.INTERNAL_ERROR;
            mensaje = "Error interno del servidor: " + ex.getMessage();
        }

        return GraphqlErrorBuilder.newError(env)
                .errorType(tipo)
                .message(mensaje)
                .build();
    }
}
