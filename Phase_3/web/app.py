# import Flask with dependecies
from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from forms import IndividualForm, BusinessForm, RepairForm, VendorForm, CustomerSearchForm, VehicleForm, ManufacturerForm, VehicleTypeForm, VendorSearchForm

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

# setup session dictionary for user authentication and other session related variables
session = {
  "authenticated":False,
  "failed_authentication":False,
  "username":None,
  "role": None,
  "previous_page": None,
  "vin":None,
  "customer": {},
  "search_result":[]
}

# main page with vehicle count
@app.route('/', methods=['GET', 'POST'])
def main():
  cursor = mysql.connection.cursor()
   
  # count of vehicles for sale
  cursor.execute(sql.count_vehicles_available)
  tmp = cursor.fetchone()
  count_vehicles_available = tmp[0] if tmp else None
  print("count_vehicles_available:",count_vehicles_available, file=sys.stderr)
   
  # pull vehicletypes for (public) dropdown
  cursor.execute(sql.get_vehicle_types)
  vehicle_types = cursor.fetchall()
  print("vehicle_types:",vehicle_types, file=sys.stderr)
   
  # pull manufacturers for (public) dropdown
  cursor.execute(sql.get_manufacturers)
  manufacturers = cursor.fetchall()
  print("manufacturers:",manufacturers, file=sys.stderr)
   
  # define static list of vehicle colors (static list provided in specification document)
  colors = [
    "Aluminum","Black","Blue","Brown","Bronze","Claret",
    "Copper","Cream","Gold","Gray","Green","Maroon","Metallic",
    "Navy","Orange","Pink","Purple","Red","Rose","Rust",
    "Silver","Tan","Turquoise","White","Yellow"
  ]
  # define static list of modelyears from range 1900 to current year + 1
  modelyears = sorted(list(range(1900, int(datetime.datetime.now().year)+1)), reverse=True) #Should this be +2?
   
  session["previous_page"] = "main"
  return render_template(
    'main.html',
    count_vehicles_available=count_vehicles_available,
    vehicle_types=vehicle_types,
    manufacturers=manufacturers,
    colors=colors,
    modelyears=modelyears,
    session=session
  )
   
# login handler
@app.route('/login', methods=['POST'])
def login():
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
      session["failed_authentication"] = False
      session["username"] = user[0]
      session["role"] = user[2] 
    else:
      # Account doesnt exist or username/password incorrect
      session["authenticated"] = False
      session["failed_authentication"] = True
  return redirect(url_for(session["previous_page"]))

# logout handler
@app.route('/logout', methods=['POST'])
def logout():
  # remove session data, this will log the user out
  session["authenticated"] = False
  session["failed_authentication"] = False
  session["username"] = None
  session["role"] = None
  return redirect(url_for("main"))

# vehicle search
@app.route('/search', methods=["GET","POST"])
def search():
  if request.method == "GET":
    return render_template('main.html')
   
  if request.method == "POST":
    vehicle_type = request.form['vehicle_type']
    manufacturer = request.form['manufacturer']
    model_year = request.form['model_year']
    color = request.form['color']
    keyword = request.form['keyword']
     
    cursor = mysql.connection.cursor()
    query_vars = [vehicle_type, manufacturer, color, model_year, keyword] 
    print("sql.vehicle_search:",sql.vehicle_search,file=sys.stderr)
    print("query_vars:",query_vars,file=sys.stderr)
    # cursor.execute(sql.vehicle_search, query_vars)
    cursor.execute(sql.vehicle_search,[vehicle_type])
    search_result = cursor.fetchall()
    session["search_result"] = search_result 
    return redirect(url_for("main"))

@app.route('/repairs', methods=["GET", "POST"])
@app.route('/repairs/vin=<string:vin>', methods=["GET", "POST"]) # http://localhost:5000/repairs/some_vin
# @login_required
def repairs(vin=None):
  if vin != None:
    session["vin"] = vin
  if session["vin"]:
    vin = session["vin"]
  form = RepairForm()
  # show repairs info for vin
  session["previous_page"] = "repairs"
  if request.method == "GET":
    cursor = mysql.connection.cursor()
    cursor.execute(sql.repairs_show_repairs, [vin])
    repair_data = cursor.fetchall()
    mysql.connection.commit()
    return render_template("repairs.html", vin=vin, repair_data=repair_data, form=form, session=session)
   
  # add new repair info for vin
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
def addindividual():
    form = IndividualForm()
    print(session, file=sys.stderr)
    if request.method == "GET":
        return render_template('addindividual.html', form=form, session=session)
    if request.method == "POST":
        print(session, file=sys.stderr)
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
            # print(previous_page, file=sys.stderr)
            if session["previous_page"] == "purchase":
              session["customer"] = {
                "customer_id": last_customer_id,
                "customer_type": "Individual",
                "customer_name": "{} {}".format(form.individual_first_name.data, form.individual_last_name.data)
              }
              return redirect(url_for("purchasevehicle"))
            else:
              session["customer"] = {
                "customer_id": last_customer_id,
                "customer_type": "Individual",
                "customer_name": "{} {}".format(form.individual_first_name.data, form.individual_last_name.data)
              }
              return redirect(url_for("sellvehicle", vin=session["vin"]))
        else:
            return render_template('addindividual.html', form=form)

