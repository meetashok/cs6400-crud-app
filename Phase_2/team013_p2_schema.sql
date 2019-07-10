CREATE USER IF NOT EXISTS gatechUser@localhost IDENTIFIED BY 'gatech123';

DROP DATABASE IF EXISTS `cs6400_sm19_team013`; 
SET default_storage_engine=InnoDB;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS cs6400_sm19_team013 
  DEFAULT CHARACTER SET utf8mb4 
  DEFAULT COLLATE utf8mb4_unicode_ci;
USE cs6400_sm19_team013;

GRANT SELECT, INSERT, UPDATE, DELETE, FILE ON *.* TO 'gatechUser'@'localhost';
GRANT ALL PRIVILEGES ON `gatechuser`.* TO 'gatechUser'@'localhost'; -- run this to check for errors
GRANT ALL PRIVILEGES ON `cs6400_sm19_team013`.* TO 'gatechUser'@'localhost';
FLUSH PRIVILEGES;


-- Tables
CREATE TABLE `user` (
  login_username varchar(20) NOT NULL,
  login_password varchar(20) NOT NULL,
  user_first_name varchar(50) NOT NULL,
  user_last_name varchar(50) NOT NULL,
  role varchar(25) NOT NULL, 
  PRIMARY KEY (login_username)
);

CREATE TABLE `customer` (
  customer_id int(32) unsigned NOT NULL AUTO_INCREMENT,
  phone_number varchar(20) NOT NULL, 
  email varchar(50) NULL,
  street varchar(50) NOT NULL,
  city varchar(50) NOT NULL,
  state varchar(50) NOT NULL,
  postal_code varchar(15) NOT NULL,
  PRIMARY KEY (customer_id)
);

CREATE TABLE `individual` (
  driver_license_number varchar(50) NOT NULL,
  customer_id int(32) unsigned NOT NULL,
  individual_first_name varchar(50) NOT NULL,
  individual_last_name varchar(50) NOT NULL,
  PRIMARY KEY (driver_license_number),
  UNIQUE KEY (customer_id)
);

CREATE TABLE `business` (
  tax_id_number varchar(50) NOT NULL,
  customer_id int(32) unsigned NOT NULL,
  business_name varchar(50) NOT NULL,
  pc_name varchar(50) NOT NULL,
  pc_title varchar(50) NOT NULL,
  PRIMARY KEY (tax_id_number),
  UNIQUE KEY (customer_id)
);

CREATE TABLE `sale` (
  vin varchar(17) NOT NULL,
  customer_id int(32) unsigned NOT NULL,
  login_username varchar(50) NOT NULL,
  sales_date timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (vin)
);

CREATE TABLE `purchase` (
  vin varchar(17) NOT NULL,
  customer_id int(32) unsigned NOT NULL,
  login_username varchar(50) NOT NULL,
  purchase_date timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (vin)
);

CREATE TABLE `vehicle` (
  vin varchar(17) NOT NULL,
  manufacturer_name varchar(50) NOT NULL,
  vehicle_type varchar(50) NOT NULL,
  model_year int(11) NOT NULL,
  model_name varchar(50) NOT NULL,
  mileage float(8) NOT NULL,
  vehicle_condition varchar(10) NOT NULL,
  vehicle_description varchar(200), 
  sales_price float(8) NOT NULL,
  kbb_value float(8) NOT NULL,
  PRIMARY KEY (vin)
);

CREATE TABLE `vehicle_color` (
  vin varchar(17) NOT NULL,
  color varchar(50) NOT NULL,
  PRIMARY KEY (vin, color) 
);

CREATE TABLE `manufacturer` (
  manufacturer_name varchar(50) NOT NULL,
  PRIMARY KEY (manufacturer_name)
);

CREATE TABLE `vehicle_type` (
  vehicle_type varchar(50) NOT NULL,
  PRIMARY KEY (vehicle_type)
);

CREATE TABLE `repair` (
  vin varchar(17) NOT NULL,
  repair_start_date date NOT NULL, 
  repair_end_date date NOT NULL,
  vendor_name varchar(50) NOT NULL,
  nhtsa_recall_number varchar(50) NULL,
  total_cost float(8) NOT NULL,
  repair_description varchar(200) NOT NULL, 
  repair_status varchar(15) NOT NULL, 
  PRIMARY KEY (vin, repair_start_date) 
);

CREATE TABLE `vendor` (
  vendor_name varchar(50) NOT NULL,
  vendor_phone_number varchar(20) NOT NULL,
  street varchar(50) NOT NULL,
  city varchar(50) NOT NULL,
  state varchar(50) NOT NULL,
  postal_code varchar(15) NOT NULL, 
  PRIMARY KEY (vendor_name)
);

CREATE TABLE `recall` (
  nhtsa_recall_number varchar(50) NOT NULL, 
  manufacturer_name varchar(50) NOT NULL,
  recall_description varchar(200) NOT NULL,
  PRIMARY KEY (nhtsa_recall_number)
);

-- Constraints   Foreign Keys: FK_ChildTable_childColumn_ParentTable_parentColumn
ALTER TABLE `individual`
  ADD CONSTRAINT fk_individual_customer_id_customer_customer_id FOREIGN KEY (customer_id) REFERENCES `customer` (customer_id);
  
ALTER TABLE `business`
  ADD CONSTRAINT fk_business_customer_id_customer_customer_id FOREIGN KEY (customer_id) REFERENCES `customer` (customer_id);

ALTER TABLE `sale`
  ADD CONSTRAINT fk_sale_customer_id_customer_customer_id FOREIGN KEY (customer_id) REFERENCES `customer` (customer_id);
ALTER TABLE `sale`
  ADD CONSTRAINT fk_sale_login_username_user_login_username FOREIGN KEY (login_username) REFERENCES `user` (login_username);
ALTER TABLE `sale`
  ADD CONSTRAINT fk_sale_vin_vehicle_vin FOREIGN KEY (vin) REFERENCES `vehicle` (vin);

ALTER TABLE `purchase`
  ADD CONSTRAINT fk_purchase_customer_id_customer_customer_id FOREIGN KEY (customer_id) REFERENCES `customer` (customer_id);
ALTER TABLE `purchase`
  ADD CONSTRAINT fk_purchase_login_username_user_login_username FOREIGN KEY (login_username) REFERENCES `user` (login_username);
ALTER TABLE `purchase`
  ADD CONSTRAINT fk_purchase_vin_vehicle_vin FOREIGN KEY (vin) REFERENCES `vehicle` (vin);

ALTER TABLE `vehicle_color`
  ADD CONSTRAINT fk_vehicleColor_vin_vehicle_vin FOREIGN KEY (vin) REFERENCES `vehicle` (vin);

ALTER TABLE `repair`
  ADD CONSTRAINT fk_repair_vin_vehicle_vin FOREIGN KEY (vin) REFERENCES `vehicle` (vin);
ALTER TABLE `repair`
  ADD CONSTRAINT fk_repair_vin_vendor_vendor_name FOREIGN KEY (vendor_name) REFERENCES `vendor` (vendor_name);
ALTER TABLE `repair`
  ADD CONSTRAINT fk_repair_nhtsa_recall_number_recall_nhtsa_recall_number FOREIGN KEY (nhtsa_recall_number) REFERENCES `recall` (nhtsa_recall_number);
