# Global Aerospace Supply Chain Analysis

**Tools:** Python · SQL (PostgreSQL) · Power BI  
**Dataset:** 5,000 synthetic orders across 7 global supplier regions

-----

## Overview

This project simulates an aerospace procurement analyst’s workflow: ingesting raw logistics data, cleaning it, computing delay and defect KPIs, and surfacing actionable insights for operations leadership.

-----

## Repository Structure

```
aerospace/
├── generate_data.py                  (generates synthetic 5,000-row CSV)
├── analysis.py                       (cleaning, KPI computation, chart export)
├── aerospace_queries.sql             (PostgreSQL schema + 5 analytical queries)
├── aerospace_supply_chain.csv        (raw dataset)
├── aerospace_supply_chain_clean.csv  (cleaned dataset)
├── supplier_summary.csv              (aggregated supplier KPIs)
└── aerospace_dashboard.png           (exported chart dashboard)
```

-----

## Key Findings

|Metric                      |Value                                 |
|----------------------------|--------------------------------------|
|Delayed orders              |~77% of all orders                    |
|Worst defect region         |South Asia (avg 4.2%)                 |
|Highest avg delay           |South America (~5.6 days)             |
|Most expensive part by spend|Composite Nosecone / Fuel Injector    |
|Q3 shortage risk month      |August (predicted +23% above baseline)|

-----

## How to Run

**Step 1** — Generate the dataset

```
python generate_data.py
```

**Step 2** — Run the analysis and export charts

```
python analysis.py
```

**Step 3** — Load the cleaned CSV into PostgreSQL, then run the SQL queries

```
psql -d your_db -f aerospace_queries.sql
```

-----

## Power BI Dashboard Setup

1. Open Power BI Desktop → **Get Data → Text/CSV** → load `aerospace_supply_chain_clean.csv`
1. In **Power Query Editor**, verify column types (Delay_In_Days = Whole Number, Shipping_Cost = Decimal)
1. Create the following visuals:
- **Clustered Bar Chart** — Axis: Supplier_Location | Values: Delay_In_Days (Average) — *“Avg Delay by Region”*
- **Scatter Chart** — X-axis: Defect_Rate | Y-axis: Shipping_Cost | Details: Supplier_Location — *“Defect Rate vs. Cost”*
- **Line Chart** — from supplier_summary.csv for trend views
- **KPI Card** — Is_Delayed (Average, formatted as %) — *“Overall Delay Rate”*
1. Add slicers on Part_Name and Supplier_Location for interactivity
1. Publish to Power BI Service for a shareable link

-----

## Business Recommendations

- **Diversify South Asia suppliers** — highest defect rate (4.2%) and longest average delays compound risk on high-value parts
- **Pre-order Q3 critical stock in Q2** — forecast indicates August demand spike exceeds safe threshold
- **Prioritise Avionics Module & Navigation Computer sourcing** — largest total spend on delayed orders, highest ROI for renegotiation
