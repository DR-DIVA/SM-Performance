import pandas as pd

file_name = 'JUBILI_R-10_Parichat SM3_03_06_2569.th.csv'

try:
    df = pd.read_csv(file_name, encoding='utf-8')
except UnicodeDecodeError:
    try:
        df = pd.read_csv(file_name, encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv(file_name, encoding='tis-620')

with open('temp_jubili_output.txt', 'w', encoding='utf-8') as f:
    f.write('--- COLUMNS ---\n')
    f.write(str(df.columns.tolist()) + '\n')
    f.write('\n--- FIRST 5 ROWS ---\n')
    f.write(df.head(5).to_string() + '\n')
    f.write('\n--- INFO ---\n')
    f.write(f"Total rows: {len(df)}\n")
    f.write('\n--- MISSING DATA ---\n')
    f.write(df.isna().sum().to_string() + '\n')
