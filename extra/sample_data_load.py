#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import MySQLdb
import datetime

def insert_user(users, mydb):
    cursor = mydb.cursor()
    for i, row in enumerate(users.iterrows()):
        username = row[1]["Username"]
        password = row[1]["Password"]
        user_first_name = row[1]["First Name"]
        user_last_name = row[1]["Last Name"]
        role = row[1]["Role"]
        
        query = "INSERT INTO USER VALUES (%s, %s, %s, %s, %s)"
        values = [username, password, user_first_name, user_last_name, role]
        
        cursor.execute(query, values)
    mydb.commit()
    cursor.close()
    print("Loaded user")

def insert_customer(transactions, mydb):
    customer_cols = ["Customer Email", 
                     "Customer Phone", 
                     "Customer Street Address", 
                     "Customer City", 
                     "Customer State", 
                     "Customer ZIP", 
                     "Persons Driver License",
                     "Persons First Name", 
                     "Persons Last Name", 
                     "Tax Number", 
                     "Business Name",
                     "Contact First Name", 
                     "Contact Last Name", 
                     "Contact Title"]
    
    customers = transactions[customer_cols].drop_duplicates()
    
    cursor = mydb.cursor()
    for i, record in enumerate(customers.iterrows()):
        row = record[1]
        phone = str(row["Customer Phone"])
        email = row["Customer Email"]
        if pd.isna(email):
            email = None
        street = row["Customer Street Address"]
        city = row["Customer City"]
        state = row["Customer State"]
        postal_code = str(row["Customer ZIP"])
        
        license = row["Persons Driver License"]
        first_name = row["Persons First Name"]
        last_name = row["Persons Last Name"]
        
        tin = row["Tax Number"]
        business_name = row["Business Name"]
        pc_name = "{} {}".format(row["Contact First Name"], row["Contact Last Name"])
        pc_title = row["Contact Title"]
        
        customer_query = "INSERT INTO customer VALUES (%s, %s, %s, %s, %s, %s, %s)"
        customer_values = [None, phone, email, street, city, state, postal_code]

        cursor.execute(customer_query, customer_values)
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_insert_id = cursor.fetchall()[0]
        
        individual_query = "INSERT INTO individual VALUES (%s, %s, %s, %s)"
        individual_values = [license, last_insert_id, first_name, last_name]
        
        business_query = "INSERT INTO business VALUES (%s, %s, %s, %s, %s)"
        business_values = [tin, last_insert_id, business_name, pc_name, pc_title]

        if isinstance(business_name, str):
            cursor.execute(business_query, business_values)
            
        else:
            cursor.execute(individual_query, individual_values)
        mydb.commit()
    cursor.close()
    print("Loaded customer")
    print("Loaded individual")
    print("Loaded business")
    
def insert_vehicle(transactions, mydb):
    vehicle_cols = ["Purchase Price", 
                "VIN",
                "Model",
               "Year",
               "Odometer",
               "Colors",
               "Vehicle Description",
               "Manufacturer",
               "Condition",
               "Type",
               "Colors"]
    vehicles = transactions[transactions["Purchase Price"] > 0][vehicle_cols].drop_duplicates()
    cursor = mydb.cursor()
    
    for i, record in enumerate(vehicles.iterrows()):
        row = record[1]
        
        vin = row["VIN"]
        manufacturer = row["Manufacturer"]
        vtype = row["Type"]
        modelyear = row["Year"]
        modelname = row["Model"]
        mileage = row["Odometer"]
        
        condition = row["Condition"]
        description = row["Vehicle Description"] 
        if pd.isna(description):
            description = None
        
        kbb_value = row["Purchase Price"]
        sales_price = kbb_value * 1.25
        
        vehicle_query = "INSERT INTO vehicle VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        vehicle_values = [vin, manufacturer, vtype, modelyear, modelname, 
                          mileage, condition, description, sales_price, kbb_value]
        cursor.execute(vehicle_query, vehicle_values)
        
    mydb.commit()
    cursor.close()
    print("Loaded vehicle")

