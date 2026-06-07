import pandas as pd

filename = 'บริษัท คอสเมดิวา จำกัด_รายชื่อลูกค้า_ข้อมูลทั่วไป_16 April - 15 May 2026.csv'
try:
    df = pd.read_csv(filename, encoding='utf-8-sig')
except:
    df = pd.read_csv(filename, encoding='tis-620')
    
cols = df.columns.tolist()
print(f"Cols: {cols}")
print(df[cols[4:8]].head())
