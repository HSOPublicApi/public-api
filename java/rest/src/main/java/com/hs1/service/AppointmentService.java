package com.hs1.service;

import com.hs1.model.ApiResponse;
import com.hs1.model.Appointment;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Collections;

@Component
@Slf4j
public class AppointmentService extends TemplateMethodService<Appointment> {

    public AppointmentService(RestTemplate serviceTemplate, HttpHeaders headers, @Value("${appointments.url}") String serviceUrl) {
        this.serviceTemplate = serviceTemplate;
        this.headers = headers;
        this.serviceUrl = serviceUrl;
    }

    @SneakyThrows
    public List<Appointment> findAll() {
        // Build the HTTP entity
        HttpHeaders requestHeaders = new HttpHeaders(headers);
        requestHeaders.add("Organization-ID", "5c8958ef64c9477daadf664e");
        HttpEntity<String> requestEntity = new HttpEntity<>(requestHeaders);

        ResponseEntity<ApiResponse<Appointment>> response = serviceTemplate.exchange(
                serviceUrl,
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<ApiResponse<Appointment>>() {}
        );

        logResponse("findAll Appointments", response);

        ApiResponse<Appointment> body = response.getBody();
        List<Appointment> appointments = body != null ? body.getData() : Collections.emptyList();

        return appointments;
    }

    @SneakyThrows
    public String createAppointment(String patientId, String providerId, String operatoryId) {
        HttpHeaders requestHeaders = new HttpHeaders(headers);
        requestHeaders.add("Organization-ID", "5c8958ef64c9477daadf664e");
        requestHeaders.setContentType(MediaType.APPLICATION_JSON);

        Map<String, Object> appointmentData = createAppointmentData(patientId, providerId, operatoryId);
        
        HttpEntity<Map<String, Object>> requestEntity = new HttpEntity<>(appointmentData, requestHeaders);

        ResponseEntity<Map<String, Object>> response = serviceTemplate.exchange(
                serviceUrl,
                HttpMethod.POST,
                requestEntity,
                new ParameterizedTypeReference<Map<String, Object>>() {}
        );

        logResponse("createAppointment", response);

        if (response.getBody() != null && response.getBody().containsKey("data")) {
            Map<String, Object> data = (Map<String, Object>) response.getBody().get("data");
            return data.get("id").toString();
        }
        throw new RuntimeException("Failed to create appointment");
    }

    @SneakyThrows
    public void updateAppointment(String appointmentId, String patientId, String providerId, String operatoryId) {
        String url = serviceUrl + "/" + appointmentId;
        
        HttpHeaders requestHeaders = new HttpHeaders(headers);
        requestHeaders.add("Organization-ID", "5c8958ef64c9477daadf664e");
        requestHeaders.setContentType(MediaType.APPLICATION_JSON);

        Map<String, Object> appointmentData = createAppointmentData(patientId, providerId, operatoryId);
        appointmentData.put("status", "HERE"); // Update status like Python version
        
        HttpEntity<Map<String, Object>> requestEntity = new HttpEntity<>(appointmentData, requestHeaders);

        ResponseEntity<Map<String, Object>> response = serviceTemplate.exchange(
                url,
                HttpMethod.PUT,
                requestEntity,
                new ParameterizedTypeReference<Map<String, Object>>() {}
        );

        logResponse("updateAppointment", response);
    }

    @SneakyThrows
    public void deleteAppointment(String appointmentId) {
        String url = serviceUrl + "/" + appointmentId;
        
        HttpHeaders requestHeaders = new HttpHeaders(headers);
        requestHeaders.add("Organization-ID", "5c8958ef64c9477daadf664e");
        HttpEntity<String> requestEntity = new HttpEntity<>(requestHeaders);

        ResponseEntity<String> response = serviceTemplate.exchange(
                url,
                HttpMethod.DELETE,
                requestEntity,
                String.class
        );

        logResponse("deleteAppointment", response);
    }

    private Map<String, Object> createAppointmentData(String patientId, String providerId, String operatoryId) {
        Map<String, Object> appointmentData = new HashMap<>();
        appointmentData.put("start", "2025-01-01T17:00:00.000Z");
        
        Map<String, Object> patient = new HashMap<>();
        patient.put("id", patientId);
        appointmentData.put("patient", patient);
        
        Map<String, Object> provider = new HashMap<>();
        provider.put("id", providerId);
        appointmentData.put("provider", provider);
        
        Map<String, Object> operatory = new HashMap<>();
        operatory.put("id", operatoryId);
        appointmentData.put("operatory", operatory);
        
        appointmentData.put("needsPremedicate", false);
        appointmentData.put("insuranceEligibilityVerified", "2024-01-01");
        appointmentData.put("status", "LATE");
        appointmentData.put("note", "My appointment test Note!!");
        appointmentData.put("other", "My Other Test Note!!");
        appointmentData.put("bookedOnline", false);
        appointmentData.put("needsFollowup", false);
        
        return appointmentData;
    }
} 