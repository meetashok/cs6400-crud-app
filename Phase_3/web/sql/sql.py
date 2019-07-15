class QueryDB:
# {{{ constructor()
  def __init__(self):
    pass
# }}}
# {{{ vehicle_detail_vehicle()
  @property
  def vehicle_detail_vehicle(self):
    return """
    SELECT
      vehicle.vin, 
      manufacturer_name, 
      vehicle_type,
      model_year,
      model_name, 
      mileage,
      vehicle_condition,
      vehicle_description,
      sales_price,
      kbb_value,
      color,
      coalesce(repair_cost, 0)
      FROM vehicle
      LEFT JOIN (
      SELECT 
      vin,
      GROUP_CONCAT(color ORDER BY color ASC SEPARATOR ', ') as color
      FROM vehicle_color
      GROUP BY vin
      ) as vehicle_color_grouped
      ON vehicle_color_grouped.vin=vehicle.vin
      LEFT JOIN (
      SELECT 
      vin,
      sum(total_cost) as repair_cost
      FROM repair
      GROUP BY vin
      ) as repair_cost
      ON vehicle.vin=repair_cost.vin
      where vehicle.vin = %s
    """    
# }}}
# {{{ vehicle_detail_seller()
  @property
  def vehicle_detail_seller(self):
    return """
    SELECT
      vehicle.vin, 
      purchase.customer_id,
      purchase.login_username,
      purchase.purchase_date,
      customer.email,
      customer.street,
      customer.city,
      customer.state,
      customer.postal_code,
      business.tax_id_number,
      business.business_name,
      business.pc_name,
      business.pc_title, 
      individual.driver_license_number,
      individual.individual_first_name,
      individual.individual_last_name,
      user.user_first_name,
      user.user_last_name
      FROM vehicle
      LEFT JOIN purchase
      ON vehicle.vin = purchase.vin
      LEFT JOIN customer
      ON purchase.customer_id = customer.customer_id
      LEFT JOIN individual
      ON customer.customer_id = individual.customer_id
      LEFT JOIN business
      ON customer.customer_id = business.customer_id
      LEFT JOIN user
      ON purchase.login_username = user.login_username
      where vehicle.vin = %s
    """    
# }}}
# {{{ vehicle_detail_buyer()
  @property
  def vehicle_detail_buyer(self):
    return """
    SELECT
      vehicle.vin, 
      sale.customer_id,
      sale.login_username,
      sale.sales_date,
      customer.email,
      customer.street,
      customer.city,
      customer.state,
      customer.postal_code,
      business.tax_id_number,
      business.business_name,
      business.pc_name,
      business.pc_title, 
      individual.driver_license_number,
      individual.individual_first_name,
      individual.individual_last_name,
      user.user_first_name,
      user.user_last_name
      FROM vehicle
      LEFT JOIN sale
      ON vehicle.vin = sale.vin
      LEFT JOIN customer
      ON sale.customer_id = customer.customer_id
      LEFT JOIN individual
      ON customer.customer_id = individual.customer_id
      LEFT JOIN business
      ON customer.customer_id = business.customer_id
      LEFT JOIN user
      ON sale.login_username = user.login_username
      where vehicle.vin = %s
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
# search
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
# {{{ count_vehicles_with_repairs()
  @property
  def count_vehicles_with_repairs(self):
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
        vehicle_in_repair.vin IS NOT NULL AND
        sale.sales_date IS NULL; 
    """
# }}}
# {{{ get_vehicle_types()
  @property
  def get_vehicle_types(self):
    return """
      SELECT vehicle_type
      FROM vehicle_type
    """
# }}}
# {{{ get_manufacturers()
  @property
  def get_manufacturers(self):
    return """
      SELECT manufacturer_name
      FROM manufacturer
    """
# }}}
# {{{ vehicle_search()
  @property
  def vehicle_search(self):
    return """
      SELECT
        vehicle.vin,
        vehicle.vehicle_type,
        vehicle.model_year,
        vehicle.manufacturer_name,
        vehicle.model_name,
        vehicle_color_grouped.color,
        vehicle.mileage,
        vehicle.sales_price,
        vehicle.vehicle_condition,
        vehicle.vehicle_description
      FROM vehicle
      LEFT JOIN (
        SELECT
          vin,
          GROUP_CONCAT(color ORDER BY color ASC SEPARATOR ',') as color
        FROM vehicle_color
        GROUP BY vin
      ) as vehicle_color_grouped
      ON vehicle_color_grouped.vin=vehicle.vin
      LEFT JOIN
      (
        SELECT
          distinct(vin) as vin
        FROM repair
        WHERE repair_status IN ('In Progress','Pending')
      ) vehicle_in_repair
      ON vehicle.vin=vehicle_in_repair.vin
      LEFT JOIN sale
      ON vehicle.vin=sale.vin
      WHERE
        vehicle_in_repair.vin IS NULL AND
        sale.sales_date IS NULL AND
         
        vehicle_type LIKE %s AND
        manufacturer_name LIKE %s AND
        model_year LIKE %s AND
        color LIKE %s AND
        (
          vehicle_type LIKE %s OR
          manufacturer_name LIKE %s OR
          model_year LIKE %s OR
          vehicle_description LIKE %s OR
          model_name LIKE %s OR
          color LIKE %s
        )
    """
