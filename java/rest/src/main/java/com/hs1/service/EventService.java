package com.hs1.service;

import com.hs1.model.Event;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
@Slf4j
public class EventService extends TemplateMethodService<Event> {

    public EventService(RestTemplate serviceTemplate, HttpHeaders headers, @Value("${events.url}") String serviceUrl) {
        this.serviceTemplate = serviceTemplate;
        this.headers = headers;
        this.serviceUrl = serviceUrl;
    }

    @Override
    protected String getEntityName() {
        return "Event";
    }

    @Override
    protected Class<Event> getEntityClass() {
        return Event.class;
    }
}

