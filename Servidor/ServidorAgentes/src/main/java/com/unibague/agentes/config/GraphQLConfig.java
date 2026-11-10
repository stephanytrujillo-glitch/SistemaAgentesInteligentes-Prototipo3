package com.unibague.agentes.config;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.Locale;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.graphql.execution.RuntimeWiringConfigurer;

import graphql.GraphQLContext;
import graphql.execution.CoercedVariables;
import graphql.language.StringValue;
import graphql.language.Value;
import graphql.schema.Coercing;
import graphql.schema.CoercingParseLiteralException;
import graphql.schema.CoercingParseValueException;
import graphql.schema.CoercingSerializeException;
import graphql.schema.GraphQLScalarType;

/** Registra el escalar DateTime para manejar LocalDateTime en GraphQL. */
@Configuration
public class GraphQLConfig {

    public static final DateTimeFormatter FORMATO = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss");

    private static final String MENSAJE_FORMATO =
            "Fecha invalida. Use el formato AAAA-MM-DDTHH:MM (ejemplo 2026-11-09T14:30)";

    @Bean
    public RuntimeWiringConfigurer runtimeWiringConfigurer() {
        GraphQLScalarType dateTime = GraphQLScalarType.newScalar()
                .name("DateTime")
                .description("Fecha y hora local, formato yyyy-MM-ddTHH:mm:ss")
                .coercing(new Coercing<LocalDateTime, String>() {

                    @Override
                    public String serialize(Object valor, GraphQLContext ctx, Locale locale) {
                        if (valor instanceof LocalDateTime fecha) {
                            return fecha.format(FORMATO);
                        }
                        if (valor instanceof String texto) {
                            return texto;
                        }
                        throw new CoercingSerializeException("No se puede convertir a DateTime: " + valor);
                    }

                    @Override
                    public LocalDateTime parseValue(Object entrada, GraphQLContext ctx, Locale locale) {
                        try {
                            return convertir(String.valueOf(entrada));
                        } catch (DateTimeParseException e) {
                            throw new CoercingParseValueException(MENSAJE_FORMATO);
                        }
                    }

                    @Override
                    public LocalDateTime parseLiteral(Value<?> entrada, CoercedVariables variables,
                                                      GraphQLContext ctx, Locale locale) {
                        if (entrada instanceof StringValue texto) {
                            try {
                                return convertir(texto.getValue());
                            } catch (DateTimeParseException e) {
                                throw new CoercingParseLiteralException(MENSAJE_FORMATO);
                            }
                        }
                        throw new CoercingParseLiteralException(MENSAJE_FORMATO);
                    }
                })
                .build();

        return wiring -> wiring.scalar(dateTime);
    }

    private static LocalDateTime convertir(String texto) {
        return LocalDateTime.parse(texto.trim().replace(' ', 'T'));
    }
}