# }}}
# {{{ vehicle_search_clerk()
  @property
  def vehicle_search_clerk(self):
    return """
      SELECT
        vehicle.vin,
        vehicle.vehicle_type,
        vehicle.model_year,
        vehicle.manufacturer_name,
        vehicle.model_name,
        vehicle_color_grouped.color,
        vehicle.mileage,
        vehicle.sales_price,
        vehicle.vehicle_condition,
        vehicle.vehicle_description
      FROM vehicle
      LEFT JOIN (
        SELECT
          vin,
          GROUP_CONCAT(color ORDER BY color ASC SEPARATOR ',') as color
        FROM vehicle_color
        GROUP BY vin
      ) as vehicle_color_grouped
      ON vehicle_color_grouped.vin=vehicle.vin
      LEFT JOIN
      (
        SELECT
          distinct(vin) as vin
        FROM repair
        WHERE repair_status IN ('In Progress','Pending')
      ) vehicle_in_repair
      ON vehicle.vin=vehicle_in_repair.vin
      LEFT JOIN sale
      ON vehicle.vin=sale.vin
      WHERE
        sale.sales_date IS NULL AND
         
        vehicle_type LIKE %s AND
        manufacturer_name LIKE %s AND
        model_year LIKE %s AND
        color LIKE %s AND
        (
          vehicle_type LIKE %s OR
          manufacturer_name LIKE %s OR
          model_year LIKE %s OR
          vehicle_description LIKE %s OR
          model_name LIKE %s OR
          color LIKE %s
        )
    """
# }}}
# {{{ vehicle_search_management_and_burdell_both_sold_and_unsold()
  @property
  def vehicle_search_management_and_burdell_both_sold_and_unsold(self):
    return """
      SELECT
        vehicle.vin,
        vehicle.vehicle_type,
        vehicle.model_year,
        vehicle.manufacturer_name,
        vehicle.model_name,
        vehicle_color_grouped.color,
        vehicle.mileage,
        vehicle.sales_price,
        vehicle.vehicle_condition,
        vehicle.vehicle_description,
        sale.sales_date
      FROM vehicle
      LEFT JOIN (
        SELECT
          vin,
          GROUP_CONCAT(color ORDER BY color ASC SEPARATOR ',') as color
        FROM vehicle_color
        GROUP BY vin
      ) as vehicle_color_grouped
      ON vehicle_color_grouped.vin=vehicle.vin
      LEFT JOIN
      (
        SELECT
          distinct(vin) as vin
        FROM repair
        WHERE repair_status IN ('In Progress','Pending')
      ) vehicle_in_repair
      ON vehicle.vin=vehicle_in_repair.vin
      LEFT JOIN sale
      ON vehicle.vin=sale.vin
      WHERE
        vehicle_type LIKE %s AND
        manufacturer_name LIKE %s AND
        model_year LIKE %s AND
        color LIKE %s AND
        (
          vehicle_type LIKE %s OR
          manufacturer_name LIKE %s OR
          model_year LIKE %s OR
          vehicle_description LIKE %s OR
          model_name LIKE %s OR
          color LIKE %s
        )
    """
# }}}
# {{{ vehicle_search_management_and_burdell_sold()
  @property
  def vehicle_search_management_and_burdell_sold(self):
    return """
      SELECT
        vehicle.vin,
        vehicle.vehicle_type,
        vehicle.model_year,
        vehicle.manufacturer_name,
        vehicle.model_name,
        vehicle_color_grouped.color,
        vehicle.mileage,
        vehicle.sales_price,
        vehicle.vehicle_condition,
        vehicle.vehicle_description,
        sale.sales_date
      FROM vehicle
      LEFT JOIN (
        SELECT
          vin,
          GROUP_CONCAT(color ORDER BY color ASC SEPARATOR ',') as color
        FROM vehicle_color
        GROUP BY vin
      ) as vehicle_color_grouped
      ON vehicle_color_grouped.vin=vehicle.vin
      LEFT JOIN
      (
        SELECT
          distinct(vin) as vin
        FROM repair
        WHERE repair_status IN ('In Progress','Pending')
      ) vehicle_in_repair
      ON vehicle.vin=vehicle_in_repair.vin
      LEFT JOIN sale
      ON vehicle.vin=sale.vin
      WHERE
        sale.sales_date IS NOT NULL AND
        vehicle_type LIKE %s AND
        manufacturer_name LIKE %s AND
        model_year LIKE %s AND
        color LIKE %s AND
        (
          vehicle_type LIKE %s OR
          manufacturer_name LIKE %s OR
          model_year LIKE %s OR
          vehicle_description LIKE %s OR
          model_name LIKE %s OR
          color LIKE %s
        )
    """
