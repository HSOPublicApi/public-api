package com.hs1.model;

import lombok.Data;

import java.util.Date;

@Data
public class Transaction {

    private Integer id;
    private Date lastModified;
    private String type;
    private String email;
    private String address1;
    private String city;
    private String state;
    private String postalCode;
    private String phone;
    private String name;
    private String timeZone;

}