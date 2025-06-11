package com.hs1;

import com.hs1.service.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class DemoRunner implements CommandLineRunner {

    private final AppointmentService appointmentService;
    private final LocationService locationService;
    private final PatientService patientService;
    private final ProviderService providerService;
    private final OperatoryService operatoryService;

    @Value("${organization.id:5c8958ef64c9477daadf664e}")
    private String organizationId;

    @Override
    public void run(String... args) {
        log.info("=== Starting PAPI Demo with Organization ID: {} ===", organizationId);
        log.info("This demo follows the same workflow as the Python version:");
        log.info("1. Get required data (locations, patients, providers, operatories)");
        log.info("2. Create appointment");
        log.info("3. Update appointment");
        log.info("4. Get appointment by ID");
        log.info("5. Delete appointment");
        log.info("Each API call will show detailed request/response information.\n");

        try {
            // Step 1: Get data needed for future requests (like Python version)
            log.info("=== Step 1: Getting required data ===");
            String locationId = locationService.getLocationId();
            String patientId = patientService.getPatientId(locationId);
            String providerId = providerService.getProviderId();
            String operatoryId = operatoryService.getOperatoryId();

            // Step 2: Create appointment (like Python version)
            log.info("\n=== Step 2: Creating appointment ===");
            String appointmentId = appointmentService.createAppointment(patientId, providerId, operatoryId);
            log.info("Created appointment with ID: {}", appointmentId);

            // Step 3: Update appointment (like Python version)
            log.info("\n=== Step 3: Updating appointment ===");
            appointmentService.updateAppointment(appointmentId, patientId, providerId, operatoryId);
            log.info("Updated appointment with ID: {}", appointmentId);

            // Step 4: Get appointment by ID (like Python version) - using inherited method
            log.info("\n=== Step 4: Getting appointment by ID ===");
            appointmentService.findById(appointmentId, com.hs1.model.Appointment.class, "Appointment");

            // Step 5: Delete appointment (like Python version)
            log.info("\n=== Step 5: Deleting appointment ===");
            appointmentService.deleteAppointment(appointmentId);
            log.info("Deleted appointment with ID: {}", appointmentId);

            log.info("\n=== Demo completed successfully! ===");
            log.info("This demo showed the same CRUD workflow as the Python version.");
            log.info("Each API call displayed detailed request/response information.");

        } catch (Exception e) {
            log.error("Error during demo execution", e);
            log.error("Demo failed. Please check your API credentials and network connectivity.");
        }
    }
} 