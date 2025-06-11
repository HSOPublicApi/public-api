package com.hs1.model;

import lombok.Data;
import java.time.ZonedDateTime;

@Data
public class PracticeProcedure {
    private Long id;
    private String code;
    private String name;
    private String description;
    private String category;
    private String type;
    private Double defaultDuration;
    private Boolean active;
    private Location location;
    private Provider provider;
    private ZonedDateTime lastModified;
} 