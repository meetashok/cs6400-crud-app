-- CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
CREATE USER IF NOT EXISTS gatechUser@localhost IDENTIFIED BY 'gatech123';

DROP DATABASE IF EXISTS `cs6400_sm19_team013`; 
SET default_storage_engine=InnoDB;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS cs6400_sm19_team013 
  DEFAULT CHARACTER SET utf8mb4 
  DEFAULT COLLATE utf8mb4_unicode_ci;
USE cs6400_fa17_team001;

GRANT SELECT, INSERT, UPDATE, DELETE, FILE ON *.* TO 'gatechUser'@'localhost';
GRANT ALL PRIVILEGES ON `gatechuser`.* TO 'gatechUser'@'localhost';
GRANT ALL PRIVILEGES ON `cs6400_sm19_team013`.* TO 'gatechUser'@'localhost';
FLUSH PRIVILEGES;

-- Tables
-- Should we start the table names with capitals? 

CREATE TABLE `User` (
  login_username varchar(20) NOT NULL,
  login_password varchar(20) NOT NULL,
  user_first_name varchar(50) NOT NULL,
  user_last_name varchar(50) NOT NULL,
  user_role varchar(25) NOT NULL, -- should we limit the size of role to a single character? Also, change in relationship mapping 
  PRIMARY KEY (login_username)
);

CREATE TABLE Customer (
  customer_id int(32) unsigned NOT NULL AUTO_INCREMENT,
  phone_number int(10) unsigned NOT NULL, -- Should be varchar, They advised against phone number being 10 digits it. e.g phone numbers with extension
  email varchar(50) NOT NULL,
  street varchar(50) NOT NULL,
  city varchar(50) NOT NULL,
  state_name varchar(50) NOT NULL,
  postal_code int(10) NOT NULL, -- should be varchar
  PRIMARY KEY (customer_id),
  UNIQUE KEY (email)
);

CREATE TABLE Individual (
  driver_license_number varchar(50) NOT NULL,
  customer_id int(32) unsigned NOT NULL,
  individual_first_name varchar(50) NOT NULL,
  individual_last_name varchar(50) NOT NULL,
  PRIMARY KEY (driver_license_number),
  UNIQUE KEY (customer_id)
);

CREATE TABLE Business (
  tax_id_number varchar(50) NOT NULL,
  customer_id int(32) unsigned NOT NULL,
  business_name varchar(50) NOT NULL,
  primary_contact_name varchar(50) NOT NULL,
  primacy_contact_title varchar(50) NOT NULL,
  PRIMARY KEY (tax_id_number),
  UNIQUE KEY (customer_id)
);

CREATE TABLE Sale (
  vin varchar(50) NOT NULL,
  customer_id int(32) unsigned NOT NULL,
  login_username varchar(50) NOT NULL,
  sales_date date NOT NULL
  PRIMARY KEY (vin)
);

CREATE TABLE Purchase (
  vin varchar(50) NOT NULL,
  customer_id int(32) unsigned NOT NULL,
  login_username varchar(50) NOT NULL,
  purchase_date date NOT NULL,
  PRIMARY KEY (vin)
);

CREATE TABLE Vehicle (
  vin varchar(50) NOT NULL,
  manufacturer_name varchar(50) NOT NULL,
  vehicle_type varchar(50) NOT NULL,
  model_year int(11) NOT NULL,
  model_name varchar(50) NOT NULL,
  mileage float(8) NOT NULL,
  vehicle_condition varchar(10) NOT NULL,
  vehicle_description varchar(200) NOT NULL, -- change in relationship mapping 
  sales_price float(8) NOT NULL,
  kelly_blue_book_value float(8) NOT NULL,
  PRIMARY KEY (vin)
);

CREATE TABLE VehicleColor (
  vin varchar(50) NOT NULL,
  color varchar(50) NOT NULL,
  PRIMARY KEY (vin, color) -- Need to check
);

CREATE TABLE Manufacturer (
  manufacturer_name varchar(50) NOT NULL,
  PRIMARY KEY (manufacturer_name)
);

CREATE TABLE VehicleType (
  vehicle_type varchar(50) NOT NULL,
  PRIMARY KEY (type_name)
);

CREATE TABLE Repair (
  vin varchar(50) NOT NULL,
  repair_start_date date NOT NULL, -- change in relationship mapping 
  repair_end_date date NOT NULL,
  vendor_name varchar(50) NOT NULL,
  nhtsa_number varchar(50) NULL,
  total_cost float(8) NOT NULL,
  repair_description varchar(200) NOT NULL, -- need to check if this can be NULL
  vehicle_status varchar(1) NOT NULL, -- change in relationship mapping 
  PRIMARY KEY (vin, repair_start_date) -- need to check 
);

CREATE TABLE Vendor (
  vendor_name varchar(50) NOT NULL,
  vendor_phone_number varchar(20) NOT NULL,
  street varchar(50) NOT NULL,
  city varchar(50) NOT NULL,
  state_name varchar(50) NOT NULL,
  postal_code varchar(10) NOT NULL, -- should be varchar
  PRIMARY KEY (vendor_name)
);

CREATE TABLE Recall (
  nhtsa_number varchar(50) NOT NULL, --change in relationship mapping 
  manufacturer_name varchar(50) NOT NULL,
  recall_description varchar(200) NOT NULL, --change in relationship mapping 
  PRIMARY KEY (nhtsa_number)
);

-- Constraints   Foreign Keys: FK_ChildTable_childColumn_ParentTable_parentColumn

ALTER TABLE Individual
  ADD CONSTRAINT fk_Individual_customer_id_Customer_customer_id FOREIGN KEY (customer_id) REFERENCES Customer (customer_id);
  
ALTER TABLE Business
  ADD CONSTRAINT fk_Business_customer_id_Customer_customer_id FOREIGN KEY (customer_id) REFERENCES Customer (customer_id);

ALTER TABLE Sale
  ADD CONSTRAINT fk_Sale_customer_id_Customer_customer_id FOREIGN KEY (customer_id) REFERENCES Customer (customer_id);
  ADD CONSTRAINT fk_Sale_login_username_User_login_username FOREIGN KEY (login_username) REFERENCES User (login_username);
  ADD CONSTRAINT fk_Sale_vin_Vehicle_vin FOREIGN KEY (vin) REFERENCES Vehicle (vin);

ALTER TABLE Purchase
  ADD CONSTRAINT fk_Purchase_customer_id_Customer_customer_id FOREIGN KEY (customer_id) REFERENCES Customer (customer_id);
  ADD CONSTRAINT fk_Purchase_login_username_User_login_username FOREIGN KEY (login_username) REFERENCES User (login_username);
  ADD CONSTRAINT fk_Purchase_vin_Vehicle_vin FOREIGN KEY (vin) REFERENCES Vehicle (vin);

ALTER TABLE VehicleColor
  ADD CONSTRAINT fk_VehicleColor_vin_Vehicle_vin FOREIGN KEY (vin) REFERENCES Vehicle (vin);

ALTER TABLE Repair
  ADD CONSTRAINT fk_Repair_vin_Vehicle_vin FOREIGN KEY (vin) REFERENCES Vehicle (vin);
  ADD CONSTRAINT fk_Repair_vin_Vendor_vendor_name FOREIGN KEY (vendor_name) REFERENCES Vendor (vendor_name);
  ADD CONSTRAINT fk_Repair_nhtsa_number_Recall_nhtsa_number FOREIGN KEY (nhtsa_number) REFERENCES Recall (nhtsa_number);