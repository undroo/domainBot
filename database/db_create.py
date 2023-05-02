import pandas as pd
import sqlite3

# Read the CSV file into a DataFrame
df = pd.read_csv('data/SuburbData2022.csv')

# Create a new SQLite database
conn = sqlite3.connect('SuburbCrime.db')

# Create a new table using the DataFrame
df.to_sql('SuburbData2022', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()
