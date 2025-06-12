package com.hs1.model;

import lombok.Data;

import java.time.ZonedDateTime;

@Data
public class Event {
    private Long id;
    private Integer duration;
    private String type;
    private String title;
    private String recurrenceStart;
    private String recurrenceEnd;
    private String recurrenceType;
    private Integer recurrenceFrequency;
    private ZonedDateTime lastModified;
    private ZonedDateTime start;
    private ZonedDateTime end;
    private boolean allDay;
    private Location location;
}
