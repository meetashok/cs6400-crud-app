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
  login_username varchar(50) NOT NULL,
  login_password varchar(50) NOT NULL,
  user_first_name varchar(50) NOT NULL,
  user_last_name varchar(50) NOT NULL,
  role varchar(25) NOT NULL,
  PRIMARY KEY (login_username)
);

CREATE TABLE `Customer` (
  customer_id int(32) unsigned NOT NULL AUTO_INCREMENT,
  phone_number int(10) unsigned NOT NULL,
  email varchar(50) NOT NULL,
  street varchar(50) NOT NULL,
  city varchar(50) NOT NULL,
  state varchar(50) NOT NULL,
  postal_code int(10) NOT NULL,
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

-- TODO left off with Vehicle
CREATE TABLE `Vehicle` (
  vin varchar(50) NOT NULL,
  manufacturer_name
  type_name
  model_year
  model_name
  mileage
  vehicle_condition
  description
  sales_price
  kelly_blue_book_value
  PRIMARY KEY (vin)
);
