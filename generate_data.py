"""
generate_data.py
Generates a synthetic aerospace supply chain dataset (5,000 rows).
Run: python generate_data.py
Output: aerospace_supply_chain.csv
"""

import pandas as pd
import numpy as np
np.random.seed(42)
N = 5000
PARTS = [
"Turbine Blade", "Heat Shield", "Fuel Injector", "Landing Gear Assembly",
"Avionics Module", "Hydraulic Pump", "Carbon Fibre Panel", "Oxygen Sensor",
"Navigation Computer", "Engine Mount", "Rotor Hub", "Composite Nosecone",
"Thrust Reverser", "APU Unit", "Pressurisation Valve"
]
SUPPLIERS = {
"North America": {"base_delay": 2.1, "defect_base": 0.018},
"Western Europe": {"base_delay": 1.4, "defect_base": 0.012},
"Eastern Europe": {"base_delay": 3.8, "defect_base": 0.027},
"East Asia": {"base_delay": 4.5, "defect_base": 0.031},
"South Asia": {"base_delay": 5.9, "defect_base": 0.042},
"Middle East": {"base_delay": 3.2, "defect_base": 0.022},
"South America": {"base_delay": 6.1, "defect_base": 0.038},
}
regions = list(SUPPLIERS.keys())
region_weights = [0.22, 0.25, 0.10, 0.20, 0.10, 0.07, 0.06]
order_ids = [f"AE-{str(i).zfill(5)}" for i in range(1, N + 1)]
part_names = np.random.choice(PARTS, size=N)
supplier_locations = np.random.choice(regions, size=N, p=region_weights)
expected_days = np.where(
np.isin(supplier_locations, ["North America", "Western Europe"]),
np.random.randint(7, 21, N),
np.random.randint(14, 45, N)
)
actual_days = []

defect_rates = []
shipping_costs = []
for i, region in enumerate(supplier_locations):
params = SUPPLIERS[region]
delay = max(0, np.random.normal(params["base_delay"], 2.5))
actual = int(expected_days[i] + delay)
actual_days.append(actual)
defect = round(max(0, np.random.normal(params["defect_base"], 0.005)), 4)
defect_rates.append(defect)
base_cost = np.random.uniform(1200, 85000)
cost = round(base_cost * (1 + delay * 0.015), 2)
shipping_costs.append(cost)
# Inject ~3% missing values realistically
df = pd.DataFrame({
"Order_ID": order_ids,
"Part_Name": part_names,
"Supplier_Location": supplier_locations,
"Expected_Delivery_Days": expected_days,
"Actual_Delivery_Days": actual_days,
"Shipping_Cost": shipping_costs,
"Defect_Rate": defect_rates,
})
for col in ["Shipping_Cost", "Defect_Rate", "Actual_Delivery_Days"]:
mask = np.random.random(N) < 0.03
df.loc[mask, col] = np.nan
df.to_csv("aerospace_supply_chain.csv", index=False)
print(f"Dataset generated: {len(df)} rows → aerospace_supply_chain.csv")
print(df.head())
