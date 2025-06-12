package com.hs1;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.PropertySource;

@SpringBootApplication
@PropertySource("classpath:application.properties")
public class RestApiApp {
	public static void main(String[] args) {
		SpringApplication app = new SpringApplication(RestApiApp.class);
		app.setWebApplicationType(WebApplicationType.NONE); // Disable web server
		app.run(args);
	}
} 