# }}}
# {{{ vehicle_search_management_and_burdell_unsold()
  @property
  def vehicle_search_management_and_burdell_unsold(self):
    return """
      SELECT
        vehicle.vin,
        vehicle.vehicle_type,
        vehicle.model_year,
        vehicle.manufacturer_name,
        vehicle.model_name,
        vehicle_color_grouped.color,
        vehicle.mileage,
        vehicle.sales_price,
        vehicle.vehicle_condition,
        vehicle.vehicle_description,
        sale.sales_date
      FROM vehicle
      LEFT JOIN (
        SELECT
          vin,
          GROUP_CONCAT(color ORDER BY color ASC SEPARATOR ',') as color
        FROM vehicle_color
        GROUP BY vin
      ) as vehicle_color_grouped
      ON vehicle_color_grouped.vin=vehicle.vin
      LEFT JOIN
      (
        SELECT
          distinct(vin) as vin
        FROM repair
        WHERE repair_status IN ('In Progress','Pending')
      ) vehicle_in_repair
      ON vehicle.vin=vehicle_in_repair.vin
      LEFT JOIN sale
      ON vehicle.vin=sale.vin
      WHERE
        sale.sales_date IS  NULL AND
        vehicle_type LIKE %s AND
        manufacturer_name LIKE %s AND
        model_year LIKE %s AND
        color LIKE %s AND
        (
          vehicle_type LIKE %s OR
          manufacturer_name LIKE %s OR
          model_year LIKE %s OR
          vehicle_description LIKE %s OR
          model_name LIKE %s OR
          color LIKE %s
        )
    """
# }}}
# {{{ vehicle_search_by_vin()
  @property
  def vehicle_search_by_vin(self):
    return """
      SELECT
        vehicle.vin,
        vehicle.vehicle_type,
        vehicle.model_year,
        vehicle.manufacturer_name,
        vehicle.model_name,
        vehicle_color_grouped.color,
        vehicle.mileage,
        vehicle.sales_price,
        vehicle.vehicle_condition,
        vehicle.vehicle_description
      FROM vehicle
      LEFT JOIN (
        SELECT
          vin,
          GROUP_CONCAT(color ORDER BY color ASC SEPARATOR ',') as
          color
        FROM vehicle_color
        GROUP BY vin
      ) as vehicle_color_grouped
      ON vehicle_color_grouped .vin= vehicle .vin
      WHERE vehicle.vin = %s
    """
# }}}
# repairs
# {{{ repairs_show_repairs()
  @property
  def repairs_show_repairs(self):
    return """
     SELECT 
       vin, repair_start_date, repair_end_date, vendor_name, nhtsa_recall_number, total_cost, repair_description, repair_status
     FROM repair 
     WHERE vin = %s
    """
# }}}
# {{{ repairs_update_status()
  @property
  def repairs_update_status(self, next_status):
    return """
     UPDATE repair
     SET vin = vin, repair_start_date = repair_start_date, repair_end_date = repair_end_date, vendor_name = vendor_name, nhtsa_recall_number = nhtsa_recall_number, total_cost = total_cost, repair_description = repair_description, repair_status= """ +  next_status + """FROM repair 
     WHERE vin = %s
    """
# }}}
# reports
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
    return """SELECT
    vendor_name,
    COUNT(*) AS number_of_repairs, 
    SUM(total_cost) AS total_spend,
    COUNT(distinct vin) AS number_of_vehicles,
    AVG(DATEDIFF(repair_end_date, repair_start_date)) AS avg_duration
    FROM repair
    WHERE
      repair_status='completed'
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
      DATE_FORMAT(sales_date, '%Y-%m')='""" + yearmonth + """' GROUP BY 
    user.login_username
    ORDER BY
     number_of_vehicles DESC,
     total_sales DESC
    """

# }}}
# {{{ reports_search_vendor_drilldown()
  @property
  def search_vendor(self, vendor_name):
    return """
    SELECT
      vendor_name,
      vendor_phone_number,
      street,
      city,
      state,
      postal_code
    FROM ​vendor 
    WHERE
      vendor_name=​""" +vendor_name
# }}}