def insert_manufacturer(mydb):    
    s = '''Acura Alfa Romeo Aston Martin Audi
    Bentley BMW Buick Cadillac
    Chevrolet Chrysler Dodge Ferrari
    FIAT Ford Freightliner Genesis
    GMC Honda Hyundai INFINITI
    Jaguar Jeep Kia Lamborghini
    Land Rover Lexus Lincoln Lotus
    Maserati MAZDA McLaren Mercedes-Benz
    MINI Mitsubishi Nissan Porsche
    Ram Rolls-Royce smart Subaru
    Tesla Toyota Volkswagen Volvo'''
    
    manufacturers = s.split()
    
    cursor = mydb.cursor()
    for manufacturer in manufacturers:
        query = "INSERT INTO manufacturer VALUES (%s)"
        values = [manufacturer]
        
        cursor.execute(query, values)
    mydb.commit()
    cursor.close()
    print("Loaded manufacturer")

def insert_vehicle_type(mydb):
    s = '''Sedan
    Coupe
    Convertible
    Truck
    Van
    Minivan
    SUV
    Other'''
    
    types = s.split()
    
    cursor = mydb.cursor()
    for vehicle_type in types:
        query = "INSERT INTO vehicle_type VALUES (%s)"
        values = [vehicle_type]
        
        cursor.execute(query, values)
    mydb.commit()
    cursor.close()        
    print("Loaded vehicle_type")

def insert_recall(repairs, mydb):
    recall_cols = ["Recall NTHSA",
              "Recall Description",
              "Manufacturer"]
    recalls = repairs[recall_cols].dropna().drop_duplicates()
    cursor = mydb.cursor()
    
    for i, record in enumerate(recalls.iterrows()):
        row = record[1]
        
        recall_number = row["Recall NTHSA"]
        description = row["Recall Description"]
        manufacturer = row["Manufacturer"]

        recall_query = "INSERT INTO recall VALUES (%s, %s, %s)"
        recall_values = [recall_number, manufacturer, description]
        cursor.execute(recall_query, recall_values)
        
    mydb.commit()
    cursor.close()    
    print("Loaded recall")

def insert_vehicle_color(transactions, mydb):
    color_cols = ["VIN", "Colors"]
    colors = transactions[transactions["Purchase Price"] > 0][color_cols].drop_duplicates()
    cursor = mydb.cursor()
    
    for i, record in enumerate(colors.iterrows()):
        row = record[1]
        
        vin = row["VIN"]
        colors = row["Colors"].split(";")
        for color in colors:
            color_query = "INSERT INTO vehicle_color VALUES (%s, %s)"
            color_values = [vin, color]
            cursor.execute(color_query, color_values)
        
    mydb.commit()
    cursor.close()    
    print("Loaded vehicle_color")    

def insert_vendor(repairs, mydb):
    vendor_cols = ["Vendor Name",
              "Vendor Phone",
              "Vendor Street Address",
              "Vendor City",
              "Vendor State",
              "Vendor ZIP"]
    vendors = repairs[vendor_cols].drop_duplicates()
    cursor = mydb.cursor()
    
    for i, record in enumerate(vendors.iterrows()):
        row = record[1]
        
        name = row["Vendor Name"]
        phone = str(row["Vendor Phone"])

        street = row["Vendor Street Address"]
        city = row["Vendor City"]
        state = row["Vendor State"]
        postal_code = str(row["Vendor ZIP"])

        vendor_query = "INSERT INTO vendor VALUES (%s, %s, %s, %s, %s, %s)"
        vendor_values = [name, phone, street, city, state, postal_code]

        cursor.execute(vendor_query, vendor_values)
        
    mydb.commit()
    cursor.close()    
    print("Loaded vendor")

