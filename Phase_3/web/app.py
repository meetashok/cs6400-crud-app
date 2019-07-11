# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from forms import IndividualForm, BusinessForm, RepairForm, VendorForm, CustomerSearchForm, VehicleForm

import sys

# import sql templating class
from  sql.sql import QueryDB
sql = QueryDB()

# create the application object
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = 'development key'

# create the connection to MySQL
mysql = MySQL(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'abcd_123'
app.config['MYSQL_DB'] = 'cs6400_sm19_team013'
app.config['MYSQL_PORT'] = 3306

# setup session dictionary for user authentication
session = {
  "authenticated":False,
  "username":"guest",
  "role": None
}

# main page with vehicle count, login, and search
@app.route('/', methods=['GET', 'POST'])
def main():
  print("session:",session,file=sys.stderr)
  cursor = mysql.connection.cursor()
  # count of vehicles for sale
  cursor.execute(sql.count_vehicles_available)
  count_vehicles_available = cursor.fetchone()
  print("count_vehicles_available:",count_vehicles_available, file=sys.stderr)
  if count_vehicles_available:
    count_vehicles_available = count_vehicles_available[0]
  return render_template('main.html', count_vehicles_available=count_vehicles_available, session=session)  # render main template

# login handler
@app.route('/login', methods=['POST'])
def login():
  # Output message if something goes wrong...
  msg = ''
  # Check if "username" and "password" POST requests exist (user submitted form)
  if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    # Create variables for easy access
    username = request.form['username']
    password = request.form['password']
    # Check if account exists using MySQL
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT login_username, login_password, role FROM user WHERE login_username = %s AND login_password = %s', (username, password))
    # cursor.execute(sql.check_login_username_and_password(username, password))
    # Fetch one record and return result
    user = cursor.fetchone()
    print("user:",user, file=sys.stderr)
    if user:
      print("login_username:",user[0], file=sys.stderr)
      print("login_password:",user[1], file=sys.stderr)
      print("role:",user[2], file=sys.stderr)
    # If account exists in accounts table in out database
    if user and user[1] == password:
      # Create session data, we can access this data in other routes
      session["authenticated"] = True
      session["username"] = user[0]
      session["role"] = user[2] 
      msg = 'Logged in successfully!'
    else:
      # Account doesnt exist or username/password incorrect
      msg = 'Incorrect username/password!'
  # Show the login form with message (if any)
  return redirect(url_for('main'))  

# logout handler
@app.route('/logout', methods=['POST'])
def logout():
  # remove session data, this will log the user out
  session["authenticated"] = False
  session["username"] = "guest"
  session["role"] = None
  return redirect(url_for('main'))  

### ##########Search form section
### def search():
###     form = SearchForm()
###     if request.method == "GET":
###         return render_template('main.html', form=form)
### 
###     if request.method == "POST":
###         if form.validate() == True:
###             vehicle_type = form.vehicle_type.data
###             manufacturer_name = form.manufacturer_name.data
###             color = form.color.data
###             model_year = form.model_year.data
###             keyword = form.keyword.data
### 
###             
###             cursor = mysql.connection.cursor()
###             query2 = "SELECT * FROM vehicle"
###             #variables = vehicle_type, manufacturer_name, color, model_year, keyword
###             cursor.execute((query, variables))
###             mysql.connection.commit()
###             # return render_template('welcome.html', query="query")
###             return redirect(url_for("main"))
### 
###         else:
###             return render_template('main.html', form=form)

@app.route('/repairs/vin=<string:vin>', methods=["GET", "POST"]) # http://localhost:5000/repairs/some_vin
# @login_required
def repairs(vin="BLANK"):
    form = RepairForm()
    if request.method == "GET":
      cursor = mysql.connection.cursor()
      cursor.execute("SELECT * FROM repair WHERE vin = %s", [vin])
      repair_data = cursor.fetchall()
      mysql.connection.commit()
      return render_template("repairs.html", vin=vin, repair_data=repair_data, form=form)
     
    if request.method == "POST":
      if form.validate() == True:
        cursor = mysql.connection.cursor()
        repair_status = "Pending"
        query = "INSERT INTO repair VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        nhtsa_recall_number = form.nhtsa_recall_number.data
        if form.nhtsa_recall_number.data == "":
          nhtsa_recall_number = None
        parameters = [vin, str(form.repair_start_date.data), str(form.repair_end_date.data), form.vendor_name.data, nhtsa_recall_number, form.total_cost.data, form.repair_description.data, repair_status]
        print((query,parameters), file=sys.stderr)
        cursor.execute(query, parameters)
        mysql.connection.commit()
        return redirect(url_for("repairs", vin=vin))
      else:
        return render_template("repairs.html", vin=vin, repair_data=repair_data, form=form)

@app.route("/addindividual", methods=['GET', 'POST'])
def addindividual(previous_page=None):
    form = IndividualForm()
    if request.method == "GET":
        return render_template('addindividual.html', form=form)
    if request.method == "POST":
        if form.validate() == True:
            cursor = mysql.connection.cursor()
            query = "INSERT INTO customer (customer_id, phone_number, email, street, city, state, postal_code) VALUES (NULL, %s, %s, %s, %s, %s, %s)"
            variables = [form.phone_number.data, form.email.data, form.street.data, form.city.data, form.state.data, form.postal_code.data]
            cursor.execute(query, variables)
            mysql.connection.commit()
            
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT LAST_INSERT_ID()")
            last_customer_id = cursor.fetchall()
            query = "INSERT INTO individual (driver_license_number, customer_id, individual_first_name, individual_last_name) VALUES (%s, %s, %s, %s)"
            variables = [form.driver_license_number.data, last_customer_id, form.individual_first_name.data, form.individual_last_name.data]
            cursor.execute(query, variables)
            mysql.connection.commit()
            return redirect(url_for("main"))
        else:
            return render_template('addindividual.html', form=form)

@app.route("/addbusiness", methods=['GET', 'POST'])
def addbusiness():
    form = BusinessForm()
    if request.method == "GET":
        return render_template('addbusiness.html', form=form)
    if request.method == "POST":
        if form.validate() == True:
            cursor = mysql.connection.cursor()
            query = "INSERT INTO customer (customer_id, phone_number, email, street, city, state, postal_code) VALUES (NULL, %s, %s, %s, %s, %s, %s)"
            variables = [form.phone_number.data, form.email.data, form.street.data, form.city.data, form.state.data, form.postal_code.data]
            cursor.execute(query, variables)
            mysql.connection.commit()
            
            cursor = mysql.connection.cursor()
            # cursor.execute("SELECT max(customer_id) from customer")
            cursor.execute("SELECT LAST_INSERT_ID()")
            last_customer_id = cursor.fetchall()
            query = "INSERT INTO business (tax_id_number, customer_id, business_name, pc_name, pc_title) VALUES (%s, %s, %s, %s, %s)"
            variables = [form.tax_id_number.data, last_customer_id, form.business_name.data, form.pc_name.data, form.pc_title.data]
            cursor.execute(query, variables)
            mysql.connection.commit()
            # return render_template('welcome.html', query="query")
            return redirect(url_for("main"))
        else:
            return render_template('addbusiness.html', form=form)

@app.route("/addvendor", methods=['GET', 'POST'])
def addvendor():
    form = VendorForm()
    if request.method == "GET":
        return render_template('addvendor.html', form=form)
    if request.method == "POST":
        if form.validate() == True:
            cursor = mysql.connection.cursor()
            query = "INSERT INTO vendor (vendor_name, vendor_phone_number, street, city, state, postal_code) VALUES (%s, %s, %s, %s, %s, %s)"
            variables = [form.vendor_name.data, form.vendor_phone_number.data, form.street.data, form.city.data, form.state.data, form.postal_code.data]
            cursor.execute(query, variables)
            mysql.connection.commit()
            return redirect(url_for("main"))
        else:
            return render_template('addvendor.html', form=form)

@app.route("/purchasevehicle", methods=["GET", "POST"])
def purchasevehicle():
      cursor = mysql.connection.cursor()
      form = VehicleForm()
      form.manufacturer_name.choices = ["bmw", "honda"]
      form.vehicle_type.choices = ["suv", "sedan"]
      form.model_year.choices = [1900, 1901]
      if request.method == "GET":
            render_template("purchasevehicle.html", form=form)
      if request.method == "POST":
            if form.validate() == True:
                  cursor = mysql.connection.cursor()
                  query = "INSERT INTO vehicle (vin, manufacturer_name, vehicle_type, model_year, model_name, mileage, vehicle_condition, vehicle_description, sales_price, kbb_value) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
                  sales_price = float(form.kbb_value.data) * 1.25
                  parameters = [form.vin.data, form.manufacturer_name.data, form.vehicle_type.data, form.model_year.data, 
                  form.model_name.data, form.vehicle_condition.data, form.vehicle_description.data, sales_price, form.kbb_value.data]
                  cursor.execute(query, parameters)
                  mysql.connection.commit()
      

@app.route("/searchcustomer", methods=["GET", "POST"])
def searchcustomer():
    form = CustomerSearchForm()
    return render_template('searchcustomer.html', form=form)
  # if request.method = "POST":
  #       if form.validate() == True:
  #             cursor = mysql.connection.cursor()
  #             cursor.execute("SELECT customer_id ")

@app.route('/dropdown', methods=['GET', 'POST'])
def dropdown():
    colours = ['Red', 'Blue', 'Black', 'Orange']
    form = CustomerID()
    if form.validate_on_submit():
        return render_template('test.html', colours=colours)

@app.route('/report/sellerhistory', methods=['GET'])
def get_SellerHistory():
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT 
  customer_name,
  COUNT(*) AS vehicles_sold,
  ROUND(AVG(purchase_price),2) AS avg_purchase_price,
  COALESCE(ROUND(AVG(number_of_repairs),2),0) AS avg_number_of_repairs
FROM
(SELECT
  customer.customer_id,
  CONCAT(individual.individual_first_name," ",individual.individual_last_name) AS customer_name,
  vehicle.vin,
  a.number_of_repairs,
  vehicle.kbb_value AS purchase_price
FROM vehicle
LEFT JOIN purchase
ON vehicle.vin=purchase.vin
LEFT JOIN customer
ON purchase.customer_id=customer.customer_id
LEFT JOIN individual
ON customer.customer_id=individual.customer_id
LEFT JOIN 
(SELECT 
  vin,
  COUNT(1) AS number_of_repairs
FROM repair
GROUP BY vin) a
ON vehicle.vin=a.vin
WHERE 
  individual.individual_first_name IS NOT NULL
  
UNION ALL

SELECT 
  customer.customer_id,
  business.business_name AS customer_name,
  vehicle.vin,
  a.number_of_repairs,
  vehicle.kbb_value AS purchase_price
FROM vehicle
LEFT JOIN purchase
ON vehicle.vin=purchase.vin
LEFT JOIN customer
ON purchase.customer_id=customer.customer_id
LEFT JOIN business
ON customer.customer_id=business.customer_id
LEFT JOIN 
(SELECT 
  vin,
  COUNT(1) AS number_of_repairs
FROM repair
GROUP BY vin) a
ON vehicle.vin=a.vin
WHERE 
  business.business_name IS NOT NULL) b
GROUP BY customer_id, customer_name
ORDER BY
  vehicles_sold DESC,
  avg_purchase_price ASC;
  """)
    data = cursor.fetchall()
    return render_template("display_seller_history_table.html", data=data)

@app.route('/report/inventoryage', methods=['GET'])
def get_InventoryAge():
  cursor = mysql.connection.cursor()
  cursor.execute("""SELECT
  vehicle_type.vehicle_type,
  COALESCE(a.min_age, 'N/A') AS min_age,
  COALESCE(a.avg_age, 'N/A') AS avg_age,
  COALESCE(a.max_age, 'N/A') AS max_age
FROM vehicle_type
LEFT JOIN 
(SELECT
  vehicle_type, 
  MIN(DATEDIFF(CURRENT_TIMESTAMP, purchase.purchase_date)) AS min_age, 
  AVG(DATEDIFF(CURRENT_TIMESTAMP, purchase.purchase_date)) AS avg_age,
  MAX(DATEDIFF(CURRENT_TIMESTAMP, purchase.purchase_date)) AS max_age
FROM vehicle 
LEFT JOIN purchase
ON vehicle.vin=purchase.vin
LEFT JOIN sale
ON vehicle.vin=sale.vin
WHERE 
  sale.sales_date IS NULL
GROUP BY vehicle_type) AS a
on vehicle_type.vehicle_type=a.vehicle_type;
  """)
  data = cursor.fetchall()
  return render_template("display_inventory_age_table.html", data=data)


@app.route('/report/averagetimeininventory', methods=['GET'])
def get_AvgTimeInInventory():
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT
  vehicle_type.vehicle_type,
  COALESCE(a.min_age, 'N/A') AS min_age,
  COALESCE(a.avg_age, 'N/A') AS avg_age,
  COALESCE(a.max_age, 'N/A') AS max_age
FROM vehicle_type 
LEFT JOIN 
(SELECT
  vehicle_type, 
  MIN(DATEDIFF(sales_date, purchase_date)) AS min_age, 
  AVG(DATEDIFF(sales_date, purchase_date)) AS avg_age,
  MAX(DATEDIFF(sales_date, purchase_date)) AS max_age
FROM vehicle 
LEFT JOIN purchase
ON vehicle.vin=purchase.vin
LEFT JOIN sale
ON vehicle.vin=sale.vin
WHERE 
  sales_date IS NOT NULL -- only for sold vehicles
GROUP BY vehicle_type) AS a
ON a.vehicle_type=vehicle_type.vehicle_type;
    """)
    data = cursor.fetchall()
    return render_template("display_avg_time_in_inventory_table.html", data=data)



