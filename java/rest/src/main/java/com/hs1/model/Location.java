package com.hs1.model;

import lombok.Data;
import java.time.ZonedDateTime;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class Location {
    private Long id;
    private String name;
    private String type;
    private String address1;
    private String address2;
    private String city;
    private String state;
    private String postalCode;
    private String phone;
    private String email;
    private String timeZone;
    private ZonedDateTime lastModified;
}
