Global Aerospace Supply Chain Analysis
Tools: Python · SQL (PostgreSQL) · Power BI
Dataset: 5,000 synthetic orders across 7 global supplier regions

Overview
This project simulates an aerospace procurement analyst’s workflow: ingesting raw
logistics data, cleaning it, computing delay and defect KPIs, and surfacing actionable
insights for operations leadership.

Repository Structure
aerospace/
├── generate_data.py # Generates synthetic 5,000-row CSV
├── analysis.py # Cleaning, KPI computation, chart export
├── aerospace_queries.sql # PostgreSQL schema + 5 analytical queries
├── aerospace_supply_chain.csv # Raw dataset (generated)
├── aerospace_supply_chain_clean.csv # Cleaned dataset
├── supplier_summary.csv # Aggregated supplier KPIs
└── aerospace_dashboard.png # Exported chart dashboard

Key Findings
Metric Value
Delayed orders ~68% of all orders
Worst defect region South Asia (avg 4.2%)
Highest avg delay South America (~6.1 days)
Most expensive delayed part Avionics Module / Navigation Computer
Q3 shortage risk month August (predicted +23% above baseline)

How to Run

# Step 1 – generate the dataset
python generate_data.py
# Step 2 – run the analysis and export charts
python analysis.py
# Step 3 – load aerospace_supply_chain_clean.csv into PostgreSQL
# then run aerospace_queries.sql in your SQL client

Power BI Dashboard Setup
1. Open Power BI Desktop → Get Data → Text/CSV → load
aerospace_supply_chain_clean.csv
2. In Power Query Editor, verify column types (Delay_In_Days = Whole Number,
Shipping_Cost = Decimal)
3. Create the following visuals:
Clustered Bar Chart → Axis: Supplier_Location | Values: Delay_In_Days
(Average) → “Avg Delay by Region”
Scatter Chart → X-axis: Defect_Rate | Y-axis: Shipping_Cost | Details:
Supplier_Location → “Defect Rate vs. Cost”
Line Chart → from supplier_summary.csv for trend views
KPI Card → Is_Delayed (Average, formatted as %) → “Overall Delay Rate”
4. Add slicers on Part_Name and Supplier_Location for interactivity
5. Publish to Power BI Service for shareable link

Business Recommendations
Diversify South Asia suppliers — highest defect rate (4.2%) and longest average
delays compound risk on high-value parts
Pre-order Q3 critical stock in Q2 — forecast indicates August demand spike

exceeds safe threshold
Prioritise Avionics Module & Navigation Computer sourcing — largest total
spend on delayed orders, highest ROI for renegotiation
