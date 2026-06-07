import fitz  # PyMuPDF
import sys
import re

try:
    doc = fitz.open('12_Monthly Content Report For COSMEDIVA.pdf')
    text = ""
    for page in doc:
        text += page.get_text()
    
    with open('temp_pdf_output.txt', 'w', encoding='utf-8') as f:
        f.write("--- PDF Content Excerpt ---\n")
        f.write(text[:2000] + "\n\n")
        
        spend = re.findall(r'(?i)(spend|budget|cost|amount spent).*?([\d,]+\.?\d*)', text)
        clicks = re.findall(r'(?i)(click|link clicks).*?([\d,]+)', text)
        reach = re.findall(r'(?i)(reach|impression).*?([\d,]+)', text)
        
        f.write("--- Extracted Metrics ---\n")
        f.write(f"Spend: {spend[:10]}\n")
        f.write(f"Clicks: {clicks[:10]}\n")
        f.write(f"Reach: {reach[:10]}\n")
        
    print("Done")
except Exception as e:
    print(f"Error: {e}")
