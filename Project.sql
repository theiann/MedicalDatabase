CREATE SCHEMA cs3380_project;
USE cs3380_project;

CREATE TABLE INSURANCE (
	I_id int,
    Name varchar(255) NOT NULL,
    Phone varchar(20) NOT NULL,
    Plan varchar(255) NOT NULL,
    PRIMARY KEY (I_id)
);

CREATE TABLE PATIENT (
	P_id int,
    P_Name varchar(255) NOT NULL,
    Sex char NOT NULL,
    DOB date NOT NULL,
    Address varchar(255),
    I_id int,
    PRIMARY KEY (P_id),
    FOREIGN KEY (I_id) REFERENCES INSURANCE(I_id)
);

CREATE TABLE MEDICATIONS (
	P_id int,
    Medication_name varchar(255) NOT NULL,
    Frequency varchar(255) NOT NULL,
    Dosage varchar(255) NOT NULL,
    FOREIGN KEY (P_id) REFERENCES PATIENT(P_id)
);

CREATE TABLE SURGERY_HISTORY (
	P_id int,
    Surgery_type varchar(255) NOT NULL,
    Surgery_date date NOT NULL,
    Doctor_name varchar(255) NOT NULL,
    FOREIGN KEY (P_id) REFERENCES PATIENT(P_id)
);

CREATE TABLE BILLING (
	B_id int,
	P_id int,
    I_id int,
    Due_date date NOT NULL,
    Total_owed float NOT NULL,
    Amount_paid float,
    PRIMARY KEY (B_id),
    FOREIGN KEY (P_id) REFERENCES PATIENT(P_id),
    FOREIGN KEY (I_id) REFERENCES INSURANCE(I_id)
);

CREATE TABLE OWES (
	P_id int,
    B_id int,
    FOREIGN KEY (P_id) REFERENCES PATIENT(P_id),
    FOREIGN KEY (B_id) REFERENCES BILLING(B_id)
);

CREATE TABLE PATIENT_PHONES (
	P_id int,
    Phone varchar(20) NOT NULL,
    FOREIGN KEY (P_id) REFERENCES PATIENT(P_id)
);
    
    