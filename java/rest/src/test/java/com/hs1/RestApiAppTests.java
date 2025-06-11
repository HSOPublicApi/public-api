package com.hs1;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@TestPropertySource(locations = "classpath:application-test.properties")
class RestApiAppTests {

    @Autowired
    private Authenticator authenticator;

    @Value("${client_id}")
    private String clientId;

    @Value("${client_secret}")
    private String clientSecret;

    @Test
    void contextLoads() {
        assertNotNull(authenticator, "Authenticator should be autowired");
    }

    @Test
    void getJwtToken_shouldReturnValidToken() {
        // When
        String token = authenticator.getToken();

        // Then
        assertNotNull(token, "Token should not be null");
        assertFalse(token.isEmpty(), "Token should not be empty");
    }

    @Test
    void verifyCredentials_shouldBeConfigured() {
        // Then
        assertNotNull(clientId, "Client ID should be configured");
        assertFalse(clientId.isEmpty(), "Client ID should not be empty");
        assertNotNull(clientSecret, "Client Secret should be configured");
        assertFalse(clientSecret.isEmpty(), "Client Secret should not be empty");
    }
} 