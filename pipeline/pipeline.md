# DS 4320 Project 1: NFL Combine Performance as a Predictor for Career Value

Pipeline Notebook | Kieran | rrx5eg

This notebook demonstrates the full solution pipeline:

Build the relational database from raw CSV files using DuckDB

Query the database to prepare the analysis dataset

Implement and evaluate a predictive ML model

Visualize results at publication quality

## Part 1: Data Preparation — Load CSVs into DuckDB

We use DuckDB as our in-process analytical database. Each of the four relational tables is loaded from its CSV file in the /data folder. DuckDB lets us query them with standard SQL without needing a separate database server.

import duckdb
import pandas as pd
import logging
import os

# --- Logging setup ---
logging.basicConfig(
    filename='pipeline.log',
    level=logging.INFO,
    format='%(asctime)s — %(levelname)s — %(message)s'
)
logging.info('Pipeline started.')
print('Logging initialized. Output will be written to pipeline.log')


# --- Connect to DuckDB ---
try:
    con = duckdb.connect(':memory:')
    logging.info('DuckDB connection established.')
    print('DuckDB connected successfully.')
except Exception as e:
    logging.error(f'Failed to connect to DuckDB: {e}')
    raise


Loading Relational Tables

Each CSV corresponds to one entity in the ER diagram.

DATA_DIR = './data' 

tables = {
    'players':          'players.csv',
    'combine_stats':    'combine_stats.csv',
    'pro_performance':  'pro_performance.csv',
    'position_groups':  'position_groups.csv',
}

for table_name, filename in tables.items():
    filepath = os.path.join(DATA_DIR, filename)
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto('{filepath}')")
    count = con.execute(f'SELECT COUNT(*) FROM {table_name}').fetchone()[0]
    print(f'  {table_name}: {count} rows loaded.')


Output:

players: 5636 rows loaded.

combine_stats: 5636 rows loaded.

pro_performance: 5636 rows loaded.

position_groups: 16 rows loaded.

Part 2: SQL Queries — Prepare the Analysis Dataset

We join all four tables to produce a flat analysis-ready view.

# --- Query 1: Full join — the master analysis dataset ---
query_full_join = """
    SELECT
        p.player_id,
        p.name,
        p.position,
        pg.group_name          AS position_group,
        cs.forty_yd_dash,
        cs.vertical_jump,
        cs.broad_jump,
        cs.three_cone,
        cs.shuttle_run,
        pp.career_av
    FROM players p
    JOIN combine_stats cs  ON p.player_id = cs.player_id
    JOIN pro_performance pp ON p.player_id = pp.player_id
    JOIN position_groups pg ON p.position = pg.position
    WHERE cs.forty_yd_dash IS NOT NULL AND pp.career_av IS NOT NULL
"""

df_analysis = con.execute(query_full_join).df()
print(f'Analysis dataset shape: {df_analysis.shape}')


Part 3: ML Model — Predicting Career AV

We implement a Random Forest Regressor to capture non-linear relationships.

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

FEATURES = ['forty_yd_dash', 'vertical_jump', 'broad_jump', 'three_cone', 'shuttle_run', 'weight']
TARGET = 'career_av'

X = df_analysis[FEATURES]
y = df_analysis[TARGET]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestRegressor(n_estimators=200, max_depth=8, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

print(f'Random Forest RMSE: {mean_squared_error(y_test, y_pred)**0.5:.2f}')
print(f'Random Forest R²: {r2_score(y_test, y_pred):.3f}')


## Part 4: Visualizations

Feature Importance

This horizontal bar chart identifies which Combine drills have the highest predictive power for Career AV.

Predicted vs. Actual Career AV

This scatter plot visualizes the model's accuracy. The red dashed line represents perfect prediction.

Average AV by Position Group

This chart demonstrates the systematic variance in "Approximate Value" across different position types, justifying the need for positional benchmarking.

Summary

Model

RMSE

R²

Linear Regression

24.51

0.037

Random Forest

23.46

0.117

The Random Forest outperforms Linear Regression on this task, capturing threshold effects (e.g., "fast enough") that linear models miss. The results suggest that while athleticism is a foundation, the high variance in AV highlights the impact of non-physical traits on professional success.


## Final Conclusion

The Random Forest model demonstrates that NFL Combine metrics have weak predictive power for Career Approximate Value (CAV). While extreme athletic outliers may show some predictive signal, the vast majority of players cluster in a range where performance is not well explained by combine data alone.

This reinforces the conclusion that athletic testing should be used as a supplementary evaluation tool rather than a primary predictor of NFL success.
