package com.hs1.service;

import com.hs1.model.ApiResponse;
import com.hs1.model.Location;
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

@Component
@Slf4j
public class LocationService extends TemplateMethodService<Location> {

    public LocationService(RestTemplate serviceTemplate, HttpHeaders headers, @Value("${locations.url}") String serviceUrl) {
        this.serviceTemplate = serviceTemplate;
        this.headers = headers;
        this.serviceUrl = serviceUrl;
    }

    @Override
    protected String getEntityName() {
        return "Location";
    }

    @Override
    protected Class<Location> getEntityClass() {
        return Location.class;
    }

    /**
     * Get locations - matches Python's getLocations function
     */
    public String getLocations() {
        // Build URL with pagination to limit results to 5
        String url = UriComponentsBuilder.fromHttpUrl(serviceUrl)
                .queryParam("pageSize", MAX_PAGE_SIZE)
                .toUriString();
        
        HttpHeaders requestHeaders = createRequestHeaders();
        HttpEntity<String> requestEntity = new HttpEntity<>(requestHeaders);

        ResponseEntity<ApiResponse<Location>> response = serviceTemplate.exchange(
                url,
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<ApiResponse<Location>>() {}
        );

        logResponse("getLocations", response);

        ApiResponse<Location> body = response.getBody();
        List<Location> locations = body != null ? body.getData() : Collections.emptyList();

        if (!locations.isEmpty()) {
            String locationId = locations.get(0).getId().toString();
            log.info("Using Location ID: {}", locationId);
            return locationId;
        }
        throw new RuntimeException("No locations found");
    }

    /**
     * Legacy method for backward compatibility
     */
    public String getLocationId() {
        return getLocations();
    }
} 