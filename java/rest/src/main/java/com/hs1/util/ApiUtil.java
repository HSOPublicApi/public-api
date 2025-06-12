package com.hs1.util;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;

/**
 * Utility class that matches Python's util.py functionality
 */
@Slf4j
public class ApiUtil {
    
    public static final String BASE_URL = "https://prod.hs1api.com/ascend-gateway/api"; // Henry Schein One base URL
    
    private static final ObjectMapper objectMapper = new ObjectMapper();
    
    /**
     * Print response - matches Python's printResponse function exactly
     */
    public static void printResponse(String requestName, ResponseEntity<?> response) {
        log.info("");
        log.info(requestName);
        log.info("status code: {}", response.getStatusCode().value());
        
        try {
            String responseBody = objectMapper.writerWithDefaultPrettyPrinter()
                    .writeValueAsString(response.getBody());
            log.info("{}", responseBody);
        } catch (Exception e) {
            log.info("Response: {}", response.getBody());
        }
    }
} 