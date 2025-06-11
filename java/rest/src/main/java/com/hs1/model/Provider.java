package com.hs1.model;

import lombok.Data;
import java.time.ZonedDateTime;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class Provider {
    private Long id;
    private String firstName;
    private String lastName;
    private String speciality;
    private String npi;
    private String email;
    private String phone;
    private Location primaryLocation;
    private ZonedDateTime lastModified;
} 