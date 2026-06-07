import pandas as pd
import glob
import os
import re

print("=== JUBILI CSV Analysis ===")
csv_files = glob.glob('JUBILI_R-*.csv')
print(f"Found {len(csv_files)} files: {csv_files}")

for f in csv_files:
    try:
        df = pd.read_csv(f, encoding='utf-8-sig', on_bad_lines='skip')
    except Exception as e:
        try:
            df = pd.read_csv(f, encoding='tis-620', on_bad_lines='skip')
        except Exception as e2:
            print(f"Error reading {f}: {e2}")
            continue
            
    print(f"\n--- {f} ---")
    cols = df.columns.astype(str).tolist()
    status_cols = [c for c in cols if any(k in c for k in ['สถานะ', 'ขั้น', 'กิจกรรม', 'หัวข้อ', 'โครงการ'])]
    
    if status_cols:
        print(f"Relevant Columns: {status_cols}")
        for col in status_cols:
            try:
                val_counts = df[col].value_counts().head(10)
                print(val_counts.to_string())
            except:
                pass
    
    rev_cols = [c for c in cols if any(k in c for k in ['มูลค่า', 'ยอด', 'ราคา', 'THB', 'ยอดขาย'])]
    if rev_cols:
        print(f"Revenue Columns: {rev_cols}")
