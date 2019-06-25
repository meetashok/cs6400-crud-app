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
CREATE TABLE `user` (
  login_username varchar(20) NOT NULL,
  login_password varchar(20) NOT NULL,
  user_first_name varchar(50) NOT NULL,
  user_last_name varchar(50) NOT NULL,
  user_role varchar(25) NOT NULL, -- should we limit the size of role to a single character? Also, change in relationship mapping 
  PRIMARY KEY (login_username)
);

CREATE TABLE customer (
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

CREATE TABLE individual (
  driver_license_number varchar(50) NOT NULL,
  customer_id int(32) unsigned NOT NULL,
  individual_first_name varchar(50) NOT NULL,
  individual_last_name varchar(50) NOT NULL,
  PRIMARY KEY (driver_license_number),
  UNIQUE KEY (customer_id)
);

CREATE TABLE business (
  tax_id_number varchar(50) NOT NULL,
  customer_id int(32) unsigned NOT NULL,
  business_name varchar(50) NOT NULL,
  primary_contact_name varchar(50) NOT NULL,
  primacy_contact_title varchar(50) NOT NULL,
  PRIMARY KEY (tax_id_number),
  UNIQUE KEY (customer_id)
);

CREATE TABLE sale (
  vin varchar(50) NOT NULL,
  customer_id int(32) unsigned NOT NULL,
  login_username varchar(50) NOT NULL,
  sales_date date NOT NULL
  PRIMARY KEY (vin)
);

CREATE TABLE purchase (
  vin varchar(50) NOT NULL,
  customer_id int(32) unsigned NOT NULL,
  login_username varchar(50) NOT NULL,
  purchase_date date NOT NULL,
  PRIMARY KEY (vin)
);

CREATE TABLE vehicle (
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

CREATE TABLE vehicleColor (
  vin varchar(50) NOT NULL,
  color varchar(50) NOT NULL,
  PRIMARY KEY (vin, color) -- Need to check
);

CREATE TABLE manufacturer (
  manufacturer_name varchar(50) NOT NULL,
  PRIMARY KEY (manufacturer_name)
);

CREATE TABLE vehicleType (
  vehicle_type varchar(50) NOT NULL,
  PRIMARY KEY (type_name)
);

CREATE TABLE repair (
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

CREATE TABLE vendor (
  vendor_name varchar(50) NOT NULL,
  vendor_phone_number varchar(20) NOT NULL,
  street varchar(50) NOT NULL,
  city varchar(50) NOT NULL,
  state_name varchar(50) NOT NULL,
  postal_code varchar(10) NOT NULL, -- should be varchar
  PRIMARY KEY (vendor_name)
);

CREATE TABLE recall (
  nhtsa_number varchar(50) NOT NULL, --change in relationship mapping 
  manufacturer_name varchar(50) NOT NULL,
  recall_description varchar(200) NOT NULL, --change in relationship mapping 
  PRIMARY KEY (nhtsa_number)
);

-- Constraints   Foreign Keys: FK_ChildTable_childColumn_ParentTable_parentColumn

ALTER TABLE individual
  ADD CONSTRAINT fk_Individual_customer_id_Customer_customer_id FOREIGN KEY (customer_id) REFERENCES customer (customer_id);
  
ALTER TABLE business
  ADD CONSTRAINT fk_Business_customer_id_Customer_customer_id FOREIGN KEY (customer_id) REFERENCES customer (customer_id);

ALTER TABLE sale
  ADD CONSTRAINT fk_Sale_customer_id_Customer_customer_id FOREIGN KEY (customer_id) REFERENCES customer (customer_id);
ALTER TABLE sale
  ADD CONSTRAINT fk_Sale_login_username_User_login_username FOREIGN KEY (login_username) REFERENCES `user` (login_username);
ALTER TABLE sale
  ADD CONSTRAINT fk_Sale_vin_Vehicle_vin FOREIGN KEY (vin) REFERENCES vehicle (vin);

ALTER TABLE purchase
  ADD CONSTRAINT fk_Purchase_customer_id_Customer_customer_id FOREIGN KEY (customer_id) REFERENCES customer (customer_id);
ALTER TABLE sale
  ADD CONSTRAINT fk_Purchase_login_username_User_login_username FOREIGN KEY (login_username) REFERENCES `user` (login_username);
ALTER TABLE sale
  ADD CONSTRAINT fk_Purchase_vin_Vehicle_vin FOREIGN KEY (vin) REFERENCES vehicle (vin);

ALTER TABLE vehicleColor
  ADD CONSTRAINT fk_VehicleColor_vin_Vehicle_vin FOREIGN KEY (vin) REFERENCES vehicle (vin);

ALTER TABLE repair
  ADD CONSTRAINT fk_Repair_vin_Vehicle_vin FOREIGN KEY (vin) REFERENCES vehicle (vin);
ALTER TABLE sale
  ADD CONSTRAINT fk_Repair_vin_Vendor_vendor_name FOREIGN KEY (vendor_name) REFERENCES vendor (vendor_name);
ALTER TABLE sale
  ADD CONSTRAINT fk_Repair_nhtsa_number_Recall_nhtsa_number FOREIGN KEY (nhtsa_number) REFERENCES recall (nhtsa_number);