@app.route('/report/priceperrepair', methods=['GET'])
def get_PricePerRepair():
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT
  vehicle_type,
  AVG(CASE WHEN vehicle_condition='Excellent' THEN kbb_value ELSE 0 END) AS 'Condition=Excellent',
  AVG(CASE WHEN vehicle_condition='Very Good' THEN kbb_value ELSE 0 END) AS 'Condition=Very Good',
  AVG(CASE WHEN vehicle_condition='Good' THEN kbb_value ELSE 0 END) AS 'Condition=Good',
  AVG(CASE WHEN vehicle_condition='Fair' THEN kbb_value ELSE 0 END) AS 'Condition=Fair'
FROM vehicle
GROUP BY vehicle_type;
    """)
    data = cursor.fetchall()
    return render_template("display_price_per_repair_table.html", data=data)



@app.route('/report/repairstatistics', methods=['GET'])
def get_RepairStats():
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT
  vendor_name,
  COUNT(*) AS number_of_repairs, 
  SUM(total_cost) AS total_spend,
  COUNT(distinct vin) AS number_of_vehicles,
  AVG(DATEDIFF(repair_end_date, repair_start_date)) AS avg_duration
FROM repair
WHERE
  repair_status='Complete'
GROUP BY vendor_name;
    """)
    data = cursor.fetchall()
    return render_template("display_repair_stats_table.html", data=data)



