"""
File: to_database.py
Description: takes a csv file and turns it into a .db
"""

import pandas as pd
import sqlite3

# Read CSV file into DataFrame
# Add column names!!
df = pd.read_csv('sunspot.csv', 
        names=['Year', 
               'Month', 
               'Day', 
               'Date_Fraction', 
               'Daily_Sunspot_Total', 
               'Daily_Standard_Deviation', 
               'Observations', 
               'Def_prov'
        ]
    )
 
# Connect to SQLite database
conn = sqlite3.connect('sunspot.db')

# Write DataFrame to SQLite database
df.to_sql('sunspot', conn, if_exists='replace', index=False)

# Close database connection
conn.close()

# print success message
print("Conversion successful!")

