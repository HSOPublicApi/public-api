package com.hs1;

import java.util.Map;
import java.util.Objects;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import org.springframework.core.ParameterizedTypeReference;

import lombok.extern.slf4j.Slf4j;

@Slf4j
public class Authenticator {
	
	private static final String CLIENT_ID_PARAM = "client_id";
	private static final String CLIENT_SECRET_PARAM = "client_secret";
	private static final String ACCESS_TOKEN_KEY = "access_token";
	
	private final String authenticationUrl;
	private final String clientId;
	private final String clientSecret;
	private final RestTemplate restTemplate;

	public Authenticator(String authenticationUrl, String clientId, String clientSecret, RestTemplate restTemplate) {
		this.authenticationUrl = Objects.requireNonNull(authenticationUrl, "authenticationUrl must not be null");
		this.clientId = Objects.requireNonNull(clientId, "clientId must not be null");
		this.clientSecret = Objects.requireNonNull(clientSecret, "clientSecret must not be null");
		this.restTemplate = Objects.requireNonNull(restTemplate, "restTemplate must not be null");
	}
	
	public String getToken() {
		try {
			HttpEntity<MultiValueMap<String, String>> requestEntity = buildTokenRequest();
			ResponseEntity<Map<String, Object>> response = sendTokenRequest(requestEntity);
			return extractToken(response);
		} catch (RestClientException e) {
			log.error("Failed to communicate with authentication service", e);
			throw new AuthenticationException("Failed to obtain authentication token", e);
		}
	}

	private HttpEntity<MultiValueMap<String, String>> buildTokenRequest() {
		HttpHeaders headers = new HttpHeaders();
		headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

		MultiValueMap<String, String> body = new LinkedMultiValueMap<>();
		body.add(CLIENT_ID_PARAM, clientId);
		body.add(CLIENT_SECRET_PARAM, clientSecret);
		
		return new HttpEntity<>(body, headers);
	}

	private ResponseEntity<Map<String, Object>> sendTokenRequest(HttpEntity<MultiValueMap<String, String>> requestEntity) {
		return restTemplate.exchange(
			authenticationUrl,
			HttpMethod.POST,
			requestEntity,
			new ParameterizedTypeReference<Map<String, Object>>() {}
		);
	}

	private String extractToken(ResponseEntity<Map<String, Object>> response) {
		if (!response.getStatusCode().is2xxSuccessful()) {
			log.error("Authentication failed. Response code: {}", response.getStatusCode());
			log.debug("Response body: {}", response.getBody());
			throw new AuthenticationException("Authentication failed with status: " + response.getStatusCode());
		}

		Map<String, Object> responseBody = response.getBody();
		if (responseBody == null || !responseBody.containsKey(ACCESS_TOKEN_KEY)) {
			log.error("Invalid authentication response. Missing access token");
			throw new AuthenticationException("Invalid authentication response: missing access token");
		}

		Object tokenObj = responseBody.get(ACCESS_TOKEN_KEY);
		if (tokenObj == null || !(tokenObj instanceof String)) {
			log.error("Invalid authentication response. Token is not a string value");
			throw new AuthenticationException("Invalid authentication response: token is not a string value");
		}

		String token = (String) tokenObj;
		if (token.isEmpty()) {
			log.error("Invalid authentication response. Empty access token");
			throw new AuthenticationException("Invalid authentication response: empty access token");
		}

		return token;
	}
}