@app.route('/report//monthlysales', methods=['GET'])
def get_MonthlySales():
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT 
  DATE_FORMAT(sales_date, '%Y-%m') as ym,
  COUNT(1) AS number_of_vehicles,
  SUM(sales_price) AS sales_revenue,
  SUM(sales_price - repair_cost - kbb_value) AS net_income
FROM
(SELECT 
 vehicle.vin,
 sale.sales_date,
 vehicle.sales_price,
 vehicle.kbb_value,
 repair_total_cost_by_vin.total_cost AS repair_cost 
FROM vehicle
LEFT JOIN sale
ON vehicle.vin=sale.vin
LEFT JOIN (
SELECT
  repair.vin,
  SUM(repair.total_cost) AS total_cost
FROM repair
GROUP BY vin
) as repair_total_cost_by_vin
ON repair_total_cost_by_vin.vin=vehicle.vin
WHERE 
  sale.sales_date IS NOT NULL) as a  -- vehicle must be sold
GROUP BY ym
order by ym DESC;
    """)
    data = cursor.fetchall()
    cursor2 = mysql.connection.cursor()
    cursor2 = execute("""SELECT
  user.user_first_name,
  user.user_last_name,
  COUNT(1) AS number_of_vehicles,
  SUM(vehicle.sales_price) AS total_sales
FROM vehicle
LEFT JOIN sale
ON vehicle.vin=sale.vin
LEFT JOIN user
ON sale.login_username=user.login_username
WHERE
  DATE_FORMAT(sales_date, '%Y-%m')='2019-06'
GROUP BY 
 user.login_username
ORDER BY
 number_of_vehicles DESC,
 total_sales DESC;
    """)
    return render_template("display_monthly_sales_table.html", data=data, data_drilldown = data_drilldown)



if __name__ == "__main__":
    app.run(debug=True)
