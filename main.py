import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "retail.csv"
DB_FILE = BASE_DIR / "Retail_database.db"

df = pd.read_csv(DATA_FILE)

print("Dataset loaded successfully")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

df["Order Date"] = pd.to_datetime(df["Order Date"],format="mixed",dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="mixed",dayfirst=True)

print("\nDate columns converted successfully")
print(df[["Order Date", "Ship Date"]].dtypes)

conn = sqlite3.connect(DB_FILE)

df.to_sql("sales_table", conn, if_exists="replace", index=False)

print("\nData saved to SQLite3 successfully")
print(
    "Rows in database:",
    pd.read_sql(
        "SELECT COUNT(*) AS total_rows FROM sales_table",
        conn
    ).iloc[0, 0]
)

check_df = pd.read_sql(
    "SELECT * FROM sales_table LIMIT 5",
    conn
)

print("\nDatabase validation successful")
print(check_df)

print("\nFinal dataset shape:", df.shape)
print("Pipeline completed successfully")

conn.close()