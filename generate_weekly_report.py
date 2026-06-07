import pandas as pd
import google.generativeai as genai
import os
from datetime import datetime

# ==========================================
# 0. ตั้งค่า API Key
# ==========================================
# (หากยังไม่มี API Key สามารถรันสคริปต์นี้เพื่อดูโครงสร้างข้อมูลก่อนได้)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "") 

# ==========================================
# 1. โหลดข้อมูล Ohochat
# ==========================================
ohochat_file = 'บริษัท คอสเมดิวา จำกัด_รายชื่อลูกค้า_ข้อมูลทั่วไป_25 พ.ค.-31 พ.ค. 69.xlsx'
try:
    ohochat_df = pd.read_excel(ohochat_file)
    print(f"✅ โหลดไฟล์ Ohochat สำเร็จ: พบข้อมูล {len(ohochat_df)} แชท")
except Exception as e:
    print(f"❌ ไม่พบไฟล์ Ohochat: {e}")
    exit(1)

# ==========================================
# 2. จำลองข้อมูล JUBILI (เนื่องจากยังไม่มีไฟล์จริง)
# ==========================================
# ในระบบจริง เราจะอ่านจาก pd.read_excel('jubili_export.xlsx')
# สมมติว่าจาก 40 แชท มีส่งต่อให้เซลล์ 5 คน และปิดการขายได้ 2 คน
mock_jubili_data = {
    'phone': ['0811111111', '0822222222', '0833333333', '0844444444', '0855555555'],
    'status': ['Won', 'Lost', 'Negotiating', 'Won', 'Negotiating'],
    'value': [50000, 0, 150000, 200000, 0],
    'sales_owner': ['Sale_A', 'Sale_A', 'Sale_B', 'Sale_C', 'Sale_B']
}
jubili_df = pd.DataFrame(mock_jubili_data)
print(f"✅ สร้างข้อมูล JUBILI จำลองเพื่อทดสอบ: พบ {len(jubili_df)} Leads")

# ==========================================
# 3. Data Processing & KPI Calculation
# ==========================================
total_chats = len(ohochat_df)

# กรอง Contact ที่มีคุณภาพ (ตัด Junk/Spam ออก)
# ดึงข้อมูลจากคอลัมน์ tags
if 'tags' in ohochat_df.columns:
    valid_contacts = ohochat_df[~ohochat_df['tags'].str.contains('มือลั่น|แชทผี|ไม่เกี่ยวข้อง|บล็อก', na=False)]
else:
    valid_contacts = ohochat_df

total_contacts = len(valid_contacts)

# คำนวณฝั่ง JUBILI
total_leads = len(jubili_df)
closed_won = len(jubili_df[jubili_df['status'].str.lower() == 'won'])
total_revenue = jubili_df[jubili_df['status'].str.lower() == 'won']['value'].sum()

# คำนวณ Conversion Rates
contact_rate = (total_contacts / total_chats * 100) if total_chats > 0 else 0
lead_conversion_rate = (total_leads / total_contacts * 100) if total_contacts > 0 else 0
win_rate = (closed_won / total_leads * 100) if total_leads > 0 else 0

# ดูเทรนด์ของ Tags (ดึงเฉพาะ 5 อันดับแรก)
if 'tags' in valid_contacts.columns:
    top_tags = valid_contacts['tags'].value_counts().head(5).to_string()
else:
    top_tags = "No tag data available"

# ==========================================
# 4. เตรียม Report & AI Prompt
# ==========================================
report_data = f"""
รายงานประสิทธิภาพ Ads และ Sales (Phase 1)
สัปดาห์: 25 พ.ค. - 31 พ.ค.
- คนทักแชททั้งหมด (Ohochat): {total_chats} คน
- ได้ Contact ลูกค้าจริง: {total_contacts} คน (Contact Rate: {contact_rate:.2f}%)
- ส่งต่อ Lead ให้เซลล์ (JUBILI): {total_leads} คน (Lead Conversion Rate: {lead_conversion_rate:.2f}%)
- ปิดการขายได้ (Won): {closed_won} ราย (Win Rate: {win_rate:.2f}%)
- ยอดขายรวมสัปดาห์นี้: ฿{total_revenue:,.2f}

สัดส่วนความสนใจ/ปัญหาจากแชท (Top 5 Tags):
{top_tags}
"""

print("\n📊 [ข้อมูลที่จะส่งให้ AI วิเคราะห์]")
print(report_data)

system_prompt = """
You are an AI Revenue Intelligence Analyst for a cosmetics OEM company.
Your role is to analyze marketing and sales funnel performance from OhoChat inbound chat data and CRM sales data from JUBILI.

Tasks:
1. Evaluate funnel conversion rates.
2. Detect abnormal drops in performance.
3. Identify highest-performing campaigns or tags.
4. Detect bottlenecks in sales follow-up.
5. Generate executive-level weekly summaries.
6. Recommend actionable improvements.

Output in Thai language, using concise executive language.
"""

# ==========================================
# 5. สั่ง AI Genearate รายงาน
# ==========================================
if GEMINI_API_KEY:
    print("\n🤖 [กำลังเรียกใช้งาน Gemini AI...]")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    full_prompt = f"{system_prompt}\n\nAnalyze this week's data:\n{report_data}"
    response = model.generate_content(full_prompt)
    
    # บันทึกเป็นไฟล์ Markdown
    with open('weekly_ai_report.md', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("\n✨ บันทึกรายงาน AI สรุปผลเรียบร้อยแล้วที่ไฟล์ 'weekly_ai_report.md'")
else:
    print("\n⚠️ [จำลองผลลัพธ์ AI - เนื่องจากยังไม่ได้ใส่ API Key]")
    print("Executive Summary:")
    print("- สัปดาห์นี้ Contact Rate ต่ำกว่าปกติ แนะนำให้ตรวจสอบโฆษณาอาจดึงดูดกลุ่มที่ไม่ตรงเป้าหมาย")
    print("- Win Rate ค่อนข้างดี แสดงว่าเมื่อส่งต่อให้เซลล์แล้ว สินค้า/ราคามีความน่าสนใจ")
    print("\n(หมายเหตุ: โปรดตั้งค่า GEMINI_API_KEY ก่อนรันบน Production เพื่อให้ AI วิเคราะห์ข้อมูลจริง)")
