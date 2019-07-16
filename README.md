# CS6400-2019-02-Team13
Repository for CS6400-2019-02-Team13

**Table of Contents**

Public Search and Vehicle Detail View

Public Search

Public Vehicle Detail view

Inventory Clerk: Login, Authenticated Search, Vehicle Detail, Add Vehicle, Search/Add Seller, Repairs, Logout

Login-Inventory Clerk

Authenticated Search

Vehicle Detail

Add Vehicle

Search/Add Customer-Seller

Add Repairs

Search/Add Vendor

Update and Complete Repairs

Logout

Salespeople: Login, Authenticated Search, Vehicle Detail, Sell Vehicle, Search/Add Customer-Seller, Logout

Login-Salespeople

Authenticated Search

Vehicle Detail

Sell Vehicle

Search/Add Customer-Seller

Logout

Managers: Login, Authenticated Search, Vehicle Detail, Reports, Logout

Login-Manager

Authenticated Search

Vehicle Detail

Reports

Logout

Owner: Login, Authenticated Search, Vehicle Detail, Reports, Logout

Login-Owner (All Roles)

Authenticated Search

Vehicle Detail

Reports

Logout

#

Public Search and Vehicle Detail View

Public Search

1. Start on public search
  1. Point out the number of vehicles available for purchase
  2. Search 1 for vehicles (pick any below)
    1. Select Vehicle Type: **Convertible**
    2. Select Manufacture: **Porsche**
    3. Select Model Year: **2007**
    4. Select Color: **Rose**
    5. Search; show results
  3. Search 2, Clear Search
    1. Enter Keyword: **gmc**
    2. Seach; &quot;Sorry, it looks like we don&#39;t have that in stock!&quot;
  4. Search 3, reload page
    1. Enter Keyword: **2013**
    2. Search; show results

Public Vehicle Detail view

1. Select a vehicle from search result
  1. Point out the Vehicle Detail Fields

Inventory Clerk: Login, Authenticated Search, Vehicle Detail, Add Vehicle, Search/Add Seller, Repairs, Logout

Login-Inventory Clerk

1. Start on Public search
2. Login as Clerk
  1. Username: **user02**
  2. Password: **pass02**
  3. Point out the number of vehicles available for purchase
  4. Point out additional count of vehicles with repairs pending or in-progress
  5. Point out new Add Vehicle link
  6. Point out the new search by VIN Field

Authenticated Search

1. Search
  1. Search 1 using same Keyword as Public user
    1. Enter Keyword: **2013**
    2. Search; Point out more returns than public user on same query
  2. Search 2 using VIN
    1. Paste VIN ( **22420XMJ47N471618** ) in VIN field
    2. Search; show results

Vehicle Detail

1. Click link for Vehicle Details
  1. Point out new fields for Inventory Clerk
    1. Original Purchase Price
    2. Total of all repair costs
  2. Point out Manage Repairs Link listing details of all repairs for the vehicle

Add Vehicle

1. Demo Add Vehicle
  1. Return to main page
  2. Click Add Vehicle Link

Search Customer-Seller

1. Demo Search Customer
  1. Click Search Customer
    1. Select Individual
    2. Enter DL: **A2840015188**
    3. Search
    4. Select Customer
  2. Complete Add Vehicle Fields
    1. Enter VIN: **1D377TZAWSW801900**
    2. Enter Purchase Price: **400**
    3. Select Manufacturer: **Audi**
    4. Select Vehicle Type: **Coupe**
    5. Select Model: **X1**
    6. Enter Year: **2001**
    7. Enter Mileage: **100000**
    8. Select Condition: **Excellent**
    9. Enter Description: **DEMO**
    10. Select Color: **Blue**
    11. Click Purchase
    12. Point out $0 for Total Repair Cost, Price is 1.25x Purchase ($500)

Add Repairs

1. Demo Add, Update, Complete Repairs
  1. In Vehicle Details for newly added Vehicle
    1. Again point out $0 for total repairs
    2. Click Vehicle Repairs
    3. Point Out, no current or past repairs

Search/Add Vendor

1. Search Vendor
  1. Click Search For Vendor Name
  2. Enter Vendor Name: **Newex**
  3. Click Search
  4. Click Select Vendor
2. Complete Add Repair Fields
  1. Enter Start Date: **2019-07-12**
  2. Enter End Date: **2019-07-13**
  3. Enter Repair Cost: **1000**
  4. Enter Description: **fix cupholder**
  5. Click Add Repair
  6. Update Repair to In Progress
  7. Update Repair to Complete
3. Add Vendor
  1. Click Search For Vendor Name
  2. Enter Vendor Name: **Bobs Shack**
  3. Enter Phone Number: **905-555-2300**
  4. Enter Street: **123 Main St**
  5. Enter City: **Dallas**
  6. Enter State: **TX**
  7. Enter Postal Code: **75003**
  8. Add Vendor
4. Complete Add Repair Fields
  1. Enter Start Date: **2019-07-14**
  2. Enter End Date: **2019-07-15**
  3. Enter NHTSA Recall Number: **04V133000**
  4. Enter Repair Cost: **100**
  5. Enter Description: **Safety Recall**
  6. Click Add Repair
  7. Update Repair to In Progress
  8. Update Repair to Complete

Update and Complete Repairs

1. Update and Complete Repairs
  1. Complete Repair
  2. Copy VIN
  3. Return to main page
  4. Search by VIN (Paste VIN in Field)
  5. Point out change in price ($1600 now)

