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

CREATE TABLE `User` (
  login_username varchar(50) NOT NULL, -- should we limit the size of username and password to a smaller size, say 20 characters?
  login_password varchar(50) NOT NULL, -- should we limit the size of username and password to a smaller size, say 20 characters?
  user_first_name varchar(50) NOT NULL,
  user_last_name varchar(50) NOT NULL,
  role varchar(25) NOT NULL, -- should we limit the size of role to a single character? 
  PRIMARY KEY (login_username)
);

CREATE TABLE `Customer` (
  customer_id int(32) unsigned NOT NULL AUTO_INCREMENT,
  phone_number int(10) unsigned NOT NULL, -- Should be varchar, They advised against phone number being 10 digits it. e.g phone numbers with extension
  email varchar(50) NOT NULL,
  street varchar(50) NOT NULL,
  city varchar(50) NOT NULL,
  state varchar(50) NOT NULL,
  postal_code int(10) NOT NULL, -- should be varchar
  PRIMARY KEY (customer_id),
  UNIQUE KEY (email)
);

CREATE TABLE `Individual` (
  driver_license_number varchar(50) NOT NULL,
  customer_id int(32) unsigned NOT NULL,
  individual_first_name varchar(50) NOT NULL,
  individual_last_name varchar(50) NOT NULL,
  PRIMARY KEY (driver_license_number),
  UNIQUE KEY (customer_id)
);

CREATE TABLE `Business` (
  tax_id_number varchar(50) NOT NULL,
  customer_id int(32) unsigned NOT NULL,
  business_name varchar(50) NOT NULL,
  primary_contact_name varchar(50) NOT NULL,
  primacy_contact_title varchar(50) NOT NULL,
  PRIMARY KEY (tax_id_number),
  UNIQUE KEY (customer_id)
);

CREATE TABLE `Sale` (
  vin varchar(50) NOT NULL,
  customer_id int(32) unsigned NOT NULL,
  login_username varchar(50) NOT NULL,
  sales_date date NOT NULL
  PRIMARY KEY (vin)
);

CREATE TABLE `Purchase` (
  vin varchar(50) NOT NULL,
  customer_id int(32) unsigned NOT NULL,
  login_username varchar(50) NOT NULL,
  purchase_date date NOT NULL,
  PRIMARY KEY (vin)
);

CREATE TABLE `Vehicle` (
  vin varchar(50) NOT NULL,
  manufacturer_name varchar(50) NOT NULL,
  type_name varchar(50) NOT NULL,
  model_year smallint NOT NULL,
  model_name varchar(50) NOT NULL,
  mileage float(8) NOT NULL,
  vehicle_condition varchar(10) NOT NULL,
  description varchar(200) NOT NULL,
  sales_price float(8) NOT NULL,
  kelly_blue_book_value float(8) NOT NULL,
  PRIMARY KEY (vin)
);

CREATE TABLE `Vehicle-Color` (
  vin varchar(50) NOT NULL,
  color varchar(50) NOT NULL,
  PRIMARY KEY (vin) -- Need to check
);

CREATE TABLE `Manufacturer` (
  manufacturer_name varchar(50) NOT NULL,
  PRIMARY KEY (manufacturer_name)
);

CREATE TABLE `VehicleType` (
  type_name varchar(50) NOT NULL,
  PRIMARY KEY (type_name)
);

CREATE TABLE `Repair` (
  vin varchar(50) NOT NULL,
  start_date date NOT NULL,
  end_date date NOT NULL,
  vendor_name varchar(50) NOT NULL,
  nhtsa_number varchar(50) NULL,
  total_cost float(8) NOT NULL,
  repair_description varchar(200) NOT NULL, -- need to check if this can be NULL
  status varchar(1) NOT NULL,
  PRIMARY KEY (vin) -- need to check 
);

CREATE TABLE `Vendor` (
  vendor_name varchar(50) NOT NULL,
  vendor_phone_number varchar(20) NOT NULL,
  street varchar(50) NOT NULL,
  city varchar(50) NOT NULL,
  state varchar(50) NOT NULL,
  postal_code varchar(10) NOT NULL, -- should be varchar
  PRIMARY KEY (vendor_name)
);

CREATE TABLE `Recall` (
  nhtsa_number varchar(50) NOT NULL, --change in relationship mapping 
  manufacturer_name varchar(50) NOT NULL,
  recall_description varchar(200) NOT NULL, --change in relationship mapping 
  PRIMARY KEY (nhtsa_number)
);

