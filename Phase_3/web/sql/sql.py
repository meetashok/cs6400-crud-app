import sys

class QueryDB:
# {{{ constructor()
  # def __init__(self, app):
  def __init__(self):
    # create the connection to MySQL
    # mysql = MySQL(app)
    #  
    # app.config['MYSQL_HOST'] = 'localhost'
    # app.config['MYSQL_USER'] = 'root'
    # app.config['MYSQL_PASSWORD'] = 'abcd_123'
    # app.config['MYSQL_DB'] = 'cs6400_sm19_team013'
    # app.config['MYSQL_PORT'] = 3306
    #  
    # cursor = mysql.connection.cursor()
    pass
# }}}
# {{{ count_vehicles_available()
  @property
  def count_vehicles_available(self):
    return """
      SELECT
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
        sale.sales_date IS NULL; 
    """
# }}}
# {{{ check_login_username_and_password()
  def check_login_username_and_password(self,username,password):
    return ("""
    SELECT 
      login_username, 
      login_password, 
      role 
    FROM user 
    WHERE
      login_username = %s AND 
      login_password = %s'
    """, (username, password))
# }}}
