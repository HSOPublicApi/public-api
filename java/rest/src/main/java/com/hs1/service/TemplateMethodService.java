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
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.util.List;
import java.util.Map;
import java.util.Collections;

@Slf4j
public abstract class TemplateMethodService<T> {

    // Constant to limit all API responses to maximum 1 item to avoid timeouts
    protected static final int MAX_PAGE_SIZE = 1;

    protected RestTemplate serviceTemplate;
    protected HttpHeaders headers;
    protected String serviceUrl;
    
    @Autowired
    protected ObjectMapper objectMapper;
    
    @Value("${organization.id:5c8958ef64c9477daadf664e}")
    protected String organizationId;

    /**
     * Creates headers with Organization-ID for API requests - matches Python version
     */
    protected HttpHeaders createRequestHeaders() {
        HttpHeaders requestHeaders = new HttpHeaders(headers);
        requestHeaders.add("Organization-ID", organizationId);
        return requestHeaders;
    }

    /**
     * Generic findAll method - matches Python's get operations
     * Limited to maximum 5 results per endpoint
     */
    public List<T> findAll() {
        // Build URL with pagination to limit results to 5
        String url = UriComponentsBuilder.fromHttpUrl(serviceUrl)
                .queryParam("pageSize", MAX_PAGE_SIZE)
                .toUriString();
        
        HttpHeaders requestHeaders = createRequestHeaders();
        HttpEntity<String> requestEntity = new HttpEntity<>(requestHeaders);

        ResponseEntity<ApiResponse<T>> response = serviceTemplate.exchange(
                url,
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<ApiResponse<T>>() {}
        );

        logResponse("findAll " + getEntityName(), response);

        ApiResponse<T> body = response.getBody();
        return body != null ? body.getData() : Collections.emptyList();
    }

    /**
     * Generic findById method - matches Python's getById operations
     */
    public T findById(String id) {
        String url = serviceUrl + "/" + id;
        
        HttpHeaders requestHeaders = createRequestHeaders();
        HttpEntity<String> requestEntity = new HttpEntity<>(requestHeaders);

        ResponseEntity<Map<String, Object>> response = serviceTemplate.exchange(
                url,
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<Map<String, Object>>() {}
        );

        logResponse("findById " + getEntityName(), response);

        if (response.getBody() != null && response.getBody().containsKey("data")) {
            Object data = response.getBody().get("data");
            return objectMapper.convertValue(data, getEntityClass());
        }
        return null;
    }

    /**
     * Generic create method - matches Python's create operations
     */
    public String create(Map<String, Object> entityData) {
        HttpHeaders requestHeaders = createRequestHeaders();
        requestHeaders.setContentType(MediaType.APPLICATION_JSON);
        
        HttpEntity<Map<String, Object>> requestEntity = new HttpEntity<>(entityData, requestHeaders);

        ResponseEntity<Map<String, Object>> response = serviceTemplate.exchange(
                serviceUrl,
                HttpMethod.POST,
                requestEntity,
                new ParameterizedTypeReference<Map<String, Object>>() {}
        );

        logResponse("create" + getEntityName(), response);

        if (response.getBody() != null && response.getBody().containsKey("data")) {
            Map<String, Object> data = (Map<String, Object>) response.getBody().get("data");
            return data.get("id").toString();
        }
        throw new RuntimeException("Failed to create " + getEntityName());
    }

    /**
     * Generic update method - matches Python's update operations
     */
    public void update(String id, Map<String, Object> entityData) {
        String url = serviceUrl + "/" + id;
        
        HttpHeaders requestHeaders = createRequestHeaders();
        requestHeaders.setContentType(MediaType.APPLICATION_JSON);
        
        HttpEntity<Map<String, Object>> requestEntity = new HttpEntity<>(entityData, requestHeaders);

        ResponseEntity<Map<String, Object>> response = serviceTemplate.exchange(
                url,
                HttpMethod.PUT,
                requestEntity,
                new ParameterizedTypeReference<Map<String, Object>>() {}
        );

        logResponse("update" + getEntityName(), response);
    }

    /**
     * Generic delete method - matches Python's delete operations
     */
    public void delete(String id) {
        String url = serviceUrl + "/" + id;
        
        HttpHeaders requestHeaders = createRequestHeaders();
        HttpEntity<String> requestEntity = new HttpEntity<>(requestHeaders);

        ResponseEntity<String> response = serviceTemplate.exchange(
                url,
                HttpMethod.DELETE,
                requestEntity,
                String.class
        );

        logResponse("delete" + getEntityName(), response);
    }

    /**
     * Response logging method - matches Python version format exactly
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

    // Abstract methods that subclasses must implement
    protected abstract String getEntityName();
    protected abstract Class<T> getEntityClass();

    // Deprecated method - keeping for backward compatibility but redirecting to new method
    @Deprecated
    public <U> U findById(String id, Class<U> entityClass, String entityName) {
        log.warn("Using deprecated findById method. Use findById(String id) instead.");
        return (U) findById(id);
    }

    // Legacy method for backward compatibility
    protected <U>U getByHeaderId (String headerId, String id) {
        headers.add(headerId, id);

        HttpEntity<String> requestEntity = new HttpEntity<>(headers);

        ResponseEntity<ApiResponse<U>> response = serviceTemplate.exchange(
                serviceUrl,
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<ApiResponse<U>>() {}
        );

        ApiResponse<U> body = response.getBody();
        return body != null && !body.getData().isEmpty() ? body.getData().get(0) : null;
    }
}
