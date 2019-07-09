queries = {}

queries["test_query"] = '''
SELECT * 
FROM vehicle
'''

queries["vehicle_count"] = '''
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
  sale.sales_date IS NULL
'''