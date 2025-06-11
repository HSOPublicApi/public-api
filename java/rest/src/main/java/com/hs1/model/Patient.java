package com.hs1.model;

import lombok.Data;
import java.time.ZonedDateTime;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class Patient {
    private Long id;
    private String firstName;
    private String lastName;
    private String dateOfBirth;
    private String gender;
    private String email;
    private String phone;
    private String address;
    private String city;
    private String state;
    private String postalCode;
    private ZonedDateTime lastModified;
} 