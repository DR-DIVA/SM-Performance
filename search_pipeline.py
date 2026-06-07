import glob
import pandas as pd
import re

csv_files = glob.glob('JUBILI_R-*.csv')

keywords = [
    'ติดต่อ', 'ทำนัด', 'นำเสนอ', 'บรีฟ', 'ส่งตัวอย่าง', 'เสนอราคา', 
    'มัดจำ', '50%', 'พัฒนาสูตร', 'อย', '100%', 'SO', 'ผลิต', 'ส่งมอบ', 'Repeat'
]

print("--- Searching for Pipeline Keywords in JUBILI CSVs ---")
for f in csv_files:
    try:
        with open(f, 'r', encoding='utf-8-sig', errors='ignore') as file:
            lines = file.readlines()
            for line in lines:
                for kw in keywords:
                    if kw in line:
                        print(f"Found '{kw}' in {f}:")
                        # print first 100 chars of line to keep it brief
                        print(f"  > {line[:200].strip()}")
                        break # move to next line
    except Exception as e:
        print(f"Error reading {f}: {e}")
