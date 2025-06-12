package com.hs1.service;

import com.hs1.model.PracticeProcedure;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
@Slf4j
public class PracticeProcedureService extends TemplateMethodService<PracticeProcedure> {

    public PracticeProcedureService(RestTemplate serviceTemplate, HttpHeaders headers, @Value("${practiceprocedures.url}") String serviceUrl) {
        this.serviceTemplate = serviceTemplate;
        this.headers = headers;
        this.serviceUrl = serviceUrl;
    }

    @Override
    protected String getEntityName() {
        return "PracticeProcedure";
    }

    @Override
    protected Class<PracticeProcedure> getEntityClass() {
        return PracticeProcedure.class;
    }
} 