import pandas as pd
import math

filename = 'บริษัท คอสเมดิวา จำกัด_รายชื่อลูกค้า_ข้อมูลทั่วไป_16 April - 15 May 2026.csv'
try:
    try:
        df = pd.read_csv(filename, encoding='utf-8-sig')
    except:
        df = pd.read_csv(filename, encoding='tis-620')
        
    tag_col = 'tags'
    contact_col = 'phone'
    
    total_chats = len(df)
    
    df[tag_col] = df[tag_col].fillna('')
    df[contact_col] = df[contact_col].fillna('')
    junk_tags = ['ผี', 'เงียบ', 'bot', 'spam', 'สแปม', 'ไม่มีตัวตน', 'อ่านไม่ตอบ', 'ซ้ำ', 'ghost']
    
    def is_qualified(row):
        tags = str(row[tag_col])
        for j in junk_tags:
            if j in tags:
                return False
        return True
        
    def has_contact_info(row):
        contact = str(row[contact_col]).strip()
        if contact and contact.lower() != 'nan' and contact != '-' and len(contact) > 4:
            return True
        return False

    qualified_df = df[df.apply(is_qualified, axis=1)]
    qualified_chats = len(qualified_df)
    
    contacts_with_info = qualified_df[qualified_df.apply(has_contact_info, axis=1)]
    num_contacts = len(contacts_with_info)
    
    print(f"Total Chats: {total_chats}")
    print(f"Qualified Contacts: {qualified_chats}")
    print(f"Provided Contact/Line ID: {num_contacts}")
    
except Exception as e:
    print(f"Error: {e}")
