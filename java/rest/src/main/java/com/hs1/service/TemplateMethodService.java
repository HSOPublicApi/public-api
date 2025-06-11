package com.hs1.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.hs1.model.ApiResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Slf4j
public class TemplateMethodService<O> {

    protected RestTemplate serviceTemplate;
    protected HttpHeaders headers;
    protected String serviceUrl;
    
    @Autowired
    protected ObjectMapper objectMapper;
    
    @Value("${organization.id:5c8958ef64c9477daadf664e}")
    protected String organizationId;

    /**
     * Creates headers with Organization-ID for API requests
     */
    protected HttpHeaders createRequestHeaders() {
        HttpHeaders requestHeaders = new HttpHeaders(headers);
        requestHeaders.add("Organization-ID", organizationId);
        return requestHeaders;
    }

    protected <T>T getByHeaderId (String headerId, String id) {
        headers.add(headerId, id);

        // Build the HTTP entity
        HttpEntity<String> requestEntity = new HttpEntity<>(headers);

        ResponseEntity<ApiResponse<T>> response = serviceTemplate.exchange(
                serviceUrl,
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<ApiResponse<T>>() {}
        );

        ApiResponse<T> body = response.getBody();
        return body != null && !body.getData().isEmpty() ? body.getData().getFirst() : null;
    }

    /**
     * Generic findById method that can be used by all services
     * @param id The ID of the entity to find
     * @param entityClass The class type to convert the response to
     * @param entityName The name of the entity for logging purposes (e.g., "Appointment", "Patient")
     * @return The found entity or null if not found
     */
    public <T> T findById(String id, Class<T> entityClass, String entityName) {
        String url = serviceUrl + "/" + id;
        
        HttpHeaders requestHeaders = new HttpHeaders(headers);
        requestHeaders.add("Organization-ID", "5c8958ef64c9477daadf664e");
        HttpEntity<String> requestEntity = new HttpEntity<>(requestHeaders);

        ResponseEntity<Map<String, Object>> response = serviceTemplate.exchange(
                url,
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<Map<String, Object>>() {}
        );

        logResponse("findById " + entityName, response);

        if (response.getBody() != null && response.getBody().containsKey("data")) {
            Object data = response.getBody().get("data");
            return objectMapper.convertValue(data, entityClass);
        }
        return null;
    }

    /**
     * Generic response logging method - matches Python version format
     */
    protected void logResponse(String operation, ResponseEntity<?> response) {
        log.info("");
        log.info(operation);
        log.info("status code: {}", response.getStatusCode().value());
        
        try {
            String responseBody = objectMapper.writerWithDefaultPrettyPrinter()
                    .writeValueAsString(response.getBody());
            log.info("{}", responseBody);
        } catch (Exception e) {
            log.info("Response: {}", response.getBody());
        }
    }
}