@app.route("/addbusiness", methods=['GET', 'POST'])
def addbusiness():
    form = BusinessForm()
    if request.method == "GET":
        return render_template('addbusiness.html', form=form, session=session)
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
            if session["previous_page"] == "purchase":
              session["customer"] = {
                "customer_id": last_customer_id,
                "customer_type": "Business",
                "customer_name": "{}".format(form.business_name.data)
              }
              return redirect(url_for("purchasevehicle"))
            else:
              session["customer"] = {
                "customer_id": last_customer_id,
                "customer_type": "Business",
                "customer_name": "{}".format(form.business_name.data)
              }
              return redirect(url_for("sellvehicle", vin=session["vin"]))
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


@app.route("/addmanufacturer", methods=['GET', 'POST'])
def add_manufacturer(previous_page=None):
    form = ManufacturerForm()
    if request.method == "GET":
        return render_template('addmanufacturer.html', form=form)
    if request.method == "POST":
        if form.validate() == True:
            cursor = mysql.connection.cursor()
            query = "INSERT INTO manufacturer (manufacturer_name) VALUES (%s)"
            variables = [form.manufacturer_name.data]
            cursor.execute(query, variables)
            mysql.connection.commit()
            print("testing", file=sys.stderr)
            return redirect(url_for("main"))
        else:
            return render_template('addmanufacturer.html', form=form)


@app.route("/addvehicletype", methods=['GET', 'POST'])
def add_vehicle_type(previous_page=None):
    form = VehicleTypeForm()
    if request.method == "GET":
        return render_template('addvehicletype.html', form=form)
    if request.method == "POST":
        if form.validate() == True:
            cursor = mysql.connection.cursor()
            query = "INSERT INTO vehicle_type (vehicle_type) VALUES (%s)"
            variables = [form.vehicle_type.data]
            cursor.execute(query, variables)
            mysql.connection.commit()
            print("testing", file=sys.stderr)
            return redirect(url_for("main"))
        else:
            return render_template('addvehicletype.html', form=form)


@app.route("/purchasevehicle", methods=["GET", "POST"])
def purchasevehicle():
      errors = []
      session["previous_page"] = "purchase"

      cursor = mysql.connection.cursor()
      cursor.execute("SELECT manufacturer_name from manufacturer")
      manufacturer_names = [record[0] for record in cursor.fetchall()]
      
      cursor.execute("SELECT vehicle_type from vehicle_type")
      vehicle_types = [record[0] for record in cursor.fetchall()]

      colors = ['Aluminum', 'Beige', 'Black', 'Blue', 'Brown', 'Bronze', 'Claret', 'Copper', 
      'Cream', 'Gold', 'Gray', 'Green', 'Maroon', 'Metallic', 'Navy', 'Orange', 'Pink', 
      'Purple', 'Red', 'Rose', 'Rust', 'Silver', 'Tan', 'Turquoise', 'White', 'Yellow']

      vehicle_conditions = ["Excellent", "Very Good", "Good", "Fair"]
      
      customer_type = session["customer"]["customer_type"] if "customer_type" in session["customer"].keys() else None
      customer_name = session["customer"]["customer_name"] if "customer_name" in session["customer"].keys() else None

      current_year = datetime.datetime.now().year
      print(session, file=sys.stderr)

      if request.method == "GET":
          return render_template("purchasevehicle.html", manufacturer_names=manufacturer_names,
          vehicle_types=vehicle_types, colors=colors, vehicle_conditions=vehicle_conditions, 
          customer_type=customer_type, customer_name=customer_name, errors=errors, session=session)
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
          sales_price = float(kbb_value) * 1.25
          colors = request.form.getlist("colors")
          customer_id = session["customer"]["customer_id"]

          vehicle_query = "INSERT INTO vehicle VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
          vehicle_values  = [vin, manufacturer_name, vehicle_type, model_year, model_name, 
          mileage, vehicle_condition, vehicle_description, sales_price, kbb_value]

          cursor.execute(vehicle_query, vehicle_values)

          color_query = "INSERT INTO vehicle_color VALUES (%s, %s)"
          for color in colors:
                color_values = [vin, color]
                cursor.execute(color_query, color_values)

          purchase_query = "INSERT INTO purchase VALUES (%s, %s, %s, %s)"
          purchase_date = str(datetime.datetime.now().date())
          purchase_values = (vin, customer_id, session["username"], purchase_date)

          cursor.execute(purchase_query, purchase_values)

          mysql.connection.commit()
          cursor.close()

          session["customer"] = {}

          return redirect(url_for("main"))

