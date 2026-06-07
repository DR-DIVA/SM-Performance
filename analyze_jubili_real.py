import pandas as pd

file_name = 'รายชื่อลูกค้า_1-249_บริษัท คอสเมดิวา จำกัด [Cosmediva Company Limited].xlsx'
df = pd.read_excel(file_name)

with open('temp_jubili_real_output.txt', 'w', encoding='utf-8') as f:
    f.write('--- COLUMNS ---\n')
    f.write(str(df.columns.tolist()) + '\n')
    f.write('\n--- FIRST 5 ROWS ---\n')
    f.write(df.head(5).to_string() + '\n')
    f.write('\n--- INFO ---\n')
    f.write(f"Total Rows: {len(df)}\n")
    if 'เบอร์โทรศัพท์' in df.columns or 'phone' in df.columns:
        phone_col = 'เบอร์โทรศัพท์' if 'เบอร์โทรศัพท์' in df.columns else 'phone'
        f.write(f"Rows with Phone: {df[phone_col].notna().sum()}\n")
