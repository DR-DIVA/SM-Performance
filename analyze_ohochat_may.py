import pandas as pd

file_name = 'บริษัท คอสเมดิวา จำกัด_รายชื่อลูกค้า_ข้อมูลทั่วไป_2026-06-03.csv'

try:
    df = pd.read_csv(file_name, encoding='utf-8')
except UnicodeDecodeError:
    try:
        df = pd.read_csv(file_name, encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv(file_name, encoding='tis-620')

with open('temp_ohochat_may.txt', 'w', encoding='utf-8') as f:
    f.write('--- INFO ---\n')
    f.write(f"Total Rows (Chats): {len(df)}\n")
    
    if 'phone' in df.columns:
        valid_phones = df['phone'].notna().sum()
        f.write(f"Rows with Phone Number: {valid_phones} ({(valid_phones/len(df))*100:.2f}%)\n")
    else:
        f.write("No 'phone' column found.\n")
        
    f.write('\n--- TOP 10 TAGS ---\n')
    if 'tags' in df.columns:
        f.write(df['tags'].value_counts().head(10).to_string() + '\n')
    else:
        f.write("No 'tags' column found.\n")
