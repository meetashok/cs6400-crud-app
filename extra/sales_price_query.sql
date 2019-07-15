
USE cs6400_sm19_team013;
SET SQL_SAFE_UPDATES = 0;

update vehicle, (select 
vehicle.vin,
coalesce(kbb_value * 1.25, 0)  + coalesce(r.repair_cost*1.1 , 0) as sales_price
from vehicle 
left join (select 
vin, 
coalesce(sum(total_cost), 0) as repair_cost from repair
group by vin) r
on vehicle.vin=r.vin) t
set vehicle.sales_price = t.sales_price
where vehicle.vin = t.vin;
