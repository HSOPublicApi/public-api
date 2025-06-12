package com.hs1;

import java.util.Collections;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.web.client.RestTemplate;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.fasterxml.jackson.databind.SerializationFeature;

@Configuration
@ComponentScan({"com.hs1"})
public class AppConfig {
	
	//@Value("${organization.id}")
	//private String organizationId;
	
	@Value("${authentication.url}")
	private String authenticationUrl;
	
	@Value("${client_id}")
	private String clientId;
	@Value("${client_secret}")
	private String clientSecret;
	
	@Bean
	public ObjectMapper objectMapper() {
		ObjectMapper mapper = new ObjectMapper();
		mapper.registerModule(new JavaTimeModule());
		mapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
		return mapper;
	}
	
	@Bean
	public Authenticator getAuthenticator() {
		Authenticator authenticator = new Authenticator(authenticationUrl, clientId, clientSecret, restTemplate());
		
		return authenticator;
	}

	@Bean
	public RestTemplate restTemplate() {
		RestTemplate restTemplate = new RestTemplate();
		MappingJackson2HttpMessageConverter mappingJackson2HttpMessageConverter = new MappingJackson2HttpMessageConverter();
		mappingJackson2HttpMessageConverter.setObjectMapper(objectMapper());
	    mappingJackson2HttpMessageConverter.setSupportedMediaTypes(Collections.singletonList(MediaType.APPLICATION_FORM_URLENCODED));
        restTemplate.getMessageConverters().add(mappingJackson2HttpMessageConverter);
        
        return restTemplate;
	}

	@Bean(name = "authenticatorTemplate")
	public RestTemplate getAuthenticatorTemplate() {
		return restTemplate();
	}
	
	@Bean(name = "serviceTemplate")
	public RestTemplate getServiceTemplate() {
		return restTemplate();
	}
	
	@Bean(name = "serviceHeaders")
	public HttpHeaders serviceHeaders() {
		// Set headers
        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(getAuthenticator().getToken());
        headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));
        
        return headers;
	}
	
}
