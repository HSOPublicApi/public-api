package com.hs1.service;

import com.hs1.model.ApiResponse;
import lombok.SneakyThrows;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import com.hs1.model.Transaction;
import lombok.extern.slf4j.Slf4j;

@Component
@Slf4j
public class OrganizationService extends TemplateMethodService<Transaction> {

	public OrganizationService(RestTemplate serviceTemplate, HttpHeaders headers, @Value("${organizations.url}") String serviceUrl) {
		this.serviceTemplate = serviceTemplate;
		this.headers = headers;
		this.serviceUrl = serviceUrl;
	}

	@SneakyThrows
	public Transaction get(String organizationId) {
		// Build the HTTP entity
		HttpEntity<String> requestEntity = new HttpEntity<>(headers);
		headers.add("Organization-ID", organizationId);

		ResponseEntity<ApiResponse<Transaction>> response = serviceTemplate.exchange(
				serviceUrl,
				HttpMethod.GET,
				requestEntity,
				new ParameterizedTypeReference<ApiResponse<Transaction>>() {}
		);

		ApiResponse<Transaction> body = response.getBody();
		return body != null && !body.getData().isEmpty() ? body.getData().getFirst() : null;
	}
}
