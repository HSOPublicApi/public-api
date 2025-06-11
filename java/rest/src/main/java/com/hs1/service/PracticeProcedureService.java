package com.hs1.service;

import com.hs1.model.ApiResponse;
import com.hs1.model.PracticeProcedure;
import lombok.SneakyThrows;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import lombok.extern.slf4j.Slf4j;
import java.util.List;
import java.util.Collections;

@Component
@Slf4j
public class PracticeProcedureService extends TemplateMethodService<PracticeProcedure> {

    public PracticeProcedureService(RestTemplate serviceTemplate, HttpHeaders headers, @Value("${practiceprocedures.url}") String serviceUrl) {
        this.serviceTemplate = serviceTemplate;
        this.headers = headers;
        this.serviceUrl = serviceUrl;
    }

    @SneakyThrows
    public List<PracticeProcedure> findAll() {
        // Build the HTTP entity
        HttpEntity<String> requestEntity = new HttpEntity<>(headers);
        headers.add("Organization-ID", "5c8958ef64c9477daadf664e");

        ResponseEntity<ApiResponse<PracticeProcedure>> response = serviceTemplate.exchange(
                serviceUrl,
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<ApiResponse<PracticeProcedure>>() {}
        );

        ApiResponse<PracticeProcedure> body = response.getBody();
        List<PracticeProcedure> practiceProcedures = body != null ? body.getData() : Collections.emptyList();

        return practiceProcedures;
    }
} 