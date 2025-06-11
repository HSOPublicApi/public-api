package com.hs1.service;

import com.hs1.model.ApiResponse;
import com.hs1.model.Provider;
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
public class ProviderService extends TemplateMethodService<Provider> {

    public ProviderService(RestTemplate serviceTemplate, HttpHeaders headers, @Value("${providers.url}") String serviceUrl) {
        this.serviceTemplate = serviceTemplate;
        this.headers = headers;
        this.serviceUrl = serviceUrl;
    }

    @SneakyThrows
    public List<Provider> findAll() {
        // Build the HTTP entity
        HttpHeaders requestHeaders = new HttpHeaders(headers);
        requestHeaders.add("Organization-ID", "5c8958ef64c9477daadf664e");
        HttpEntity<String> requestEntity = new HttpEntity<>(requestHeaders);

        ResponseEntity<ApiResponse<Provider>> response = serviceTemplate.exchange(
                serviceUrl,
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<ApiResponse<Provider>>() {}
        );

        logResponse("getProviders", response);

        ApiResponse<Provider> body = response.getBody();
        List<Provider> providers = body != null ? body.getData() : Collections.emptyList();

        return providers;
    }

    @SneakyThrows
    public String getProviderId() {
        List<Provider> providers = findAll();
        if (!providers.isEmpty()) {
            String providerId = providers.get(0).getId().toString();
            log.info("Using Provider ID: {}", providerId);
            return providerId;
        }
        throw new RuntimeException("No providers found");
    }
} 