# main page with vehicle count, login, and search
@app.route('/', methods=['GET', 'POST'])
########Count of vehicles for sale
def main(query="DEFAULT"):
    cursor = mysql.connection.cursor()
    cursor.execute(("""SELECT
      count(vehicle.vin) as vehicles_available
FROM vehicle 
LEFT JOIN
(
  SELECT
    distinct(vin)  as vin
  FROM repair
  WHERE repair_status IN ('In Progress','Pending')
) vehicle_in_repair 
ON vehicle.vin=vehicle_in_repair.vin
LEFT JOIN sale
  ON vehicle.vin=sale.vin
WHERE 
  vehicle_in_repair.vin IS NULL AND
  sale.sales_date IS NULL;"""),)
    vehicle_data = cursor.fetchall()
    mysql.connection.commit() 
########Login section
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute('SELECT login_password, role FROM user WHERE login_username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        user = cursor.fetchone()
        # If account exists in accounts table in out database
        if user:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
# Show the login form with message (if any)
return render_template('main.html', msg=msg)    
######Logout section (need a button?)
def logout():
  # Remove session data, this will log the user out
 session.pop('loggedin', None)
 session.pop('id', None)
 session.pop('username', None)
 # Redirect to login page
 return redirect(url_for('main'))  
    return render_template('main.html', vehicle_data=vehicle_data, query=query, error=error)  # render main template
"""
##########Search form section
def search():
    form = SearchForm()
    if request.method == "GET":
        return render_template('main.html', form=form)

    if request.method == "POST":
        if form.validate() == True:
            vehicle_type = form.vehicle_type.data
            manufacturer_name = form.manufacturer_name.data
            color = form.color.data
            model_year = form.model_year.data
            keyword = form.keyword.data

            
            cursor = mysql.connection.cursor()
            query2 = "SELECT * FROM vehicle"
            #variables = vehicle_type, manufacturer_name, color, model_year, keyword
            cursor.execute((query, variables))
            mysql.connection.commit()
            # return render_template('welcome.html', query="query")
            return redirect(url_for("main"))

        else:
            return render_template('main.html', form=form)
""" 