@app.route("/sell/vin=<string:vin>", methods=["GET", "POST"])
def sellvehicle(vin):
      errors = []
      session["previous_page"] = "sell"
      session["vin"] = vin
      print(session, file=sys.stderr)

      cursor = mysql.connection.cursor()
      
      customer_type = session["customer"]["customer_type"] if "customer_type" in session["customer"].keys() else None
      customer_name = session["customer"]["customer_name"] if "customer_name" in session["customer"].keys() else None

      cursor.execute("SELECT vin, manufacturer_name, vehicle_type, model_name, model_year, mileage, sales_price from vehicle where vin = %s", [vin])
      data = cursor.fetchone()

      vehicle_data = {}
      vehicle_data["vin"] = data[0]
      vehicle_data["manufacturer_name"] = data[1]
      vehicle_data["vehicle_type"] = data[2]
      vehicle_data["model_name"] = data[3]
      vehicle_data["model_year"] = data[4]
      vehicle_data["mileage"] = data[5]
      vehicle_data["sales_price"] = data[6]

      print(data, file=sys.stderr)
      return render_template("sellvehicle.html", vehicle_data=vehicle_data, session=session)

      # if request.method == "GET":
      #     return render_template("sellvehicle.html", vehicle_data=vehicle_data)

@app.route("/sellvehiclesubmit")
def sellvehiclesubmit():
  cursor = mysql.connection.cursor()

  sale_query = "INSERT INTO sale VALUES (%s, %s, %s, %s)"
  sale_date = str(datetime.datetime.now().date())
  sale_values = (session["vin"], session["customer"]["customer_id"], session["username"], sale_date)

  cursor.execute(sale_query, sale_values)
  mysql.connection.commit()
  cursor.close()
  session["customer"] = {}
  return redirect(url_for("main"))

@app.route("/searchcustomer", methods=["GET", "POST"])
def searchcustomer():
  print(session, file=sys.stderr)
  cursor = mysql.connection.cursor()
  data_found = False
  
  if request.method == "GET":
    return render_template('searchcustomer.html', session=session)
  
  if request.method == "POST":
    customer_type = request.form.get("customer_type")
    customer_key = request.form.get("customer_key")
    data_found = False

    print(customer_key, customer_type, file=sys.stderr)
    if customer_type == "Business":
      business_query = "SELECT customer_id, business_name from business where tax_id_number = %s"
      business_values = [customer_key]
      cursor.execute(business_query, business_values)
      data = cursor.fetchone()
      print(data, file=sys.stderr)
      if data:
        session["customer"]["customer_type"] = "Business"
        session["customer"]["customer_id"] = data[0]
        session["customer"]["customer_name"] = data[1]
    else:
      individual_query = "SELECT customer_id, individual_first_name, individual_last_name from individual where driver_license_number = %s"
      individual_values = [customer_key]
      cursor.execute(individual_query, individual_values)
      data = cursor.fetchone()
      if data:
        session["customer"]["customer_type"] = "Individual"
        session["customer"]["customer_id"] = data[0]
        session["customer"]["customer_name"] = "{} {}".format(data[1], data[2])
    return render_template('searchcustomer.html', session=session)

@app.route("/vin=<string:vin>")
def vehicledetail(vin):
  session["vin"] = vin
  print(session, file=sys.stderr)

  cursor = mysql.connection.cursor()
  cursor.execute(sql.vehicle_detail_vehicle, [vin])
  vehicle_data = cursor.fetchone()
  if vehicle_data:
    cursor.execute(sql.vehicle_detail_seller, [vin])
    seller_data = cursor.fetchone()
    
    cursor.execute(sql.vehicle_detail_buyer, [vin])
    buyer_data = cursor.fetchone()

  return render_template("vehicledetail.html", vehicle_data=vehicle_data, seller_data=seller_data, buyer_data=buyer_data, session=session)
  # if data:
  #   vin, manufacturer_name, vehicle_type, model_year, model_name, mileage, vehicle_condition, vehicle_description, sales_price, kbb_value = data


@app.route("/searchvendor", methods=["GET", "POST"])
def searchvendor(vendor_name=None):
    form = VendorSearchForm()
    cursor = mysql.connection.cursor()
    cursor.execute(sql.search_vendor(vendor_name))
    data = cursor.fetchall()
    return render_template('searchvendor.html', form=form, data=data)


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