Logout

1. Logout
  1. Return to Main pages
  2. Click Logout

Salespeople: Login, Authenticated Search, Vehicle Detail, Sell Vehicle, Search/Add Customer-Seller, Logout

Login-Salespeople

1. Start on Public search
2. Login as Sales Person
  1. Username: **user08**
  2. Password: **pass08**
  3. Point out the number of vehicles available for purchase (increased by 1)
  4. Point out the new search by VIN Field

Authenticated Search

1. Search
  1. Search 1 using Keyword as Public user
    1. Enter Keyword: **2001**
    2. Search; Displays newly purchased vehicle

Vehicle Detail

1. Click link for Vehicle Details
  1. Point out the same columns as Public Search
  2. Point out new Sell Vehicle link

Sell Vehicle

1. Demo Sell Vehicle
  1. Click Sell Vehicle Link

Add Customer-Buyer

1. Demo Search/Add Customer-Buyer
  1. Click Search customer
  2. Enter TIN ID: **08-2477133**
  3. Search Customer
  4. Add Business Customer
  5. Phone number: **972-555-2300**
  6. Email Address: **m@c.com**
  7. Street: **123 Main St**
  8. City: **Plano**
  9. State: **TX**
  10. Postal Code: **75075**
  11. Business Tax ID: **08-2477133**
  12. Business Name: **DEMO**
  13. Primary Contact Name: **Jim Demo**
  14. Primary Contact Title: **Owner/Operator**

** **

1. Complete Sell
  1. Click Sell Vehicle

Logout

1. Demo Logout
  1. Return to Main Page
  2. Click Logout

Managers: Login, Authenticated Search, Vehicle Detail, Reports, Logout

Login-Manager

1. Start on Public search
2. Login as Manager
  1. Username: **user01**
  2. Password: **pass01**
  3. Point out the number of vehicles available for purchase
  4. Point out additional count of vehicles with repairs pending or in-progress
  5. Point out the new Reports link
  6. Point out the new search by VIN Field
  7. Point out the new filter by status (Unsold, Sold, All)

Authenticated Search

1. Search
  1. Search 1 using same Keyword as Public user
    1. Enter Keyword: **2013**
    2. Select All in Filter Sold/Unsold
    3. Enter Keyword again and select Unsold
    4. Enter Keyword again and select Sold
    5. Search

Vehicle Detail

1. Click link for Vehicle Details on Sold
  1. Point out the additional information for manager
    1. Seller&#39;s Contact Information
    2. Inventory Clerk that purchased the vehicle
    3. Purchase info (price, date, total cost of repairs)
    4. Repairs Link listing details for all repairs on the vehicle
    5. Buyer&#39;s contact information
    6. Sale date
    7. Salesperson that sold the vehicle

Reports

1. Return to Main page
  1. Select Dropdown for each report and demo
    1. Seller History Report
      1. Name of Seller
      2. Total vehicles sold to Burdell
      3. Average Purchase Price
      4. Average Number of Repairs
      5. Sorted:
        1. Vehicles Sold Descending
        2. Average Purchase Ascending
      6. Highlighted Average Repair \&gt;=5
    2. Inventory Age Report
      1. Vehicle Type
      2. Min/Avg/Max Age unsold by type
    3. Average Time in Inventory Report
      1. Vehicle Type
      2. Min/Avg/Max in inventory
    4. Price Per Condition Report
      1. Vehicle Type
      2. Average price per condition
    5. Repair Statistics Report
      1. Vendor Name
      2. Number of completed repairs
      3. Total spend
      4. Number of repairs
      5. Average duration of repairs
    6. Monthly Sales Report
      1. Summary page
        1. Total vehicles sold by year and month
        2. All transactions by year and month
      2. Drilldown page
        1. Ranked order of Salesperson performance
        2. Descending vehicle count/total sales

Logout

1. Demo Logout

1.
  1. Return to Main Page
  2. Click Logout

Owner: Login, Authenticated Search, Vehicle Detail, Reports, Logout

Login-Owner (All Roles)

1. Start on Public search
2. Login as Manager
  1. Username: **burdell**
  2. Password: **burdell**
  3. Point out the number of vehicles available for purchase
  4. Point out additional count of vehicles with repairs pending or in-progress
  5. Point out the new links:
    1. Reports
    2. Add Vehicle
  6. Point out the new search by VIN Field
  7. Point out the filter by status (Unsold, Sold, All)

Authenticated Search

1. Search
  1. Search using same Keyword as Public user
    1. Enter Keyword: **2013**
    2. Select All in Filter Sold/Unsold
    3. Search

Vehicle Detail

1. Click link for Vehicle Details for Sold Vehicle
  1. Point out the additional information for Owner
    1. Seller&#39;s Contact Information
    2. Inventory Clerk that purchased the vehicle
    3. Purchase info (price, date, total cost of repairs)
    4. Repairs section listing details for all repairs on the vehicle
    5. Buyer&#39;s contact information
    6. Sale date
    7. Salesperson that sold the vehicle
  2. Point out additional links for Owner
    1. Sell Vehicle
    2. Manage Repairs

Reports

1. Return to Main page
  1. Click Reports Link
  2. Display Dropdown of available reports and select one or more demo
    1. Seller History Report
    2. Inventory Age Report
    3. Average Time in Inventory Report
    4. Price Per Condition Report
    5. Repair Statistics Report
    6. Monthly Sales Report

Logout

1. Demo Logout

1.
  1. Return to Main Page
  2. Click Logout
