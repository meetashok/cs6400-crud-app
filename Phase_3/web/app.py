# import Flask with dependecies
from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from forms import IndividualForm, BusinessForm, RepairForm, VendorForm, CustomerSearchForm, VehicleForm

# import sql templating class
from  sql.sql import QueryDB
sql = QueryDB()

# import misc python modules
import sys
import datetime

# instantiate Flask app
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = 'development key'

# build connection to MySQL
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
    print("sql.check_login_username_and_password,(username, password):",sql.check_login_username_and_password,(username, password),file=sys.stderr)
    cursor.execute(sql.check_login_username_and_password,(username, password))
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
      errors = []

      cursor = mysql.connection.cursor()
      cursor.execute("SELECT manufacturer_name from manufacturer")
      manufacturer_names = [record[0] for record in cursor.fetchall()]
      
      cursor.execute("SELECT vehicle_type from vehicle_type")
      vehicle_types = [record[0] for record in cursor.fetchall()]

      colors = ['Aluminum', 'Beige', 'Black', 'Blue', 'Brown', 'Bronze', 'Claret', 'Copper', 
      'Cream', 'Gold', 'Gray', 'Green', 'Maroon', 'Metallic', 'Navy', 'Orange', 'Pink', 
      'Purple', 'Red', 'Rose', 'Rust', 'Silver', 'Tan', 'Turquoise', 'White', 'Yellow']

      vehicle_conditions = ["Excellent", "Very Good", "Good", "Fair"]
      
      current_year = datetime.datetime.now().year

      if request.method == "GET":
          return render_template("purchasevehicle.html", manufacturer_names=manufacturer_names,
          vehicle_types=vehicle_types, colors=colors, vehicle_conditions=vehicle_conditions, errors=errors)
      if request.method == "POST":
          vin = request.form.get("vin")
          manufacturer_name = request.form.get("manufacturer_name")
          vehicle_type = request.form.get("vehicle_type")
          model_year = request.form.get("model_year")
          model_name = request.form.get("model_name")
          mileage = request.form.get("mileage")
          vehicle_condition = request.form.get("vehicle_condition")
          vehicle_description = request.form.get("vehicle_description")
          kbb_value = request.form.get("kbb_value")
          colors = request.form.getlist("colors")

          return "Done"
      

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
    cursor.execute(sql.reports_seller_history)
    data = cursor.fetchall()
    return render_template("display_seller_history_table.html", data=data)

@app.route('/report/inventoryage', methods=['GET'])
def get_InventoryAge():
    cursor = mysql.connection.cursor()
    cursor.execute(sql.reports_inventoryage)
    data = cursor.fetchall()
    return render_template("display_inventory_age_table.html", data=data)

@app.route('/report/averagetimeininventory', methods=['GET'])
def get_AvgTimeInInventory():
    cursor = mysql.connection.cursor()
    cursor.execute(sql.reports_average_time_in_inventory)
    data = cursor.fetchall()
    return render_template("display_avg_time_in_inventory_table.html", data=data)


@app.route('/report/priceperrepair', methods=['GET'])
def get_PricePerRepair():
    cursor = mysql.connection.cursor()
    cursor.execute(sql.reports_price_per_repair)
    data = cursor.fetchall()
    return render_template("display_price_per_repair_table.html", data=data)



@app.route('/report/repairstatistics', methods=['GET'])
def get_RepairStats():
    cursor = mysql.connection.cursor()
    cursor.execute(sql.reports_repair_statistics)
    data = cursor.fetchall()
    return render_template("display_repair_stats_table.html", data=data)



@app.route('/report/monthlysales', methods=['GET'])
def get_MonthlySales():
    cursor = mysql.connection.cursor()
    print("sql.reports_monthly_sales:",sql.reports_monthly_sales,file=sys.stderr)
    cursor.execute(sql.reports_monthly_sales)
    data = cursor.fetchall()
    return render_template("display_monthly_sales_table.html", data=data)



@app.route('/report/monthlysalesdrilldown/yearmonth=<string:yearmonth>', methods=['GET'])
def get_MonthlySalesDrilldown(yearmonth=None):
    cursor = mysql.connection.cursor()
    cursor.execute(sql.reports_monthly_sales_drilldown(yearmonth))
    data = cursor.fetchall()
    return render_template("display_monthly_sales_drilldown_table.html", data=data)

if __name__ == "__main__":
  app.run(debug=True)
