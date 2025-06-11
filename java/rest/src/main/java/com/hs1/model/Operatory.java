package com.hs1.model;

import lombok.Data;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class Operatory {
    private Long id;
    private String name;
    private String description;
    private Boolean active;
    private Location location;
} 