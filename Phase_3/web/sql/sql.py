class QueryDB:
# {{{ constructor()
  def __init__(self):
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
  @property
  def check_login_username_and_password(self):
    return """
      SELECT
        login_username,
        login_password,
        role
      FROM user
      WHERE
        login_username = %s AND 
        login_password = %s
    """
# }}}
