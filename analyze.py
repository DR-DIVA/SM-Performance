import pandas as pd

file_name = 'บริษัท คอสเมดิวา จำกัด_รายชื่อลูกค้า_ข้อมูลทั่วไป_25 พ.ค.-31 พ.ค. 69.xlsx'
df = pd.read_excel(file_name)

with open('temp_output.txt', 'w', encoding='utf-8') as f:
    f.write('--- COLUMNS ---\n')
    f.write(str(df.columns.tolist()) + '\n')
    f.write('\n--- FIRST 5 ROWS ---\n')
    f.write(df.head(5).to_string() + '\n')
    f.write('\n--- UNIQUE TAGS ---\n')
    if 'tags' in df.columns:
        f.write(df['tags'].value_counts().to_string() + '\n')
    else:
        f.write('No tags column found.\n')
