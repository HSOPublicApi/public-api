package com.hs1.service;

import com.hs1.model.ApiResponse;
import com.hs1.model.Operatory;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.Collections;
import java.util.List;

@Component
@Slf4j
public class OperatoryService extends TemplateMethodService<Operatory> {

    public OperatoryService(RestTemplate serviceTemplate, HttpHeaders headers, @Value("${operatories.url}") String serviceUrl) {
        this.serviceTemplate = serviceTemplate;
        this.headers = headers;
        this.serviceUrl = serviceUrl;
    }

    @SneakyThrows
    public List<Operatory> findAll() {
        // Build the HTTP entity
        HttpHeaders requestHeaders = new HttpHeaders(headers);
        requestHeaders.add("Organization-ID", "5c8958ef64c9477daadf664e");
        HttpEntity<String> requestEntity = new HttpEntity<>(requestHeaders);

        ResponseEntity<ApiResponse<Operatory>> response = serviceTemplate.exchange(
                serviceUrl,
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<ApiResponse<Operatory>>() {}
        );

        // Custom logging for operatories - simplified
        logOperatoriesResponse("getOperatories", response);

        ApiResponse<Operatory> body = response.getBody();
        List<Operatory> operatories = body != null ? body.getData() : Collections.emptyList();

        return operatories;
    }

    private void logOperatoriesResponse(String operation, ResponseEntity<ApiResponse<Operatory>> response) {
        log.info("");
        log.info(operation);
        log.info("status code: {}", response.getStatusCode().value());
        
        // For operatories, show a simplified version since it's a lot of data
        ApiResponse<Operatory> body = response.getBody();
        if (body != null && body.getData() != null) {
            log.info("{{");
            log.info("  \"statusCode\": {},", body.getStatusCode());
            log.info("  \"data\": [");
            log.info("    // {} operatories found (showing count only to avoid overwhelming output)", body.getData().size());
            log.info("  ]");
            log.info("}}");
        } else {
            log.info("No operatories found");
        }
    }

    @SneakyThrows
    public String getOperatoryId() {
        List<Operatory> operatories = findAll();
        if (!operatories.isEmpty()) {
            String operatoryId = operatories.get(0).getId().toString();
            log.info("Using Operatory ID: {}", operatoryId);
            return operatoryId;
        }
        throw new RuntimeException("No operatories found");
    }
} 