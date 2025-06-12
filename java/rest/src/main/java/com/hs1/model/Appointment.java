package com.hs1.model;

import lombok.Data;
import java.time.ZonedDateTime;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class Appointment {
    private Long id;
    private String type;
    private String status;
    private ZonedDateTime start;
    private ZonedDateTime end;
    private String notes;
    private Patient patient;
    private Provider provider;
    private Location location;
    private ZonedDateTime lastModified;
} 