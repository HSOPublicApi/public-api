package com.hs1.service;

import com.hs1.model.ApiResponse;
import com.hs1.model.Patient;
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

    @SneakyThrows
    public List<Patient> findAll() {
        // Build the HTTP entity
        HttpHeaders requestHeaders = new HttpHeaders(headers);
        requestHeaders.add("Organization-ID", "5c8958ef64c9477daadf664e");
        HttpEntity<String> requestEntity = new HttpEntity<>(requestHeaders);

        ResponseEntity<ApiResponse<Patient>> response = serviceTemplate.exchange(
                serviceUrl,
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<ApiResponse<Patient>>() {}
        );

        logResponse("getPatients", response);

        ApiResponse<Patient> body = response.getBody();
        List<Patient> patients = body != null ? body.getData() : Collections.emptyList();

        return patients;
    }

    @SneakyThrows
    public String getPatientId(String locationId) {
        // Simplified approach - just get first available patient
        // Build URL with basic pagination (without location filter since API doesn't support it)
        String url = UriComponentsBuilder.fromHttpUrl(serviceUrl)
                .queryParam("pageSize", 10)
                .toUriString();

        // Build the HTTP entity
        HttpHeaders requestHeaders = new HttpHeaders(headers);
        requestHeaders.add("Organization-ID", "5c8958ef64c9477daadf664e");
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
} 