def insert_repair(repairs, mydb):
    repair_cols = [
        "Start Date",
        "End Date",
        "VIN",
        "Repair Description",
        "Repair Cost",
        "Repair Status",
        "Vendor Name",
        "Recall NTHSA",
        "Repair Cost"
    ]
    repairs = repairs[repair_cols].drop_duplicates()
    cursor = mydb.cursor()
    
    for i, record in enumerate(repairs.iterrows()):
        row = record[1]
        vin = row["VIN"]
        start_date = str(datetime.datetime.strptime(row["Start Date"], "%m/%d/%y").date())
        end_date = str(datetime.datetime.strptime(row["End Date"], "%m/%d/%y").date())
        vendor = row["Vendor Name"]
        

        recall_number = row["Recall NTHSA"]
        if pd.isna(recall_number):
            recall_number = None
        cost = row["Repair Cost"][0]
        description = row["Repair Description"]
        status = str(row["Repair Status"])

        repair_query = "INSERT INTO repair VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        repair_values = [vin, start_date, end_date, vendor, recall_number, cost, description, status]

        cursor.execute(repair_query, repair_values)
        
    mydb.commit()
    cursor.close()    
    print("Loaded repair")

def insert_purchase(transactions, mydb):
    purchase_cols = [
        "VIN",
        "Persons Driver License",
        "Tax Number",
        "Username",
        "Date"
    ]
    purchases = transactions[transactions["PurchaseSell"] == "Purchase"]
    cursor = mydb.cursor()
    
    for i, record in enumerate(purchases.iterrows()):
        row = record[1]
        vin = row["VIN"]
        date = str(datetime.datetime.strptime(row["Date"], "%m/%d/%y").date())
        license = row["Persons Driver License"]
        tax_number = row["Tax Number"]
        user = row["Username"]
        
        if pd.isna(license):
            cursor.execute("SELECT customer_id from business WHERE tax_id_number = %s", [tax_number])
        else:
            cursor.execute("SELECT customer_id from individual WHERE driver_license_number = %s", [license])
        customer_id = cursor.fetchall()

        purchase_query = "INSERT INTO purchase VALUES (%s, %s, %s, %s)"
        purchase_values = [vin, customer_id, user, date]
        cursor.execute(purchase_query, purchase_values)
        
    mydb.commit()
    cursor.close()
    print("Loaded purchase")    
    
def insert_sale(transactions, mydb):
    purchase_cols = [
        "VIN",
        "Persons Driver License",
        "Tax Number",
        "Username",
        "Date"
    ]
    sales = transactions[transactions["PurchaseSell"] == "Sale"]
    cursor = mydb.cursor()
    
    for i, record in enumerate(sales.iterrows()):
        row = record[1]
        vin = row["VIN"]
        date = str(datetime.datetime.strptime(row["Date"], "%m/%d/%y").date())
        license = row["Persons Driver License"]
        tax_number = row["Tax Number"]
        user = row["Username"]
        
        if pd.isna(license):
            cursor.execute("SELECT customer_id from business WHERE tax_id_number = %s", [tax_number])
        else:
            cursor.execute("SELECT customer_id from individual WHERE driver_license_number = %s", [license])
        customer_id = cursor.fetchall()

        sale_query = "INSERT INTO sale VALUES (%s, %s, %s, %s)"
        sale_values = [vin, customer_id, user, date]
        cursor.execute(sale_query, sale_values)
        
    mydb.commit()
    cursor.close()    
    print("Loaded sale")

if __name__ == "__main__":
    host = "localhost"
    user = "root"
    passwd = "abcd_123"
    db = "cs6400_sm19_team013"

    mydb = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)

    repairs = pd.read_csv("sample_data/repairs.csv")
    transactions = pd.read_csv("sample_data/transactions.csv")
    users = pd.read_csv("sample_data/users.csv")

    insert_user(users, mydb)
    insert_customer(transactions, mydb)
    insert_manufacturer(mydb)
    insert_vehicle_type(mydb)
    insert_vehicle(transactions, mydb)
    insert_vehicle_color(transactions, mydb)
    insert_vendor(repairs, mydb)
    insert_recall(repairs, mydb)
    insert_repair(repairs, mydb)
    insert_purchase(transactions, mydb)
    insert_sale(transactions, mydb)