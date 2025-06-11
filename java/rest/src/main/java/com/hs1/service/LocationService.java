package com.hs1.service;

import com.hs1.model.ApiResponse;
import com.hs1.model.Location;
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
public class LocationService extends TemplateMethodService<Location> {

    public LocationService(RestTemplate serviceTemplate, HttpHeaders headers, @Value("${locations.url}") String serviceUrl) {
        this.serviceTemplate = serviceTemplate;
        this.headers = headers;
        this.serviceUrl = serviceUrl;
    }

    @SneakyThrows
    public List<Location> findAll() {
        // Build the HTTP entity
        HttpHeaders requestHeaders = new HttpHeaders(headers);
        requestHeaders.add("Organization-ID", "5c8958ef64c9477daadf664e");
        HttpEntity<String> requestEntity = new HttpEntity<>(requestHeaders);

        ResponseEntity<ApiResponse<Location>> response = serviceTemplate.exchange(
                serviceUrl,
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<ApiResponse<Location>>() {}
        );

        logResponse("getLocations", response);

        ApiResponse<Location> body = response.getBody();
        List<Location> locations = body != null ? body.getData() : Collections.emptyList();

        return locations;
    }

    @SneakyThrows
    public Location findById(String locationId) {
        return super.findById(locationId, Location.class, "Location");
    }

    @SneakyThrows
    public String getLocationId() {
        List<Location> locations = findAll();
        if (!locations.isEmpty()) {
            String locationId = locations.get(0).getId().toString();
            log.info("Using Location ID: {}", locationId);
            return locationId;
        }
        throw new RuntimeException("No locations found");
    }
} 