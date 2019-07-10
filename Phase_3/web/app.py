# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL

from flask_wtf import FlaskForm
from wtforms import StringField, validators, Form, SubmitField

# create the application object
app = Flask(__name__)
app.secret_key = 'development key'

# create the connection to MySQL
mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'abcd_123'
app.config['MYSQL_DB'] = 'cs6400_sm19_team013'
app.config['MYSQL_PORT'] = 3306

# use decorators to link the function to a url
@app.route('/')
def home():
    return "Hello, World!"  # return a string

@app.route('/welcome', methods=["GET", "POST"])
def welcome(query="DEFAULT"):
    return render_template('welcome.html', query=query)  # render a template

# route decorator for login page logic
@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
	    if request.form['username'] != 'admin' or request.form['password'] != 'admin':
	        error = 'Invalid Credentials. Please try again.'
	    else:
	    	return redirect(url_for('home'))
	return render_template('login.html', error=error)

# Create forms
class IndividualForm(FlaskForm):
    phone_number = StringField("Phone number", validators=[validators.DataRequired()])
    email = StringField("Email address")
    street = StringField("Street", validators=[validators.DataRequired()])
    city = StringField("City", validators=[validators.DataRequired()])
    state = StringField("State", validators=[validators.DataRequired()])
    postal_code = StringField("Postal code", validators=[validators.DataRequired()])

    # driver_license_number = StringField("Driver license number", validators=[validators.DataRequired()])
    # individual_first_name = StringField("First name", validators=[validators.DataRequired()])
    # individual_last_name = StringField("Last name", validators=[validators.DataRequired()])
    submit = SubmitField("Send")

class BusinessForm(FlaskForm):
    phone_number = StringField("Phone number", validators=[validators.DataRequired()])
    email = StringField("Email address", validators=[])
    street = StringField("Street", validators=[validators.DataRequired()])
    city = StringField("City", validators=[validators.DataRequired()])
    state = StringField("State", validators=[validators.DataRequired()])
    postal_code = StringField("Postal code", validators=[validators.DataRequired()])

    tax_id_number = StringField("Business tax ID", validators=[validators.DataRequired()])
    business_name = StringField("Business name", validators=[validators.DataRequired()])
    pc_name = StringField("Primary contact name", validators=[validators.DataRequired()])
    pc_title = StringField("Primary contact title", validators=[validators.DataRequired()])

# class RepairForm(FlaskForm):
#     vendor_name = StringField("Vendor name", validators[validators.DataRequired()])

# @app.route('/repair')
# @app.route('/repairs')
@app.route('/repairs/vin=<string:vin>', methods=["GET", "POST"]) # http://localhost:5000/repairs/some_vin
# @login_required
def repairs(vin="BLANK"):
    cursor = mysql.connection.cursor()
    cursor.execute(("SELECT * FROM repair WHERE vin = '"+vin+"'"),)
    repair_data = cursor.fetchall()
    mysql.connection.commit()
    post_confirm = "nope"
    if request.method == "POST":
        post_confirm = "YUP"
    return render_template("repairs.html", vin=vin, repair_data=repair_data, confirm=post_confirm)

@app.route("/addindividual", methods=['GET', 'POST'])
def addindividual():
    form = IndividualForm()
    if request.method == "GET":
        return render_template('addindividual.html', form=form)
    if request.method == "POST":
        if form.validate() == True:
            phone_number = form.phone_number.data
            email = form.email.data
            street = form.street.data
            city = form.city.data
            state = form.state.data
            postal_code = form.postal_code.data
            
            # driver_license_number = form.driver_license_number.data 
            # individual_first_name = form.individual_first_name.data 
            # individual_last_name = form.individual_last_name.data 
            # query = "INSERT INTO customer (customer_id, phone_number, email, street, city, state, postal_code) VALUES (NULL, {0}, {1}, {2}, {3}, {4}, {5})".format(phone_number, email, street, city, state, postal_code)
            cursor = mysql.connection.cursor()
            query = "INSERT INTO customer (customer_id, phone_number, email, street, city, state, postal_code) VALUES (NULL, %s, %s, %s, %s, %s, %s)"
            variables = phone_number, email, street, city, state, postal_code
            cursor.execute((query, variables))
            mysql.connection.commit()
            # return render_template('welcome.html', query="query")
            return redirect(url_for("welcome"))
        else:
            return render_template('addindividual.html', form=form)

@app.route("/addbusiness", methods=['GET', 'POST'])
def addbusiness():
    pass


@app.route("/searchcustomer")
def searchcustomer():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * from customer''')
    rv = cur.fetchall()
    return str(rv)

@app.route('/dropdown', methods=['GET', 'POST'])
def dropdown():
    colours = ['Red', 'Blue', 'Black', 'Orange']
    form = CustomerID()
    if form.validate_on_submit():
        return render_template('test.html', colours=colours)

@app.route('/reoport/sellerhistory', methods=['GET'])
def get_SellerHistory():
    cursor.execute("""SELECT 
  customer_id,
  customer_name,
  COUNT(*) AS vehicles_sold,
  AVG(purchase_price) AS avg_purchase_price,
  AVG(number_of_repairs) AS avg_number_of_repairs
FROM
(SELECT
  customer.customer_id,
  individual.individual_first_name + " " + individual.individual_last_name AS customer_name,
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

if __name__ == "__main__":
    app.run(debug=True)