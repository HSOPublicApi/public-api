package com.hs1.service;

import com.hs1.model.ApiResponse;
import com.hs1.model.Provider;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.util.Collections;
import java.util.List;
import java.util.Map;

@Component
@Slf4j
public class ProviderService extends TemplateMethodService<Provider> {

    public ProviderService(RestTemplate serviceTemplate, HttpHeaders headers, @Value("${providers.url}") String serviceUrl) {
        this.serviceTemplate = serviceTemplate;
        this.headers = headers;
        this.serviceUrl = serviceUrl;
    }

    @Override
    protected String getEntityName() {
        return "Provider";
    }

    @Override
    protected Class<Provider> getEntityClass() {
        return Provider.class;
    }

    /**
     * Get providers - matches Python's getProviders function
     * Custom implementation to handle complex Provider response structure
     */
    public String getProviders() {
        // Build URL with pagination to limit results to 1 to avoid overwhelming output
        String url = UriComponentsBuilder.fromHttpUrl(serviceUrl)
                .queryParam("pageSize", MAX_PAGE_SIZE)
                .toUriString();

        HttpHeaders requestHeaders = createRequestHeaders();
        HttpEntity<String> requestEntity = new HttpEntity<>(requestHeaders);

        ResponseEntity<ApiResponse<Map<String, Object>>> response = serviceTemplate.exchange(
                url,
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<ApiResponse<Map<String, Object>>>() {}
        );

        // Custom logging for providers - simplified to avoid overwhelming output
        logProviderResponse("getProviders", response);

        ApiResponse<Map<String, Object>> body = response.getBody();
        List<Map<String, Object>> providerMaps = body != null ? body.getData() : Collections.emptyList();

        if (!providerMaps.isEmpty()) {
            Map<String, Object> firstProvider = providerMaps.get(0);
            String providerId = firstProvider.get("id").toString();
            log.info("Using Provider ID: {}", providerId);
            return providerId;
        }
        throw new RuntimeException("No providers found");
    }

    private void logProviderResponse(String operation, ResponseEntity<ApiResponse<Map<String, Object>>> response) {
        log.info("");
        log.info(operation);
        log.info("status code: {}", response.getStatusCode().value());
        
        // For providers, show a simplified version since they have massive insurance carrier data
        ApiResponse<Map<String, Object>> body = response.getBody();
        if (body != null && body.getData() != null && !body.getData().isEmpty()) {
            Map<String, Object> firstProvider = body.getData().get(0);
            log.info("{{");
            log.info("  \"statusCode\": {},", body.getStatusCode());
            log.info("  \"data\": [");
            log.info("    {{");
            log.info("      \"id\": \"{}\",", firstProvider.get("id"));
            log.info("      \"firstName\": \"{}\",", firstProvider.get("firstName"));
            log.info("      \"lastName\": \"{}\",", firstProvider.get("lastName"));
            log.info("      \"shortName\": \"{}\",", firstProvider.get("shortName"));
            log.info("      \"npi\": \"{}\",", firstProvider.get("npi"));
            log.info("      \"active\": {},", firstProvider.get("active"));
            log.info("      \"specialty\": \"{}\"", firstProvider.get("specialty"));
            
            // Show insurance carriers count instead of full list
            List<?> insuranceCarriers = (List<?>) firstProvider.get("insuranceCarriers");
            if (insuranceCarriers != null) {
                log.info("      // {} insurance carriers (details omitted for brevity)", insuranceCarriers.size());
            }
            
            log.info("    }}");
            log.info("  ]");
            log.info("}}");
        } else {
            log.info("No providers found");
        }
    }

    /**
     * Legacy method for backward compatibility
     */
    public String getProviderId() {
        return getProviders();
    }
} 