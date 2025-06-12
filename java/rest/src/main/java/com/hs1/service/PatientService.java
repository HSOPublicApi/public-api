package com.hs1.service;

import com.hs1.model.ApiResponse;
import com.hs1.model.Patient;
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
public class PatientService extends TemplateMethodService<Patient> {

    public PatientService(RestTemplate serviceTemplate, HttpHeaders headers, @Value("${patients.url}") String serviceUrl) {
        this.serviceTemplate = serviceTemplate;
        this.headers = headers;
        this.serviceUrl = serviceUrl;
    }

    @Override
    protected String getEntityName() {
        return "Patient";
    }

    @Override
    protected Class<Patient> getEntityClass() {
        return Patient.class;
    }

    /**
     * Get patients - matches Python's getPatients function
     */
    public String getPatients(String locationId) {
        // Build URL with pagination limited to 1 result to avoid timeouts
        String url = UriComponentsBuilder.fromHttpUrl(serviceUrl)
                .queryParam("pageSize", MAX_PAGE_SIZE)
                .toUriString();

        // Build the HTTP entity
        HttpHeaders requestHeaders = createRequestHeaders();
        HttpEntity<String> requestEntity = new HttpEntity<>(requestHeaders);

        ResponseEntity<ApiResponse<Patient>> response = serviceTemplate.exchange(
                url,
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<ApiResponse<Patient>>() {}
        );

        logResponse("getPatients", response);

        ApiResponse<Patient> body = response.getBody();
        List<Patient> patients = body != null ? body.getData() : Collections.emptyList();

        if (!patients.isEmpty()) {
            String patientId = patients.get(0).getId().toString();
            log.info("Using Patient ID: {} (from first available patient)", patientId);
            return patientId;
        }
        throw new RuntimeException("No patients found");
    }

    /**
     * Legacy method for backward compatibility
     */
    public String getPatientId(String locationId) {
        return getPatients(locationId);
    }
} 