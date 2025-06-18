package com.hs1.service;

import com.hs1.model.Appointment;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@Component
@Slf4j
public class AppointmentService extends TemplateMethodService<Appointment> {

    public AppointmentService(RestTemplate serviceTemplate, HttpHeaders headers, @Value("${appointments.url}") String serviceUrl) {
        this.serviceTemplate = serviceTemplate;
        this.headers = headers;
        this.serviceUrl = serviceUrl;
    }

    @Override
    protected String getEntityName() {
        return "Appointment";
    }

    @Override
    protected Class<Appointment> getEntityClass() {
        return Appointment.class;
    }

    /**
     * Creates appointment data - matches Python's getAppointmentData function
     */
    public static Map<String, Object> getAppointmentData(String patientId, String providerId, String operatoryId) {
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

    /**
     * Create appointment - matches Python's createAppointment function
     */
    public String createAppointment(String patientId, String providerId, String operatoryId) {
        Map<String, Object> appointmentData = getAppointmentData(patientId, providerId, operatoryId);
        return create(appointmentData);
    }

    /**
     * Update appointment - matches Python's updateAppointment function
     */
    public void updateAppointment(String appointmentId, String patientId, String providerId, String operatoryId) {
        Map<String, Object> appointmentData = getAppointmentData(patientId, providerId, operatoryId);
        appointmentData.put("status", "HERE"); // Update status like Python version
        update(appointmentId, appointmentData);
    }

    /**
     * Get appointment by ID - matches Python's getAppointmentById function
     */
    public Appointment getAppointmentById(String appointmentId) {
        return findById(appointmentId);
    }

    /**
     * Delete appointment - matches Python's deleteAppointment function
     */
    public void deleteAppointment(String appointmentId) {
        delete(appointmentId);
    }
} 