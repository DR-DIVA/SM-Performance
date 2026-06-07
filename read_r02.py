import pandas as pd
import glob
import sys

files = glob.glob('*JUBILI_R-02*.csv')
if not files:
    print("File not found.")
    sys.exit()

filename = files[0]
print(f"Reading: {filename}")
try:
    df = pd.read_csv(filename, encoding='utf-8-sig', skiprows=2)
except:
    try:
        df = pd.read_csv(filename, encoding='tis-620', skiprows=2)
    except:
        df = pd.read_csv(filename, encoding='utf-16', sep='\t', skiprows=2)

print("Columns:", df.columns.tolist())
print("First 10 rows:")
print(df.head(10))
