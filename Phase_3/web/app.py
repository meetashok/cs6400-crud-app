# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL

from flask_wtf import FlaskForm
from wtforms import StringField, validators

# create the application object
app = Flask(__name__)
app.secret_key = 'development key'

# create the connection to MySQL
mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'abcd_123'
app.config['MYSQL_DB'] = 'cs6400_sm19_team013'

# use decorators to link the function to a url
@app.route('/')
def home():
    return "Hello, World!"  # return a string

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


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

	# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)

# Create forms
class IndividualForm(FlaskForm):
    phone_number = StringField("phone_number", validators=[validators.DataRequired()])
    email = StringField("email", validators=[])
    street = StringField("street", validators=[validators.DataRequired()])
    city = StringField("city", validators=[validators.DataRequired()])
    state = StringField("state", validators=[validators.DataRequired()])
    postal_code = StringField("postal_code", validators=[validators.DataRequired()])

    driver_license_number = StringField("driver_license_number", validators=[validators.DataRequired()])
    individual_first_name = StringField("individual_first_name", validators=[validators.DataRequired()])
    individual_last_name = StringField("individual_last_name", validators=[validators.DataRequired()])

class BusinessForm(FlaskForm):
    phone_number = StringField("phone_number", validators=[validators.DataRequired()])
    email = StringField("email", validators=[])
    street = StringField("street", validators=[validators.DataRequired()])
    city = StringField("city", validators=[validators.DataRequired()])
    state = StringField("state", validators=[validators.DataRequired()])
    postal_code = StringField("postal_code", validators=[validators.DataRequired()])

    tax_id_number = StringField("tax_id_number", validators=[validators.DataRequired()])
    business_name = StringField("business_name", validators=[validators.DataRequired()])
    pc_name = StringField("pc_name", validators=[validators.DataRequired()])
    pc_title = StringField("pc_title", validators=[validators.DataRequired()])

@app.route("/addindividual", method=['GET', 'POST'])
def addindividual():
    if request.method == 'POST':
        pass
    else:
        pass

@app.route("/addbusiness", method=['GET', 'POST'])
def addbusiness():
    pass


@app.route("/searchcustomer")
def searchcustomer():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * from individual''')
    rv = cur.fetchall()
    return str(rv)

@app.route('/dropdown', methods=['GET', 'POST'])
def dropdown():
    colours = ['Red', 'Blue', 'Black', 'Orange']
    form = CustomerID()
    if form.validate_on_submit():
        return render_template('test.html', colours=colours)
