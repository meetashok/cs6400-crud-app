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
# {{{ reports_seller_history()
  @property
  def reports_seller_history(self):
    return """
    SELECT 
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
    (
    SELECT 
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
      avg_purchase_price ASC
      """
# }}}
# {{{ reports_inventory_age()
  @property
  def reports_inventoryage(self):
    return """
    SELECT
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
    on vehicle_type.vehicle_type=a.vehicle_type
    """
# }}}
# {{{ reports_average_time_in_inventory()
  @property
  def reports_average_time_in_inventory(self):
    return """
    SELECT
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
      sales_date IS NOT NULL
    GROUP BY vehicle_type) AS a
    ON a.vehicle_type=vehicle_type.vehicle_type
    """
# }}}
# {{{ reports_priceperrepair()
  @property
  def reports_price_per_repair(self):
    return """
    SELECT
    vehicle_type,
    AVG(CASE WHEN vehicle_condition='Excellent' THEN kbb_value ELSE 0 END) AS 'Condition=Excellent',
    AVG(CASE WHEN vehicle_condition='Very Good' THEN kbb_value ELSE 0 END) AS 'Condition=Very Good',
    AVG(CASE WHEN vehicle_condition='Good' THEN kbb_value ELSE 0 END) AS 'Condition=Good',
    AVG(CASE WHEN vehicle_condition='Fair' THEN kbb_value ELSE 0 END) AS 'Condition=Fair'
    FROM vehicle
    GROUP BY vehicle_type
    """
# }}} 
# {{{ reports_repair_statistics()
  @property
  def reports_repair_statistics(self):
    return """ SELECT
    vendor_name,
    COUNT(*) AS number_of_repairs, 
    SUM(total_cost) AS total_spend,
    COUNT(distinct vin) AS number_of_vehicles,
    AVG(DATEDIFF(repair_end_date, repair_start_date)) AS avg_duration
    FROM repair
    WHERE
      repair_status='Complete'
    GROUP BY vendor_name"""
# }}}
# {{{ reports_monthly_sales()
  @property
  def reports_monthly_sales(self):
    return """
    SELECT 
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
    order by ym DESC
    """
# }}}
# {{{ reports_monthly_sales_drilldown()
  def reports_monthly_sales_drilldown(self, yearmonth):
    return """
    SELECT
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
      DATE_FORMAT(sales_date, '%Y-%m')=""" + "'" + yearmonth + "'" + """ GROUP BY 
    user.login_username
    ORDER BY
     number_of_vehicles DESC,
     total_sales DESC"""
# }}}
